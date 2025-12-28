use std::fs;

/// Represents the current network and system status of the system
#[derive(Debug, Clone, Default)]
pub struct NetworkStatus {
    pub interface: String,
    pub ip: String,
    pub is_secure: bool, // VPN detected
    pub is_up: bool,
    pub uptime: String,  // HH:MM:SS
    pub cpu_usage: f64,  // 0.0 to 100.0
    pub mem_usage: f64,  // 0.0 to 100.0
    pub mem_total_kb: u64,
    pub mem_used_kb: u64,

    // Internal state for CPU calculation
    pub last_cpu_total: u64,
    pub last_cpu_idle: u64,
}

impl NetworkStatus {
    /// Probe the system for network and system information
    pub fn probe(&mut self) {
        // 1. Probe Network
        self.probe_network();

        // 2. Probe Uptime
        self.probe_uptime();

        // 3. Probe Memory
        self.probe_memory();

        // 4. Probe CPU
        self.probe_cpu();
    }

    fn probe_network(&mut self) {
        if let Ok(entries) = fs::read_dir("/sys/class/net/") {
            let mut interfaces = Vec::new();
            for entry in entries.flatten() {
                let name = entry.file_name().to_string_lossy().into_owned();
                if name == "lo" {
                    continue;
                }
                
                let operstate_path = format!("/sys/class/net/{}/operstate", name);
                if let Ok(state) = fs::read_to_string(operstate_path) {
                    if state.trim() == "up" {
                        interfaces.push(name);
                    }
                }
            }

            let vpn_iface = interfaces.iter().find(|i| {
                i.starts_with("tun") || i.starts_with("tap") || i.starts_with("wg") || i.starts_with("ppp")
            });

            if let Some(iface) = vpn_iface {
                self.interface = iface.clone();
                self.is_secure = true;
                self.is_up = true;
            } else if let Some(iface) = interfaces.first() {
                self.interface = iface.clone();
                self.is_secure = false;
                self.is_up = true;
            } else {
                self.interface = "NONE".to_string();
                self.is_up = false;
            }
        }

        if self.is_up {
            self.ip = get_ip_for_interface(&self.interface).unwrap_or_else(|| "0.0.0.0".to_string());
        } else {
            self.ip = "0.0.0.0".to_string();
        }
    }

    fn probe_uptime(&mut self) {
        if let Ok(uptime_str) = fs::read_to_string("/proc/uptime") {
            if let Some(seconds_str) = uptime_str.split_whitespace().next() {
                if let Ok(seconds) = seconds_str.parse::<f64>() {
                    let total_secs = seconds as u64;
                    let hours = total_secs / 3600;
                    let minutes = (total_secs % 3600) / 60;
                    let secs = total_secs % 60;
                    self.uptime = format!("{:02}:{:02}:{:02}", hours, minutes, secs);
                }
            }
        }
    }

    fn probe_memory(&mut self) {
        if let Ok(meminfo) = fs::read_to_string("/proc/meminfo") {
            let mut mem_total = 0;
            let mut mem_available = 0;

            for line in meminfo.lines() {
                if line.starts_with("MemTotal:") {
                    mem_total = line.split_whitespace().nth(1).and_then(|s| s.parse::<u64>().ok()).unwrap_or(0);
                } else if line.starts_with("MemAvailable:") {
                    mem_available = line.split_whitespace().nth(1).and_then(|s| s.parse::<u64>().ok()).unwrap_or(0);
                }
            }

            if mem_total > 0 {
                let used = mem_total.saturating_sub(mem_available);
                self.mem_total_kb = mem_total;
                self.mem_used_kb = used;
                self.mem_usage = (used as f64 / mem_total as f64) * 100.0;
            }
        }
    }

    fn probe_cpu(&mut self) {
        if let Ok(stat) = fs::read_to_string("/proc/stat") {
            if let Some(line) = stat.lines().next() {
                let parts: Vec<u64> = line.split_whitespace()
                    .skip(1)
                    .filter_map(|s| s.parse::<u64>().ok())
                    .collect();

                if parts.len() >= 4 {
                    let idle = parts[3];
                    let total: u64 = parts.iter().sum();

                    let total_delta = total.saturating_sub(self.last_cpu_total);
                    let idle_delta = idle.saturating_sub(self.last_cpu_idle);

                    if total_delta > 0 {
                        self.cpu_usage = 100.0 * (1.0 - (idle_delta as f64 / total_delta as f64));
                    }

                    self.last_cpu_total = total;
                    self.last_cpu_idle = idle;
                }
            }
        }
    }
}

/// Helper to get IP address for a specific interface using nix
fn get_ip_for_interface(interface_name: &str) -> Option<String> {
    use nix::ifaddrs::getifaddrs;
    use nix::sys::socket::SockAddr;
    
    if let Ok(addrs) = getifaddrs() {
        for ifaddr in addrs {
            if ifaddr.interface_name == interface_name {
                if let Some(address) = ifaddr.address {
                    if let SockAddr::Inet(inet) = address {
                        return Some(inet.ip().to_string());
                    }
                }
            }
        }
    }
    None
}

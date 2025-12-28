use ratatui::{
    backend::Backend,
    layout::{Alignment, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::Paragraph,
    Frame,
};

use super::network::NetworkStatus;
use super::status_message::{InfoStatusMessage, StatusMessage};

/// Sci-Fi Footer Decoration Widget
/// Displays dynamic "System Vitals" like CPU and RAM usage
#[derive(Clone)]
pub struct FooterDecoWidget {
    primary_color: Color,
    dim_color: Color,
    accent_color: Color,
}

impl Default for FooterDecoWidget {
    fn default() -> Self {
        Self {
            primary_color: Color::Rgb(28, 237, 255), // #1CEDFF
            dim_color: Color::Rgb(80, 80, 80),        // Dim gray
            accent_color: Color::Rgb(255, 51, 51),    // Red for high usage
        }
    }
}

impl FooterDecoWidget {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn render(&self, frame: &mut Frame<impl Backend>, area: Rect, network: &NetworkStatus, status: Option<StatusMessage>, elapsed_ms: u64) {
        let green = Style::default().fg(Color::Rgb(0, 255, 65));
        let green_bold = green.add_modifier(Modifier::BOLD);
        let dim = Style::default().fg(self.dim_color);

        if matches!(status, Some(StatusMessage::Info(InfoStatusMessage::LoggingIn))) {
            // Animation settings
            let typing_speed = 30; // ms per char (Slower for deliberate sequence)
            
            // Log Line Definitions: (Base Text, Suffix, Suffix Display Duration MS)
            let log_data = vec![
                ("INITIALIZING KERNEL MODULES: ", "[ DONE ]", 400),
                ("MOUNTING ENCRYPTED ARCHIVES: ", "[ SUCCESS ]", 500),
                ("ESTABLISHING SECURE TUNNEL: ", "[ LINKED ]", 600),
                ("VERIFYING SYSTEM INTEGRITY: ", "[ PASSED ]", 400),
                ("SYNCHRONIZING USER PREFERENCES: ", "[ SYNCED ]", 500),
                ("EXECUTING POST-AUTH SCRIPTS: ", "[ COMPLETE ]", 600),
                ("SPECTRE SYSTEM: ", "[ ONLINE | READY ]", 1000),
            ];

            let mut lines = Vec::new();
            let mut current_total_time = 0;

            for (base, suffix, suffix_duration) in log_data {
                let start_delay = current_total_time;
                let typing_duration = base.len() as u64 * typing_speed;
                let line_duration = typing_duration + suffix_duration + 100; // 100ms pause between lines
                
                // Advance the global timer for the next line
                current_total_time += line_duration;

                let line_elapsed = elapsed_ms.saturating_sub(start_delay);
                if line_elapsed == 0 {
                    lines.push(Line::from(vec![Span::styled(" ", dim)]));
                    continue;
                }

                let chars_to_show = (line_elapsed / typing_speed) as usize;
                
                // Show base text revealed over time
                let show_base = &base[0..chars_to_show.min(base.len())];
                let base_complete = chars_to_show >= base.len();

                let mut spans = vec![
                    Span::styled("[ LOG ] ", dim),
                    Span::styled(show_base, green),
                ];

                // Show suffix only after base is fully typed
                if base_complete && line_elapsed >= typing_duration {
                    spans.push(Span::styled(suffix, green_bold));
                }

                lines.push(Line::from(spans));
            }

            let paragraph = Paragraph::new(lines)
                .alignment(Alignment::Center);

            frame.render_widget(paragraph, area);
            return;
        }

        let primary = Style::default().fg(self.primary_color);
        let dim = Style::default().fg(self.dim_color);
        let primary_bold = primary.add_modifier(Modifier::BOLD);

        // CPU Usage Bar
        let cpu_pct = network.cpu_usage;
        let cpu_bar = self.make_bar(cpu_pct, 20);
        let cpu_style = if cpu_pct > 80.0 { Style::default().fg(self.accent_color) } else { primary };

        let cpu_line = Line::from(vec![
            Span::styled("CPU_LOAD: [", dim),
            Span::styled(cpu_bar, cpu_style),
            Span::styled("] ", dim),
            Span::styled(format!("{:>5.1}%", cpu_pct), primary_bold),
            Span::styled(" :: ", dim),
            Span::styled("STATUS: ", dim),
            Span::styled("ACTIVE", primary),
        ]);

        // Memory Usage Bar
        let mem_pct = network.mem_usage;
        let mem_bar = self.make_bar(mem_pct, 20);
        let mem_style = if mem_pct > 90.0 { Style::default().fg(self.accent_color) } else { primary };
        
        let mem_line = Line::from(vec![
            Span::styled("MEM_USED: [", dim),
            Span::styled(mem_bar, mem_style),
            Span::styled("] ", dim),
            Span::styled(format!("{:>5.1}%", mem_pct), primary_bold),
            Span::styled(" :: ", dim),
            Span::styled(format!("{:.1}GB / {:.1}GB", network.mem_used_kb as f64 / 1024.0 / 1024.0, network.mem_total_kb as f64 / 1024.0 / 1024.0), primary),
        ]);

        let paragraph = Paragraph::new(vec![cpu_line, mem_line])
            .alignment(Alignment::Center);

        frame.render_widget(paragraph, area);
    }

    fn make_bar(&self, pct: f64, width: usize) -> String {
        let filled = ((pct / 100.0) * width as f64).round() as usize;
        let empty = width.saturating_sub(filled);
        format!("{}{}", "|".repeat(filled), ".".repeat(empty))
    }
}

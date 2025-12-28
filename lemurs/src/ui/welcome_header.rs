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

/// Sci-Fi Welcome Header Widget
/// Displays an extreme futuristic NASA/Cyberpunk style authentication banner
/// PERFECT RECTANGLE (70 characters wide)
#[derive(Clone)]
pub struct WelcomeHeaderWidget {
    primary_color: Color,
    accent_color: Color,
    dim_color: Color,
}

impl Default for WelcomeHeaderWidget {
    fn default() -> Self {
        Self {
            primary_color: Color::Rgb(28, 237, 255),  // #1CEDFF - Cyan
            accent_color: Color::Rgb(255, 51, 51),     // #FF3333 - Red
            dim_color: Color::Rgb(80, 80, 80),         // Dim gray
        }
    }
}

impl WelcomeHeaderWidget {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn render(&self, frame: &mut Frame<impl Backend>, area: Rect, network: NetworkStatus, status: Option<StatusMessage>) {
        let primary = Style::default()
            .fg(self.primary_color)
            .add_modifier(Modifier::BOLD);
        
        let accent = Style::default()
            .fg(self.accent_color)
            .add_modifier(Modifier::BOLD);
        
        let dim = Style::default()
            .fg(self.dim_color);

        let primary_dim = Style::default()
            .fg(Color::Rgb(20, 160, 180)); // Dimmer cyan

        // Define a fixed width for the entire header box to ensure a "perfect rectangle"
        let width: usize = 70;

        // Line 1: Top Border (Removed Agency Names)
        // <<(2) + =========================================(41) + [ SECURE TERMINAL ](19) + =======(6) + >>(2) = 70
        let top_border = Line::from(vec![
            Span::styled("<<", accent),
            Span::styled("=========================", dim),
            Span::styled("[ ", primary_dim),
            Span::styled("SECURE TERMINAL", primary),
            Span::styled(" ]", primary_dim),
            Span::styled("=========================", dim),
            Span::styled(">>", accent),
        ]);

        // Check if we are logging in to show a "Welcome back" splash
        let is_logging_in = matches!(status, Some(StatusMessage::Info(InfoStatusMessage::LoggingIn)));
        let green = Style::default().fg(Color::Rgb(0, 255, 65)).add_modifier(Modifier::BOLD);

        // Line 5: Bottom Border (Uptime moved to RIGHT bracket)
        let (sec_text, sec_style) = if network.is_secure {
            (" SECURE ", primary)
        } else {
            (" PUBLIC ", accent)
        };

        // Up: HH:MM:SS is 12 chars
        let uptime_text = format!("UP: {}", network.uptime);

        let bottom_border = Line::from(vec![
            Span::styled("<<", accent),
            Span::styled("==", dim),
            Span::styled("[", primary_dim),
            Span::styled(sec_text, sec_style),
            Span::styled("]", primary_dim),
            Span::styled("==========================================", dim),
            Span::styled("[", primary_dim),
            Span::styled(uptime_text, primary_dim),
            Span::styled("]", primary_dim),
            Span::styled("==", dim),
            Span::styled(">>", accent),
        ]);

        let lines = if is_logging_in {
            // CINEMATIC SPLASH MODE
            let splash_line1 = self.format_aligned_inner(" ", green, dim, width);
            let splash_line2 = self.format_aligned_inner(">>>>> WELCOME BACK, SIR <<<<<", green, dim, width);
            let splash_line3 = self.format_aligned_inner("SESSION AUTHENTICATED: LEVEL ALPHA", green, dim, width);
            let splash_line4 = self.format_aligned_inner(" ", green, dim, width);
            vec![top_border, splash_line1, splash_line2, splash_line3, splash_line4, bottom_border]
        } else {
            // NORMAL HUD MODE
            // Line 2: Title (Centered in || bars)
            let line2_text = ">>> SYSTEM ACCESS TERMINAL <<<";
            let line2 = self.format_aligned_inner(line2_text, primary, dim, width);

            // Line 3: Auth Warning (Centered in || bars)
            let line3_content = vec![
                Span::styled("[!] ", accent),
                Span::styled("AUTHENTICATION REQUIRED", primary),
                Span::styled(" - ", dim),
                Span::styled("CLASSIFIED LEVEL: ALPHA", accent),
                Span::styled(" [!] ", accent),
            ];
            let line3 = self.format_aligned_spans(line3_content, dim, width);

            // Line 4: Technical Telemetry (Live Data)
            let link_status = if network.is_up { "LINK: UP" } else { "LINK: DOWN" };
            let link_style = if network.is_up { primary_dim } else { accent };
            
            let line4_content = vec![
                Span::styled(link_status, link_style),
                Span::styled(" | ", dim),
                Span::styled("IP: ", dim),
                Span::styled(network.ip, primary_dim),
                Span::styled(" | ", dim),
                Span::styled("IFACE: ", dim),
                Span::styled(network.interface, primary_dim),
            ];
            let line4 = self.format_aligned_spans(line4_content, dim, width);
            vec![top_border, line2, line3, line4, bottom_border]
        };

        let paragraph = Paragraph::new(lines)
            .alignment(Alignment::Center);

        frame.render_widget(paragraph, area);
    }

    /// Helper to format a line with vertical bars and centered text
    fn format_aligned_inner<'a>(&self, text: &'a str, style: Style, dim: Style, total_width: usize) -> Line<'a> {
        let padding = total_width.saturating_sub(text.len() + 4); // 4 for "|| " and " ||"
        let left_pad = padding / 2;
        let right_pad = padding - left_pad;

        Line::from(vec![
            Span::styled("||", dim),
            Span::raw(" ".repeat(left_pad)),
            Span::styled(text, style),
            Span::raw(" ".repeat(right_pad)),
            Span::styled("||", dim),
        ])
    }

    /// Helper to format a line with vertical bars and centered spans
    fn format_aligned_spans<'a>(&self, content: Vec<Span<'a>>, dim: Style, total_width: usize) -> Line<'a> {
        let content_len: usize = content.iter().map(|s| s.content.len()).sum();
        let padding = total_width.saturating_sub(content_len + 4);
        let left_pad = padding / 2;
        let right_pad = padding - left_pad;

        let mut spans = vec![
            Span::styled("||", dim),
            Span::raw(" ".repeat(left_pad)),
        ];
        spans.extend(content);
        spans.push(Span::raw(" ".repeat(right_pad)));
        spans.push(Span::styled("||", dim));

        Line::from(spans)
    }
}

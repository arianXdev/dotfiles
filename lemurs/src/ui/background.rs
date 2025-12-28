use ratatui::{
    layout::{Alignment, Rect},
    style::Style,
    widgets::{Block, Paragraph},
    Frame,
};

use crate::config::{get_color, BackgroundConfig};

#[derive(Clone)]
pub struct BackgroundWidget {
    config: BackgroundConfig,
}

impl BackgroundWidget {
    pub fn new(config: BackgroundConfig) -> Self {
        Self { config }
    }

    pub fn render(&self, frame: &mut Frame<impl ratatui::backend::Backend>) {
        if !self.config.show_background {
            return;
        }

        let size = frame.size();
        
        // 1. Render the background color using a block
        let bg_block = Block::default().style(self.background_style());
        frame.render_widget(bg_block, size);

        // 2. Render Custom ASCII Borders (Extreme Sci-Fi Style)
        let border_style = self.border_style();
        let width = size.width as usize;
        let height = size.height as usize;

        if width < 2 || height < 2 {
            return;
        }

        // Top Line (Cleaned up corners: replaced '+' with '=')
        let title_text = " :: TERMINAL ACTIVE :: ";
        let dash_count = (width.saturating_sub(title_text.len() + 2)) / 2;
        let top_line = format!(
            "={}[{}]{}=",
            "=".repeat(dash_count),
            title_text,
            "=".repeat(width.saturating_sub(dash_count + title_text.len() + 2))
        );
        let top_widget = Paragraph::new(top_line)
            .style(border_style)
            .alignment(Alignment::Center);
        frame.render_widget(top_widget, Rect::new(0, 0, size.width, 1));

        // Bottom Line (Cleaned up corners: replaced '+' with '=')
        let bottom_text = " :: SECURE CONNECTION :: ";
        let dash_count_b = (width.saturating_sub(bottom_text.len() + 2)) / 2;
        let bottom_line = format!(
            "={}[{}]{}=",
            "=".repeat(dash_count_b),
            bottom_text,
            "=".repeat(width.saturating_sub(dash_count_b + bottom_text.len() + 2))
        );
        let bottom_widget = Paragraph::new(bottom_line)
            .style(border_style)
            .alignment(Alignment::Center);
        frame.render_widget(bottom_widget, Rect::new(0, size.height - 1, size.width, 1));

        // Side Lines (Vertical using '|')
        let inner_height = height.saturating_sub(2);
        if inner_height > 0 {
            let mut side_str = String::with_capacity(inner_height * 2);
            for _ in 0..inner_height {
                side_str.push_str("|\n");
            }

            // Left Side
            let left_widget = Paragraph::new(side_str.clone()).style(border_style);
            frame.render_widget(left_widget, Rect::new(0, 1, 1, inner_height as u16));

            // Right Side
            let right_widget = Paragraph::new(side_str).style(border_style);
            frame.render_widget(right_widget, Rect::new(size.width - 1, 1, 1, inner_height as u16));
        }
    }

    fn background_style(&self) -> Style {
        Style::default().bg(get_color(&self.config.style.color))
    }
    fn border_style(&self) -> Style {
        Style::default().fg(get_color(&self.config.style.green_color))
    }
}

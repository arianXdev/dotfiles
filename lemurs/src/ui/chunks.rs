use ratatui::{
    backend::Backend,
    layout::{Constraint, Direction, Layout, Rect},
    Frame,
};
use Constraint::{Length, Min};

pub struct Chunks {
    pub key_menu: Rect,
    pub welcome_header: Rect,
    pub username_field: Rect,
    pub password_field: Rect,
    pub status_message: Rect,
    pub footer_deco: Rect,
}

impl Chunks {
    pub fn new<B: Backend>(frame: &Frame<B>) -> Self {
        let size = frame.size();
        
        // Calculate the content height needed for centered elements
        // Welcome header: 6 lines, gap: 2, username: 3, gap: 1, password: 3, gap: 1, status: 1, footer: 8
        let content_height: u16 = 6 + 2 + 3 + 1 + 3 + 1 + 1 + 8; // = 25
        
        // Calculate top padding to center content vertically
        let available_height = size.height.saturating_sub(4); 
        let top_padding = if available_height > content_height {
            (available_height - content_height) / 2
        } else {
            0
        };

        let constraints = [
            Length(1),              // [0] key_menu (power controls) - top
            Length(1),              // [1] spacer after key menu
            Length(top_padding),    // [2] dynamic top padding for centering
            Length(6),              // [3] welcome_header (sci-fi banner)
            Length(2),              // [4] gap after header
            Length(3),              // [5] username_field
            Length(1),              // [6] gap
            Length(3),              // [7] password_field
            Length(1),              // [8] gap
            Length(1),              // [9] status_message
            Length(1),              // [10] gap before footer
            Length(8),              // [11] footer_deco
            Min(0),                 // [12] remaining space
        ];

        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .horizontal_margin(2)
            .vertical_margin(1)
            .constraints(constraints.as_ref())
            .split(size);

        Self {
            key_menu: chunks[0],
            welcome_header: chunks[3],
            username_field: chunks[5],
            password_field: chunks[7],
            status_message: chunks[9],
            footer_deco: chunks[11],
        }
    }
}

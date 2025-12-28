use ratatui::backend::Backend;
use ratatui::layout::{Alignment, Rect};
use ratatui::style::{Color, Modifier, Style};
use ratatui::widgets::Paragraph;
use ratatui::Frame;

use crate::auth::AuthenticationError;

#[derive(Clone)]
pub enum ErrorStatusMessage {
    AuthenticationError(AuthenticationError),
    NoGraphicalEnvironment,
    FailedGraphicalEnvironment,
    FailedDesktop,
    FailedPowerControl(String),
}

impl From<ErrorStatusMessage> for Box<str> {
    fn from(err: ErrorStatusMessage) -> Self {
        use ErrorStatusMessage::*;

        match err {
            AuthenticationError(_) => "[ERR] >> AUTHENTICATION FAILED <<".into(),
            NoGraphicalEnvironment => "[ERR] >> NO ENVIRONMENT SPECIFIED <<".into(),
            FailedGraphicalEnvironment => "[ERR] >> ENVIRONMENT BOOT FAILURE <<".into(),
            FailedDesktop => "[ERR] >> DESKTOP INIT FAILURE <<".into(),
            FailedPowerControl(name) => {
                format!("[ERR] >> FAILED: {name} <<").into()
            }
        }
    }
}

impl From<ErrorStatusMessage> for StatusMessage {
    fn from(err: ErrorStatusMessage) -> Self {
        Self::Error(err)
    }
}

#[derive(Clone, Copy)]
pub enum InfoStatusMessage {
    LoggingIn,
    Authenticating,
}

impl From<InfoStatusMessage> for Box<str> {
    fn from(info: InfoStatusMessage) -> Self {
        use InfoStatusMessage::*;

        match info {
            LoggingIn => "[SYS] >> AUTH SUCCESS :: INITIATING SESSION <<".into(),
            Authenticating => "[SYS] >> VERIFYING CREDENTIALS... <<".into(),
        }
    }
}

impl From<InfoStatusMessage> for StatusMessage {
    fn from(info: InfoStatusMessage) -> Self {
        Self::Info(info)
    }
}

#[derive(Clone)]
pub enum StatusMessage {
    Error(ErrorStatusMessage),
    Info(InfoStatusMessage),
}

impl From<StatusMessage> for Box<str> {
    fn from(msg: StatusMessage) -> Self {
        use StatusMessage::*;

        match msg {
            Error(sm) => sm.into(),
            Info(sm) => sm.into(),
        }
    }
}

impl StatusMessage {
    /// Fetch whether status is an error
    pub fn is_error(&self) -> bool {
        matches!(self, Self::Error(_))
    }

    pub fn render<B: Backend>(status: Option<Self>, frame: &mut Frame<B>, area: Rect) {
        if let Some(status_message) = status {
            let text: Box<str> = status_message.clone().into();
            let color = if status_message.is_error() {
                Color::Rgb(255, 51, 51)  // #FF3333 - Red for errors
            } else {
                Color::Rgb(28, 237, 255) // #1CEDFF - Cyan for info
            };
            let widget = Paragraph::new(text.as_ref())
                .style(Style::default().fg(color).add_modifier(Modifier::BOLD))
                .alignment(Alignment::Center);

            frame.render_widget(widget, area);
        } else {
            // Clear the area
            let widget = Paragraph::new("");
            frame.render_widget(widget, area);
        }
    }
}

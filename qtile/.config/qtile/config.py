# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this perbmission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, ScratchPad, DropDown, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

# GLOBAL VARIABLES
mod = "mod4"
alt = "mod1"
myTerm = "alacritty"
myBrowser = "brave"


# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == "monadtall":
        qtile.current_group.layout = "max"
    elif current_layout_name == "max":
        qtile.current_group.layout = "monadtall"


# KEYS
keys = [
    # The essentials
    Key([alt], "Return", lazy.spawn(myTerm + " -e tmux"), desc="Launch terminal"),
    Key([mod], "t", lazy.group["scratchpad"].dropdown_toggle("yazi")),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Brave Browser"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([alt], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    Key([mod], "z", lazy.hide_show_bar(position="all"), desc="Toggles the bar to show/hide"),
    KeyChord(
        [mod],
        "o",
        [
            Key([], "p", lazy.group["scratchpad"].dropdown_toggle("volume")),
            Key([], "1", lazy.group["scratchpad"].dropdown_toggle("term")),
            Key([], "2", lazy.group["scratchpad"].dropdown_toggle("term-2")),
            Key([], "3", lazy.group["scratchpad"].dropdown_toggle("term-3")),
            Key([], "4", lazy.group["scratchpad"].dropdown_toggle("term-4")),
        ],
    ),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([alt], "Tab", lazy.group.next_window()),
    Key([mod, "shift"], "space", lazy.layout.flip()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),
    ### Switch focus to specific monitor (out of three)
    Key([alt], "w", lazy.to_screen(1), desc="Keyboard focus to monitor 1"),
    Key([alt], "e", lazy.to_screen(0), desc="Keyboard focus to monitor 2"),
    Key([mod], "u", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Key([], "f1", lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle"), lazy.widget["genpollcommand"].force_update(), desc="Handle the microphone"),
    # Key([], "f4", lazy.spawn("pactl set-card-profile bluez_card.14_2C_78_13_1D_14 a2dp_sink"), lazy.widget["genpollcommand"].force_update(), desc="Switch to the headset mode"),
    # Key([], "f5", lazy.spawn("pactl set-card-profile bluez_card.14_2C_78_13_1D_14 handsfree_head_unit"), lazy.widget["genpollcommand"].force_update(), desc="Switch to the microphone mode"),
    Key([mod], "space", lazy.spawn("setxkbmap us"), desc=""),
    Key([mod], "i", lazy.spawn("setxkbmap ir"), desc=""),
]

# GROUPS
groups = []
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]
group_labels = [
    "$$$",
    ">--",
    "</>",
    "WWW",
    "MUS",
    "VID",
    "COMM",
    "STUFF",
    "SYSTEM",
]
group_layouts = ["monadtall", "monadtall", "max", "max", "tile", "floating", "floating", "max", "floating"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

# SCRATCHPADS
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown("term", "alacritty --class=scratch", width=0.8, height=0.5, x=0.1, y=0.1, opacity=0.98, on_focus_lost_hide=False),
            DropDown("term-2", "alacritty --class=scratch -e tmux a", width=0.8, height=0.6, x=0.1, y=0.1, opacity=0.98, on_focus_lost_hide=False),
            DropDown("term-3", "alacritty --class=scratch", width=0.8, height=0.5, x=0.1, y=0.1, opacity=0.98, on_focus_lost_hide=False),
            DropDown("term-4", "alacritty --class=scratch", width=0.8, height=0.5, x=0.1, y=0.2, opacity=0.95, on_focus_lost_hide=False),
            DropDown("yazi", "alacritty --class=yazi -e yazi", width=0.8, height=0.58, x=0.1, y=0.1, opacity=1, on_focus_lost_hide=False),
            DropDown("volume", "alacritty --class=pulsemixer -e pulsemixer", width=0.6, height=0.4, x=0.2, y=0.2, opacity=1, on_focus_lost_hide=True),
        ],
    )
)

# LAYOUTS
layout_theme = {"border_width": 2, "margin": 6, "border_focus": "007efc", "border_normal": "777777"}

layouts = [
    layout.Tile(
        shift_windows=True,
        border_width=0,
        margin=0,
        ratio=0.335,
    ),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Columns(
        border_normal="777777",
        border_focus="007efc",
        margin=3,
    ),
]

colors = [
    ["#282c34", "#282c34"],
    ["#1c1f24", "#1c1f24"],
    ["#dfdfdf", "#dfdfdf"],
    ["#FB3048", "#FB3048"],
    ["#98be65", "#98be65"],
    ["#da8548", "#da8548"],
    ["#51afef", "#51afef"],
    ["#c678dd", "#c678dd"],
    ["#46d9ff", "#46d9ff"],
    ["#a9a1e1", "#a9a1e1"],
    ["#1CEDFF", "#1CEDFF"],
]


# WIDGETS
widget_defaults = dict(
    font="Operator Mono",
    fontsize=12,
    padding=4,
)

extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
        widget.Spacer(length=6),
        widget.GroupBox(
            margin_y=3,
            margin_x=1,
            padding_y=5,
            padding_x=3,
            borderwidth=3,
            active=colors[2],
            block_highlight_text_color=colors[3],
            inactive=colors[6],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="line",
            this_current_screen_border=colors[3],
            this_screen_border=colors[1],
            other_current_screen_border=colors[1],
            other_screen_border=colors[0],
            disable_drag=True,
            toggle=False,
            urgent_alert_method="text",
        ),
        widget.TextBox(text="|", font="Ubuntu Mono", foreground=colors[6], padding=2, fontsize=14),
        widget.CurrentLayoutIcon(scale=0.64, use_mask=True, foreground=colors[10]),
        widget.Prompt(
            prompt="COMMAND: ",
            fontsize=13,
            foreground="00e325",
            cursor=True,
            padding=10,
        ),
        widget.Spacer(length=4),
        widget.WindowName(
            max_chars=40,
            font="Oxanium SemiBold",
        ),
        widget.Cmus(noplay_color="#ff0011", font="Tektur Medium", fontsize=12.9, format="{play_icon}{artist} / {album} - {title}"),
        widget.Spacer(length=4),
        widget.Pomodoro(),
        widget.Spacer(length=4),
        widget.Volume(
            font="Oxanium SemiBold",
            fontsize=12.4,
            foreground=colors[7],
            volume_app="pamixer",
            get_volume_command="pamixer --get-volume-human",
            check_mute_command="pamixer --get-mute",
        ),
        widget.Memory(
            font="Oxanium SemiBold",
            fontsize=12.5,
            foreground=colors[10],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(myTerm + " -e btop")},
            format="{MemUsed: .0f} out of{MemTotal: .0f} ({MemPercent}%)",
        ),
        widget.Spacer(length=4),
        widget.KeyboardLayout(
            configured_keyboards=["us", "ir"],
            display_map={"ir": "🇦🇶", "us": "🇺🇸"},
        ),
        widget.Spacer(length=4),
        widget.CurrentLayout(
            font="Oxanium SemiBold",
            fontsize=12.1,
        ),
        widget.Spacer(length=4),
        widget.GenPollCommand(
            cmd="/home/spectre/GitHub/dotfiles/scripts/check-microphone",
            shell=True,
            fmt="<i>{}</i>",
            foreground="#e30526",
        ),
        widget.TextBox(text="|", font="Ubuntu Mono", foreground=colors[6], padding=2, fontsize=14),
        widget.Spacer(length=4),
        widget.Clock(
            font="Oxanium Medium",
            fontsize=13,
            foreground="#000000",
            format="%H:%M %a, %B %d",
            decorations=[RectDecoration(filled=True, colour=colors[3], radius=6, padding_y=4)],
        ),
        widget.Spacer(length=4),
        widget.TextBox(text="|", font="Ubuntu Mono", foreground=colors[6], padding=2, fontsize=14),
        widget.Systray(icon_size=18),
        widget.Spacer(length=4),
        widget.CPUGraph(
            border_width=0,
            start_pos="bottom",
            fill_color=colors[3],
            graph_color=colors[8],
            padding=2,
        ),
        widget.Spacer(length=4),
        widget.Redshift(
            # disabled_txt="󱄼",
            disabled_txt="󰒙",
            enabled_txt="󱁝",
            fontsize=17,
            padding=6,
            font="Oxanium",
            temperature=3500,
        ),
        widget.Spacer(length=4),
        widget.DoNotDisturb(disabled_icon="󰂵", enabled_icon="󰄻", fontsize=20, fmt="{} "),
    ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    # del widgets_screen1[19]
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    # del widgets_screen2[16]
    # widgets_screen2.pop()
    return widgets_screen2


# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, margin=1)), Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, margin=1))]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    # border_focus=colors[8],
    border_width=0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="dialog"),  # dialog boxes
        Match(wm_class="download"),  # downloads
        Match(wm_class="error"),  # error msgs
        Match(wm_class="notification"),  # notifications
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="toolbar"),  # toolbars
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Tor Browser"),
        Match(title="DevTools"),
        Match(title="Qalculate!"),  # qalculate-gtk
        Match(wm_class="Windscribe"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="anydesk"),
        Match(wm_class="lxappearance"),
        Match(wm_class="feh"),
        Match(wm_class="viewnior"),
        Match(wm_class="crx_nkbihfbeogaeaoehlefnkodbefgpgknn"),  # MetaMask Notification
        Match(wm_class="btop"),
        Match(wm_class="flameshot"),
        Match(wm_class="MEGAsync"),
        Match(wm_class="qv2ray"),
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


@hook.subscribe.client_new
def display_apps_in_certain_groups(window):
    wm_class = window.window.get_wm_class()
    if not wm_class:
        return

    if "teams-for-linux" in wm_class:
        window.togroup("7")
    elif "brave-browser" in wm_class:
        window.togroup("4")
    elif "Windscribe" in wm_class:
        window.togroup("9")
    elif "megasync" in wm_class:
        window.togroup("6")
    elif "Telegram" in wm_class:
        window.togroup("7")
    elif "thunderbird" in wm_class:
        window.togroup("1")
    elif "qv2ray" in wm_class:
        window.togroup("9")

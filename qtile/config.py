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
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy

from libqtile.utils import guess_terminal

# GLOBAL VARIABLES
myTerm = "alacritty"
myBrowser = "brave"
mod = "mod4"
alt = "mod1"
terminal = guess_terminal()

# KEYS
keys = [
    Key([mod], "b",
        lazy.spawn(myBrowser),
        desc='Brave Browser'
    ),

    Key([mod], "t",
        lazy.spawn("pcmanfm"),
        desc='Graphical File Manager'
    ),

    Key([mod], 'd', lazy.spawn("dmenu_run"), desc="Launch dmenu"),
    
    # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
    KeyChord([mod], "p", [
        Key([], "h", lazy.spawn("dm-hub"), desc='List all dmscripts'),
        Key([], "i", lazy.spawn("dm-maim"), desc='Take a screenshot'),
        Key([], "k", lazy.spawn("dm-kill"), desc='Kill processes'),
        Key([], "w", lazy.spawn("dm-wifi"), desc='Connect to wifi'),
        Key([], "n", lazy.spawn("dm-note"), desc='Store and copy notes'),
        Key([], "c", lazy.spawn("clipmenu"), desc='Clipboard'),
        Key([], "d", lazy.spawn("dm-longman"), desc='Look up words in Longman dictionary'),
        Key([], "t", lazy.spawn("/opt/brave-bin/brave --profile-directory=Default --app-id=majiogicmcnmdhhlgmkahaleckhjbmlk"), desc='Launch Telegram Web through Brave'),
        Key([], "s", lazy.spawn("dm-websearch"), desc='Search various engines'),
    ]),

    # Start SPECTRE DEX Development server & local Ethereum Blockchain
    Key([mod], "s",
        lazy.spawn("alacritty --working-directory /home/spectre/Projects/spectre-decentralized-exchange -T 'Local Ethereum Blockchain' -e npx hardhat node"),
        lazy.spawn("alacritty --working-directory /home/spectre/Projects/spectre-decentralized-exchange -T 'SPECTRE Deployment' -e npm run deploy"),
        lazy.spawn("alacritty --working-directory /home/spectre/Projects/spectre-decentralized-exchange -T 'VITE Server' -e npm run dev"),
        desc='Start SPECTRE DEX needed libraries'
    ),
    
    # Floating windows
    Key([alt], "f",
        lazy.window.toggle_floating(),
        desc="Toggle floating",
    ),

    Key([alt], "Tab",
        lazy.group.next_window()
    ),
    
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
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
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill focused window'
    ),

    Key([mod], "f",
            lazy.window.toggle_fullscreen(),
            desc='Put the focused window to/from fullscreen mode'
    ),

    ### Switch focus to specific monitor (out of three)
    Key([mod], "w",
            lazy.to_screen(0),
            desc='Keyboard focus to monitor 1'
    ),

    Key([mod], "e",
            lazy.to_screen(1),
            desc='Keyboard focus to monitor 2'
    ),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "l", lazy.spawn("slock"), desc="Lock the screen using slock"),
    
    # Sound control
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),

    # Keyboard Layout
    Key([mod], "space",
        lazy.spawn("setxkbmap us"), 
        desc= "Change to US layout"),
    Key([mod],"i",
        lazy.spawn("setxkbmap ir"),
        desc= "Change to Persian layout"),
]

# GROUPS
groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8"]

group_labels = ["WWW", "TER", "DEV", "WEB", "MUS", "BLK", "VID", "ETC"]
# group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
 
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


# LAYOUTS
layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": "007efc",
    "border_normal": "777777"
}

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    # layout.Stack(num_stacks=2),
    #layout.Zoomy(**layout_theme),
    
    layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

colors = [
    ["#282c34", "#282c34"],
    ["#1c1f24", "#1c1f24"],
    ["#dfdfdf", "#dfdfdf"],
    ["#ff6c6b", "#ff6c6b"],
    ["#98be65", "#98be65"],
    ["#da8548", "#da8548"],
    ["#51afef", "#51afef"],
    ["#c678dd", "#c678dd"],
    ["#46d9ff", "#46d9ff"],
    ["#a9a1e1", "#a9a1e1"]
]


# WIDGETS
widget_defaults = dict(
    font="Operator Mono",
    fontsize=12,
    padding=3,
    # background=colors[1]
)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
         widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                    # background = colors[0]
                ),
            widget.GroupBox(
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       block_highlight_text_color = colors[3],
                       inactive = colors[6],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[3],
                       this_screen_border = colors[1],
                       other_current_screen_border = colors[1],
                       other_screen_border = colors[0],
                       disable_drag = True,
                    #    foreground = colors[2],
                    #    background = colors[0]
                ),
                widget.Prompt(
                    prompt="command: ",
                    foreground = '00e325',
                    cursor = True,
                    padding = 10,
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 5,
                ),
                widget.WindowName(),
                widget.Cmus(noplay_color='eee82d'),
                widget.Sep(
                    linewidth = 0,
                    padding = 10,
                    foreground = colors[0],
                ),
                widget.PulseVolume(
                    foreground = colors[7],
                    padding = 5,
                ),
                widget.Memory(
                    foreground = colors[9],
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                    fmt = 'Mem: {}',
                    padding = 6,
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 3,
                    foreground = colors[0],
                ),
                widget.ThermalSensor(
                    foreground = colors[4],
                    threshold = 90,
                    padding = 2,
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[0],
                ),
                widget.KeyboardLayout(
                    configured_keyboards = ['us', 'ir'],
                    display_map = { 'ir': 'fa' },
                    foreground = colors[2],
                    padding = 5,
                ),
                widget.CurrentLayout(padding=6),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                ),
                widget.Systray(
                    padding = 3
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                ),
                widget.Clock(
                    foreground = colors[6],
                    format = "%A, %B %d | %H:%M ",
                ),
        ]
    return widgets_list

# Monitor 1 will display ALL widgets in widgets_list. It is important that this
# is the only monitor that displays all widgets because the systray widget will
# crash if you try to run multiple instances of it.
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1 

# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[15:17], widgets_screen2[5:8]
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26))]

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
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Tor Browser"),
        Match(title="MetaMask Notification"),
        Match(title="DevTools"),
        Match(wm_class="persepolis"),
    ]
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
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.client_new
def display_apps_in_certain_groups(window):
    if window.name == "Persepolis Download Manager":
        window.togroup("8")
    elif window.name == "Visual Studio Code":
        window.togroup("3")
    elif window.name == "New Tab - Brave":
        window.togroup("4")
    elif window.name == "cmus":
        window.togroup("5")
    elif window.name == "Local Ethereum Blockchain":
        window.togroup("6")
    elif window.name == "SPECTRE Deployment":
        window.togroup("6")
    elif window.name == "VITE Server":
        window.togroup("6")

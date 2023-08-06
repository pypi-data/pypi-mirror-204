import uvicore
from ohmyi3 import util
from uvicore.typing import Dict
from uvicore.configuration import env
from uvicore.support.dumper import dump, dd
from ohmyi3.util import Overridable, gather, path, plugin

# Settings and hooks for ohmyi3 i3ctl config generator.
# Configs as python gives unlimited flexibility and programability.
# All of these self.* variables are accessible as jinja2 variables
# to dynamically control your i3 configs and anything else that
# requires automation (see the plugins)

def config():
    """Ohmyi3 variables for configuring and templating i3"""

    # Hostname and user from system
    host = util.hostname()
    user = util.loggedinuser()

    # Refresh overridables with all local variables thus far
    set = Overridable(**locals())

    # Paths to all relevant locations
    # If you need to change the ohmyi3 path, use the
    # environment variable OHMYI3_PATH (default ~/.config/ohmyi3)
    ohmyi3_path = uvicore.config('ohmyi3.config_path')
    paths = set({
        'ohmyi3': path(ohmyi3_path),
        'ohmyi3_configd': path([ohmyi3_path, 'config.d']),
        'ohmyi3_themes': path([ohmyi3_path, 'themes']),
        'i3': path('~/.config/i3'),
        'i3status': path('~/.config/i3status'),
        'alacritty': path('~/.config/alacritty'),
        'polybar': path('~/.config/polybar'),
    })

    # OS variant
    os = set('manjaro', if_host={
        'p14s': 'lmde'
    })

    # Main network interface
    net_interface = set('enp11s0', if_host={
        'p15': 'enp11s0',
        'p53': 'wlp0s20f3',
        'deajaro': 'wlp2s0',
    })

    # Has battery (laptop?)
    has_battery = set(True, if_host={
        'sunjaro': False,
        'p53': True,
        'p15': True,
        'p14s': True,
    })
    battery_device = set('BAT0')

    # Backlinght
    backlight_device = set('intel_backlight')

    # Desktop Environment (kde, xfce, i3, cinnamon, mate, gnome)
    # I like to run i3 inside kde and xfce etc...  If runing under these DE's
    # I need to tweak the configs (no screen lock, different autostarts etc...)
    desktop = set('i3', if_host={
        'sunjaro': 'kde',
        'p53': 'i3',
        'p15': 'i3',
        #'p14s': 'cinnamon',
    })

    # Main desktop tools (kde, xfce...)
    # Not the same as desktop, which is the running Desktop Environment
    desktop_tools = set('kde', if_host={
        'deajaro': 'xfce'
    })

    # Using i3 capable of gaps
    i3_gaps = set(True, if_host={
        'p14s': False
    })

    # Restart i3 command
    i3_restart = set('~/.files/scripts/i3ctl-dev generate && i3-msg restart', if_host={
        'deajaro': 'i3ctl generate && i3-msg restart',
    })

    # Wallpaper base
    wallpaper_base = set('~/Wallpaper', if_host={
        'sunjaro': '~/Pictures/Wallpaper',
        'p53': '~/Pictures/Wallpaper',
    })

    # Current theme (amber, archlinux, manjaro, pink)
    theme = set('manjaro', if_host={
        'sunjaro': 'manjaro',
        'p53': 'manjaro',
        'p15': 'pink',
        'p14s': 'manjaro',
    })

    # Refresh overridables with all local variables thus far
    set = Overridable(**locals())

    # Extra theme details
    # Wallpaper is an OVERRIDE, else defaults to the themes folder/background.[jpg|png]
    themes = set({
        'amber': {
            #'wallpaper': 'Abstract/cracked_orange.jpg',
            #'wallpaper': 'Manjaro/antelope-canyon-984055.jpg',
            #'wallpaper': 'Scenes/digital_sunset.jpg',
            #'wallpaper': 'LinuxMint/linuxmint-vera/mpiwnicki_red_dusk.jpg',
            #'wallpaper': 'LinuxMint/linuxmint-vanessa/navi_india.jpg',
            'wallpaper': 'LinuxMint/linuxmint-una/nwatson_eclipse.jpg',
            #'wallpaper': 'LinuxMint/linuxmint-vera/navi_india.jpg',
            #'wallpaper': 'LinuxMint/linuxmint-ulyssa/tangerine_nanpu.jpg',
            #'wallpaper': 'Manjaro/sky-3189347.jpg',
            'archey3': 'yellow',
        },
        'archlinux': {
            #'wallpaper': 'Archlinux/349880.jpg',
            'archey3': 'blue',
            'wallpaper': 'De/budgie.jpg',
        },
        'manjaro': {
            #'wallpaper': 'Manjaro/illyria-default-lockscreen-nobrand.jpg',
            #'wallpaper': 'Manjaro/wpM_orbit2_textured.jpg'
            'wallpaper': 'De/deepin.jpg',
            'archey3': 'green',
        },
        'pink': {
            #'wallpaper': 'Abstract/artistic_colors2.jpg',
            #'wallpaper': 'Landscape/backlit-chiemsee-dawn-1363876.jpg',
            #`'wallpaper': 'Manjaro/DigitalMilkyway.png',
            #'wallpaper': 'LinuxMint/linuxmint-una/eeselioglu_istanbul.jpg',
            #'wallpaper': 'Abstract/neon_huawei.jpg',
            'wallpaper': 'De/budgie.jpg',
            'archey3': 'magenta',
        },
    },
        if_host={
            #'p15': {'manjaro.wallpaper': 'Manjaro/wpM_orbit2_textured.jpg'}
            'p15': {'manjaro.wallpaper': 'De/deepin.jpg'}
        }
    )

    # Polybar
    # Specific to the custom qpanel theme made from this https://github.com/adi1090x/polybar-themes
    polybar = set({
        'enabled': True,
        # blocks|colorblocks|cuts|docky|forest|grayblocks|hack|material
        # panels|pwidgets|qpanels|shades|shapes
        'theme': 'qpanels',
        # budgie|deepin|elight|edark|gnomw|klight|kdark
        # liri|mint|ugnome|unity|xubuntu|zorin
        'subtheme': 'deepin'
    }, if_host={
        'p14s': {'polybar.enabled': False},
    })

    # Rofi
    rofi = set({
        'launcher': f'~/.config/polybar/{polybar.theme}/scripts/launcher.sh --{polybar.subtheme}',
        'powermenu': f'~/.config/polybar/{polybar.theme}/scripts/powermenu.sh --{polybar.subtheme}',
    },
        if_host={
            'p14s': {'launcher': 'rofi -show drun'}
        }
    )

    # Alacritty
    alacritty = set({
        'font_size': '10.0',
    }, if_host={
        'p15': {'font_size': '8.0'}
    })

    # Default font for window titles (not bar.font)
    font = set('xft:URWGothic-Book 9')

    # i3bar configs
    # All themes may obey these global bar configs, or they may set their own
    bar = set({
        'enabled': False,
        #'cmd': 'i3bar',
        'cmd': 'i3bar --transparency',
        'status_cmd': 'i3status',
        'position': 'bottom',
        'font': 'xft:URWGothic-Book 8',

        # Hide or show the bar
        'mode': 'dock', # dock|hide|invisible
        'hidden_state': 'hide', # hide|show

        # Modifier makes the hidden bar show up while key is pressed
        'modifier': 'none',
        #'modifier': 'Ctrl+$alt',
    },
        # FIXME, make an ifnot_desktop == i3
        if_desktop={
            'kde': {'mode': 'hide'}
        },
        if_hostname={
            'p15': {'position': 'top'},
            'p14s': {'enabled': True},
        },
    )

    # Preferred applications, could change depending on DE installed
    apps = set({
        'terminal': 'alacritty',
        'filemanager': 'dolphin',
        'webbrowser': 'firefox',
        'webbrowser2': 'chromium',
        'calculator': 'kcalc',
        'settings': 'systemsettings',
        'screenshot': 'spectacle', # i3-scrot
        'dmenu': path('~/.files/scripts/dmenu-run-blue'),
        'screenlock': 'blurlock',
        'powermanager': 'xfce4-power-manager',
        'powermanagersettings': 'xfce4-power-manager-settings',
        'xsslock': f'xss-lock -- blurlock',
        #'xsslock': f'xss-lock -- i3lock --nofork --image {wallpaper_base}/De/deepin.jpg',
        'networkeditor': 'nm-connection-editor',
        'htop': 'htop',
        'bashtop': 'bashtop',
        'taskmanager': 'ksysguard',
        'codeeditor': 'code',
        'notepad': 'kate',
        'colorpicker': 'kcolorchooser',
        'spotify': 'spotify',
        'clipboard': 'clipit --daemon',
    },
        if_theme={
            'manjaro': {'dmenu': path('~/.files/scripts/dmenu-run-green')}
        },
        if_host={
            'p14s': {
                'terminal': 'gnome-terminal',
                'calculator': 'gnome-calculator',
                'screenlock': 'i3lock',
            },
            'deajaro': {
                'filemanager': 'thunar',
                'calculator': 'xcalc',
                'taskmanager': 'xfce4-taskmanager',
                'settings': 'xfce4-settings-manager',
            },
        },
    )

    # Tray Icons
    tray = set({
        'volume': 'volumeicon',
        'network': 'nm-applet',
    })

    # Volume Control
    volume = set({
        'up': 'amixer -D pulse sset Master 5%+',
        'down': 'amixer -D pulse sset Master 5%-',
        'mute': 'amixer -D pulse set Master 1+ toggle',
        # Or self.terminal + '-e alsamixer'
        'mixer': 'pavucontrol'
    })

    # Media Control
    media = set({
        'play_pause': 'playerctl play-pause',
        'next': 'playerctl next',
        'previous': 'playerctl previous',
    })

    # Brightness Control
    brightness = set({
        'up': 'brightnessctl -q set 3%+',
        'down': 'brightnessctl --min-val=2 -q set 3%-',
    })

    # Dynamically Load and Instantiate Plugins
    # Pluging must be LAST after all variables are set
    _vars = gather(locals())
    plugins = set({
        'nitrogen': plugin('nitrogen.Nitrogen')(_vars),
        'archey3': plugin('archey3.Archey3')(_vars),
        'polybar': plugin('polybar.Polybar')(_vars),
        'alacritty': plugin('alacritty.Alacritty')(_vars),
    })

    # Return all variables to the ohmyi3 generator for templating
    return gather(locals())



async def before_generate(config):
    """This hook fires before the new i3 config is generated"""
    #dump('before hook')

async def after_generate(config):
    """This hook fires after the new i3 config is generated"""
    #dump('after hook')

    # Set themed wallpaper
    config.plugins.nitrogen.set_wallpaper()

    # Set themed archey in my .zshrc and or .bashrc
    config.plugins.archey3.set_archey()

    # Modify polybar theme files (template some variables)
    config.plugins.polybar.adjust_polybar()

    # Template the alacritty config
    config.plugins.alacritty.template_config()

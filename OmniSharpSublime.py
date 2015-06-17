import sys
import sublime
import os
import stat

from .listeners import *
from .commands import *

if sys.version_info < (3, 3):
    raise RuntimeError('OmniSharpSublime works with Sublime Text 3 only')

def plugin_loaded():
    print('omnisharp plugin_loaded')
    settings = sublime.load_settings('OmniSharpSublime.sublime-settings')
    configpath = settings.get("omnisharp_server_config_location")
    if not configpath:
        settings.set("omnisharp_server_config_location", "")
        sublime.save_settings('OmniSharpSublime.sublime-settings')

    if os.name == 'posix':
        # give the launch script executable permissions
        script_path = os.path.dirname(__file__) + '/omnisharp-roslyn/scripts/Omnisharp'
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | 0o111)

def plugin_unloaded():
    from package_control import events

    if events.pre_upgrade('OmniSharp'):
        print('About to upgrade OmniSharp')
        if os.name != 'posix':
            # kill the exe before the update complains about exe in use
            # os.system('taskkill /f /im omnisharp-roslyn/OmniSharp.exe')
            pass

    print('omnisharp plugin_unloaded')

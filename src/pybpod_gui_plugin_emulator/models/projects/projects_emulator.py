from AnyQt.QtGui import QIcon
from confapp import conf
from pybpod_gui_plugin_emulator import EmulatorGUI


class ProjectsEmulator(object):

    def register_on_main_menu(self, mainmenu):
        super(ProjectsEmulator, self).register_on_main_menu(mainmenu)

        if len([m for m in mainmenu if 'Tools' in m.keys()]) == 0:
            mainmenu.append({'Tools': []})

        menu_index = 0
        for i, m in enumerate(mainmenu):
            if 'Tools' in m.keys():
                menu_index = i
                break

        mainmenu[menu_index]['Tools'].append('-')
        mainmenu[menu_index]['Tools'].append(
            {'Emulator': self.open_emulator_plugin, 'icon': QIcon(conf.EMULATOR_PLUGIN_ICON)})

    def open_emulator_plugin(self):
        if not hasattr(self, 'emulator_plugin'):
            self.emulator_plugin = EmulatorGUI(self, projects=self.projects)
            self.emulator_plugin.show()
            self.emulator_plugin.resize(*conf.EMULATOR_PLUGIN_WINDOW_SIZE)
        else:
            self.emulator_plugin.show()

        return self.emulator_plugin

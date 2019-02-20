from pybpod_gui_plugin_emulator import EmulatorGUI
from pybpodgui_plugin.models.setup.setup_dockwindow import SetupDockWindow
from pyforms_gui.controls.control_button import ControlButton
from confapp import conf


class SetupWindowEmulator(SetupDockWindow):

    def __init__(self, experiment=None):
        super(SetupWindowEmulator, self).__init__(experiment)

        self._emulator = ControlButton('Test with emulator',
                                       default=self.__emulator_btn_evt,
                                       icon=conf.EMULATOR_LAUNCH_ICON)

        self._formset = [
            '_name',
            '_board',
            '_task',
            ('_detached', '_run_task_btn'),
            '_emulator',
            ('_stoptrial_btn', '_pause_btn'),
            '=',
            {
                'Subjects': [
                    # '_allsubjects',
                    '',
                    '_add_subject',
                    '_subjects_list',
                ],
                'Variables': [
                    '_varspanel',
                ],
            }
        ]

    def __emulator_btn_evt(self):
        if not hasattr(self, 'emulator_plugin'):
            self.emulator_plugin = EmulatorGUI(self)
            self.emulator_plugin.show()
            self.emulator_plugin.resize(*conf.EMULATOR_PLUGIN_WINDOW_SIZE)
        else:
            self.emulator_plugin.show()

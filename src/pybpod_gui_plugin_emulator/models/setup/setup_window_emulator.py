from pybpod_gui_plugin_emulator import EmulatorGUI
from pybpodgui_plugin.models.setup.setup_dockwindow import SetupDockWindow
from pyforms_gui.controls.control_button import ControlButton
from confapp import conf


class SetupWindowEmulator(SetupDockWindow):

    def __init__(self, experiment=None):
        super(SetupWindowEmulator, self).__init__(experiment)

        self._emulator = ControlButton('Test with emulator',
                                       default=self.__emulator_btn_evt,
                                       icon=conf.EMULATOR_LAUNCH_ICON,
                                       enabled=False)

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

    def show(self):
        super().show()
        if self._board.value and self._task.value:
            self._emulator.enabled = True

    def _task_changed_evt(self):
        if hasattr(self, '_emulator'):
            self._emulator.enabled = (self._task.value is not 0 and self._board.value is not 0)
        super()._task_changed_evt()

    def _board_changed_evt(self):
        if hasattr(self, '_emulator'):
            self._emulator.enabled = (self._board.value is not 0 and self._task.value is not 0)
        super()._board_changed_evt()

    def __emulator_btn_evt(self):
        if not hasattr(self, 'emulator_plugin'):
            self.emulator_plugin = EmulatorGUI(self)
            self.emulator_plugin.show()
            self.emulator_plugin.resize(*conf.EMULATOR_PLUGIN_WINDOW_SIZE)
        else:
            self.emulator_plugin.show()

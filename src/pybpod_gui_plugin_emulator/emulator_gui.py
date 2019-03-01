import io

import pyforms
from pybpodapi.com.arcom import ArduinoTypes
from pybpodapi.com.protocol.send_msg_headers import SendMessageHeader
from pybpodgui_api.exceptions.run_setup import RunSetupError
from pybpodgui_plugin.utils import make_lambda_func
from pyforms.basewidget import BaseWidget
from pyforms_gui.controls.control_button import ControlButton
from confapp import conf
from pyforms_gui.controls.control_label import ControlLabel


class EmulatorGUI(BaseWidget):

    def __init__(self, parent_win=None):
        self.setup = parent_win
        title = 'Emulator for setup: ' + self.setup.name

        BaseWidget.__init__(self, title, parent_win=parent_win)

        self.CHECKED_ICON = conf.EMULATOR_CHECKED_ICON
        self.UNCHECKED_ICON = conf.EMULATOR_UNCHECKED_ICON

        self._currentSetup = ControlLabel(self.setup.name)
        self._selectedBoard = ControlLabel(self.setup.board.name)
        self._selectedProtocol = ControlLabel(self.setup.task.name)

        self._run_task_btn = ControlButton('Run protocol',
                                           default=self.__run_protocol_btn_evt,
                                           checkable=True)

        self._valve_buttons = []
        self._valve_label = ControlLabel("Valve")
        self._led_buttons = []
        self._led_label = ControlLabel("LED")
        self._poke_buttons = []
        self._poke_label = ControlLabel("Poke")

        for n in range(1, 9):
            btn_valve = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)
            btn_led = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)
            btn_poke = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)

            btn_valve.value = make_lambda_func(self.__button_on_click_evt, btn=btn_valve)
            btn_led.value = make_lambda_func(self.__button_on_click_evt, btn=btn_led)
            btn_poke.value = make_lambda_func(self.__button_on_click_evt, btn=btn_poke)

            setattr(self, f'_btn_valve{n}', btn_valve)
            setattr(self, f'_btn_led{n}', btn_led)
            setattr(self, f'_btn_poke{n}', btn_poke)
            self._valve_buttons.append(btn_valve)
            self._led_buttons.append(btn_led)
            self._poke_buttons.append(btn_poke)

        self._bnc_in_buttons = []
        self._bnc_in_label = ControlLabel("BNC In")
        self._bnc_out_buttons = []
        self._bnc_out_label = ControlLabel("BNC Out")

        for n in range(1, 3):
            btn_bnc_in = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)
            btn_bnc_out = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)

            btn_bnc_in.value = make_lambda_func(self.__button_on_click_evt, btn=btn_bnc_in)
            btn_bnc_out.value = make_lambda_func(self.__button_on_click_evt, btn=btn_bnc_out)

            setattr(self, f'_btn_bnc_in{n}', btn_bnc_in)
            setattr(self, f'_btn_bnc_out{n}', btn_bnc_out)
            self._bnc_in_buttons.append(btn_bnc_in)
            self._bnc_out_buttons.append(btn_bnc_out)

        self._wire_in_buttons = []
        self._wire_in_label = ControlLabel("Wire In")
        self._wire_out_buttons = []
        self._wire_out_label = ControlLabel("Wire Out")

        for n in range(1, 5):
            btn_wire_in = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)
            btn_wire_out = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)

            btn_wire_in.value = make_lambda_func(self.__button_on_click_evt, btn=btn_wire_in)
            btn_wire_out.value = make_lambda_func(self.__button_on_click_evt, btn=btn_wire_out)

            setattr(self, f'_btn_wire_in{n}', btn_wire_in)
            setattr(self, f'_btn_wire_out{n}', btn_wire_out)
            self._wire_in_buttons.append(btn_wire_in)
            self._wire_out_buttons.append(btn_wire_out)

        self.formset = [
            ('h5:Current setup:',
             '_currentSetup',
             'h5:Selected board:',
             '_selectedBoard',
             'h5:Selected protocol:',
             '_selectedProtocol',
             '_run_task_btn'),
            '',
            'h5:Behaviour Ports',
            ('_valve_label', tuple([f'_btn_valve{n.label}' for n in self._valve_buttons])),
            ('_led_label', tuple([f'_btn_led{n.label}' for n in self._led_buttons])),
            ('_poke_label', tuple([f'_btn_poke{n.label}' for n in self._poke_buttons])),
            'h5:BNC',
            ('_bnc_in_label',
             tuple([f'_btn_bnc_in{n.label}' for n in self._bnc_in_buttons]),
             '_bnc_out_label',
             tuple([f'_btn_bnc_out{n.label}' for n in self._bnc_out_buttons])
             ),
            'h5:Wire',
            ('_wire_in_label',
             tuple([f'_btn_wire_in{n.label}' for n in self._wire_in_buttons]),
             '_wire_out_label',
             tuple([f'_btn_wire_out{n.label}' for n in self._wire_out_buttons])
             ),
            ' '
        ]

        self.set_margin(10)

    def __button_on_click_evt(self, btn=None):
        if btn is None:
            return

        if btn.checked:
            btn.icon = self.CHECKED_ICON

            #print("Preparing and sending message through stdin directly into the board.proc")

            # TODO: prepare message and write to stdin
            #message = ArduinoTypes.get_uint8_array([ord('V'), 5, 2])
            message = b'trigger_input:B:1:255\n'

            self.setup.board.proc.stdin.write(message)
            self.setup.board.proc.stdin.flush()

        else:
            btn.icon = self.UNCHECKED_ICON

    def __run_protocol_btn_evt(self):
        try:
            if self.setup.status == self.setup.STATUS_RUNNING_TASK:
                self.setup.stop_task()
            elif self.setup.status == self.setup.STATUS_READY:
                self.setup.run_task()
        except RunSetupError as err:
            self.warning(str(err), "Warning")
        except Exception as err:
            self.alert(str(err), "Unexpected Error")
        pass


if __name__ == '__main__':
    pyforms.start_app(EmulatorGUI, geometry=(0, 0, 300, 300))

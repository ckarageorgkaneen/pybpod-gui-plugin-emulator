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
from pyforms_gui.controls.control_text import ControlText


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
        self._stop_trial_btn = ControlButton('Stop trial',
                                           default=self.__stop_trial_btn_evt,
                                           enabled=False)
        self._pause_btn = ControlButton('Pause',
                                           default=self.__pause_btn_evt,
                                           enabled=False)

        self._valve_buttons = []
        self._valve_label = ControlLabel("Valve")
        self._led_buttons = []
        self._led_label = ControlLabel("LED")
        self._poke_buttons = []
        self._poke_label = ControlLabel("Poke")

        for n in range(1, 5):
            btn_valve = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)
            btn_led = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)
            btn_poke = ControlButton(str(n), icon=self.UNCHECKED_ICON, checkable=True)

            btn_valve.value = make_lambda_func(self.__button_on_click_evt, btn=btn_valve)
            btn_led.value = make_lambda_func(self.__button_on_click_evt, btn=btn_led)
            btn_poke.value = make_lambda_func(self.__button_on_click_evt, btn=btn_poke)

            setattr(self, f'_btn_Valve{n}', btn_valve)
            setattr(self, f'_btn_PWM{n}', btn_led)
            setattr(self, f'_btn_Port{n}', btn_poke)
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

            setattr(self, f'_btn_BNC_in{n}', btn_bnc_in)
            setattr(self, f'_btn_BNC_out{n}', btn_bnc_out)
            self._bnc_in_buttons.append(btn_bnc_in)
            self._bnc_out_buttons.append(btn_bnc_out)

        self._send_msg_buttons = []
        self._control_text_bytes_msg = []
        for n in range(1, 6):
            module_label = ControlLabel(f'Module {n}')
            control_text_bytes_msg = ControlText()

            btn_send_msg_module = ControlButton(f'Send bytes')
            btn_send_msg_module.value = make_lambda_func(self.__send_msg_btn_evt, btn=btn_send_msg_module, control_text=control_text_bytes_msg)

            setattr(self, f'_module_label{n}', module_label)
            setattr(self, f'_control_text_bytes_msg{n}', control_text_bytes_msg)
            setattr(self, f'_btn_send_msg_module{n}', btn_send_msg_module)
            self._send_msg_buttons.append(btn_send_msg_module)
            self._control_text_bytes_msg.append(control_text_bytes_msg)

        self.formset = [
            ([('h5:Current setup:', '_currentSetup'),
              ('h5:Selected board:', '_selectedBoard'),
              ('h5:Selected protocol:', '_selectedProtocol')],
             '',
             ['_run_task_btn', '_stop_trial_btn', '_pause_btn']),
            '',
            'h5:Behaviour Ports',
            ('_valve_label', tuple([f'_btn_Valve{n.label}' for n in self._valve_buttons])),
            ('_led_label', tuple([f'_btn_PWM{n.label}' for n in self._led_buttons])),
            ('_poke_label', tuple([f'_btn_Port{n.label}' for n in self._poke_buttons])),
            'h5:BNC',
            ('_bnc_in_label',
             tuple([f'_btn_BNC_in{n.label}' for n in self._bnc_in_buttons]),
             '_bnc_out_label',
             tuple([f'_btn_BNC_out{n.label}' for n in self._bnc_out_buttons])
             ),
            '',
            'h5: Send bytes to modules',
            [(f'_module_label{idx+1}', f'_control_text_bytes_msg{idx+1}', f'_btn_send_msg_module{idx+1}') for idx, n in enumerate(self._send_msg_buttons)]
        ]

        self.set_margin(10)

    def __send_msg_btn_evt(self, btn=None, control_text=None):
        # get message from textbox
        if btn is None or control_text is None:
            return
        module_index = btn.name[-1]
        message = f"message:{module_index}:{control_text.value}"

        # send msg through stdin to bpod (we need to create a command first in the other side)
        self.setup.board.proc.stdin.write(message.encode('utf-8'))
        self.setup.board.proc.stdin.flush()

    def __button_on_click_evt(self, btn=None):
        if btn is None:
            return

        if self.setup.status is not self.setup.STATUS_RUNNING_TASK:
            return

        name = btn.name.split('_')
        port_name = name[2]
        is_pwm = port_name.startswith('PWM')
        is_valve = port_name.startswith('Valve')
        is_output = is_pwm or is_valve
        if len(name) > 3:
            port_number = name[3][-1]
            is_output = name[3].startswith('out')
        else:
            port_number = ''

        if btn.checked:
            val = 1
            if is_pwm:
                val = 255
            btn.icon = self.CHECKED_ICON
        else:
            val = 0
            btn.icon = self.UNCHECKED_ICON

        if is_output:
            message = f'trigger_output:{port_name}{port_number}:{val}'
        else:
            message = f'trigger_input:{port_name}{port_number}:{val}'

        self.setup.board.proc.stdin.write(message.encode('utf-8'))
        self.setup.board.proc.stdin.flush()

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

    def __stop_trial_btn_evt(self):
        setup = self.setup
        if setup:
            setup._stop_trial_evt()
        else:
            self.critical("There isn't any setup selected. Please select one before continuing.", "No setup selected")

    def __pause_btn_evt(self):
        setup = self.setup
        if setup:
            setup._pause_evt()


if __name__ == '__main__':
    pyforms.start_app(EmulatorGUI, geometry=(0, 0, 300, 300))

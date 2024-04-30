import logging
from AnyQt import QtCore
from AnyQt import QtNetwork
from PyQt5 import sip
from .emulator_gui_server import EmulatorGUIServer
from .emulator_gui_server_error import EmulatorGUIServerError

logger = logging.getLogger(__name__)


class EmulatorGUIClient():

    _SOCKET_WAIT_FOR_CONNECTED_TIMEOUT = 500

    def __init__(self):
        self._socket = None

    @property
    def socket(self):
        if self._socket is None or sip.isdeleted(self._socket):
            self._socket = QtNetwork.QLocalSocket()
        return self._socket

    def send(self, output_channel_name, output_value):
        self.socket.connectToServer(
            EmulatorGUIServer.NAME,
            QtCore.QIODevice.WriteOnly)
        if self.socket.waitForConnected(
                self._SOCKET_WAIT_FOR_CONNECTED_TIMEOUT):
            message = f'{output_channel_name}:{output_value}'
            self.socket.write(message.encode('utf-8'))
            if not self.socket.waitForBytesWritten(2000):
                error_message = \
                    f'Could not connect to server: {self.socket.errorString()}'
                logger.error(error_message)
                raise EmulatorGUIServerError(error_message)
            self.socket.disconnectFromServer()
        elif self.socket.error() != \
                QtNetwork.QAbstractSocket.HostNotFoundError:
            error_message = \
                f'Could not connect to server: {self.socket.errorString()}'
            logger.error(error_message)
            raise EmulatorGUIServerError(error_message)
        else:
            logger.error('Emulator gui plugin server is down.')

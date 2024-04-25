import logging
from AnyQt import QtCore
from AnyQt import QtNetwork
from .emulator_gui_server_error import EmulatorGUIServerError

logger = logging.getLogger(__name__)


class EmulatorGUIServer(QtNetwork.QLocalServer):

    signal_data_received = QtCore.pyqtSignal(object)
    NAME = 'gui_plugin_emulator_server'
    _SOCKET_TIMEOUT = 2000

    def __init__(self):
        super().__init__()
        self.setSocketOptions(QtNetwork.QLocalServer.WorldAccessOption)
        self.newConnection.connect(self._handleConnection)

    def listen(self):
        if not super().listen(self.NAME):
            raise EmulatorGUIServerError(
                f'Could not start server: {self.NAME}')

    def close(self):
        super().close()
        self.removeServer(self.fullServerName())

    def _handleConnection(self):
        socket = self.nextPendingConnection()
        if socket is not None:
            data = None
            if socket.waitForReadyRead(self._SOCKET_TIMEOUT):
                data = socket.readAll().data().decode('utf-8')
                logger.debug(f'Read data from emulator: {data}')
                socket.disconnectFromServer()
            socket.deleteLater()
            if data is not None:
                self.signal_data_received.emit(data)
                logger.debug('Data emitted.')

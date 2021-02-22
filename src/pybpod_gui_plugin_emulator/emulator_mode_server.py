import logging
from AnyQt import QtCore
from AnyQt import QtNetwork
from pybpodapi.bpod.emulator import Emulator

logger = logging.getLogger(__name__)


class EmulatorModeServer(QtNetwork.QLocalServer):
    signal_data_received = QtCore.pyqtSignal(object)

    _SOCKET_TIMEOUT = 2000

    def __init__(self):
        super().__init__()
        self.setSocketOptions(QtNetwork.QLocalServer.WorldAccessOption)
        self.newConnection.connect(self._handleConnection)

    def listen(self):
        if not super().listen(Emulator.GUI_PLUGIN_SERVER_NAME):
            raise RuntimeError(
                f'Could not start server: {Emulator.GUI_PLUGIN_SERVER_NAME}')

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

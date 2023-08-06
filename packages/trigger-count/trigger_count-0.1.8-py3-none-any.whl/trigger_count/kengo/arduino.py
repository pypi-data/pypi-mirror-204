"""Serial connection to arduino to interact with Kengo's setup."""
import time

import serial


BAUDRATE = 9600
PORT = "/dev/ttyACM0"
TRIAL_START_COMMAND = "D"
STIM_START_COMMAND = "B"
STIM_END_COMMAND = "X"
TRIAL_END_COMMAND = "T"


class KengoArduino:
    """Class that implements serial connection to arduino."""
    def __init__(self, port: str = PORT, baudrate: int = BAUDRATE) -> None:
        self._serial = serial.Serial(
            baudrate=BAUDRATE,
            port=port,
        )
        time.sleep(1)

    def send_trial_start(self) -> None:
        """Send trigger for trial start."""
        self._serial.write(TRIAL_START_COMMAND.encode())

    def send_stim_start(self) -> None:
        self._serial.write(STIM_START_COMMAND.encode())

    def send_stim_end(self) -> None:
        self._serial.write(STIM_END_COMMAND.encode())

    def send_trial_end(self) -> None:
        self._serial.write(TRIAL_END_COMMAND.encode())

    def close(self) -> None:
        self._serial.close()
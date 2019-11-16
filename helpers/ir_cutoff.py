# -*- code utf-8 -*-
from time import sleep

from gpio.ir_cutoff_motor import IRCutOffMotor
from helpers import Singleton
from helpers.config import config, logger
from helpers.sundial import Sundial


class IRCutOff(metaclass=Singleton):
    """
    Turns IR Cut-Off filter on/off depending time of the day
    """
    def __init__(self):
        # ToDo it seems to work without enable PIN. test it.
        self.__ir_cutoff_motor = IRCutOffMotor(
            forward=config.get('IR_CUTOFF_FORWARD_GPIO_BCM'),
            backward=config.get('IR_CUTOFF_BACKWARD_GPIO_BCM'),
            enable=config.get('IR_CUTOFF_ENABLER_GPIO_BCM'))

    def __del__(self):
        if self.__ir_cutoff_motor:
            self.__ir_cutoff_motor.close()

    def toggle(self, mode):
        """
        This method is separated in 2 other methods to be able to
        run unit tests on `_toggle` and get PIN states before `.stop()`
        is called.
        :param mode: str. Sundial.DAY|Sundial.NIGHT
        """
        self._toggle(mode)
        self.stop()

    def stop(self):
        """
        Turns off the motor.
        We do not need to keep a GPIO on high state because IR Cut-Off filter
        only need current for a small period of time to be activated in one
        direction or the other
        """
        sleep(0.5)  # Leave some time to motor to toggle IR Cut-Off filter
        self.__ir_cutoff_motor.stop()

    def _toggle(self, mode):
        if mode == Sundial.DAY:
            logger.warning('Day mode: Turn IR cut-off filter ON')
            self.__ir_cutoff_motor.backward()
        else:
            logger.warning('Night mode: Turn IR cut-off filter OFF')
            self.__ir_cutoff_motor.forward()

import logging

from ios_device.util.lockdown import LockdownClient
from ios_device.util.usbmux import USBMux


class Wireless:

    def __init__(self, lockdown=None, udid=None, network=True,logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.lockdown = lockdown or LockdownClient(udid=udid,network=network)

    def start_wireless(self):
        data = self.lockdown.get_value('com.apple.mobile.wireless_lockdown')
        # print(data)
        # data = self.lockdown.get_value('com.apple.xcode.developerdomain')
        # # print(data)
        print(USBMux().get_devices(network=True))


        # print(self.lockdown.enable_wireless())
        # pass


Wireless().start_wireless()
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Copyright (C) 2016 Gary Chen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
### BEGIN NODE INFO
[info]
name = Lakeshore 340 Temperature Monitor
version = 1.0
description =

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""

from labrad.server import setting
from labrad.gpib import GPIBManagedServer, GPIBDeviceWrapper
from twisted.internet.defer import inlineCallbacks, returnValue

class LakeshoreWrapper(GPIBDeviceWrapper):

    @inlineCallbacks
    def get_temperature_reading(self, channel='A'):
        '''
        
        '''
        command = "KRDG? " + channel
        yield self.write(command)
        
        output = yield self.read()
        returnValue(output)

    def initialize(self):
        '''
        Provides a lookup table for waveform to GPIB lingo
        '''
        #self.lookup = {'sine':'SIN', 'square':'SQU', 'ramp':'RAMP', 'pulse':'PULS', 'noise':'NOIS', 'DC' : 'DC', 'USER':'USER'}


class LakeshoreServer(GPIBManagedServer):
    name = 'Lakeshore 340 Server' # Server name
    deviceName = 'Lakeshore 340' # Model string returned from *IDN?
    deviceWrapper = LakeshoreWrapper

    @setting(0, 'get_temperature_reading', channel = 's', output = 'v')
    def get_temperature_reading(self, c, channel='A'):
        dev = self.selectedDevice(c)
        yield dev.get_temperature_reading(channel)


__server__ = LakeshoreServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)

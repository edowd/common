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

<<<<<<< HEAD
def parse(val):
    """
    Parse function to account for the occasional GPIB glitches where we get extra characters in front of the numbers.
    """
    if len(val):
        try:
            return float(val)
        except ValueError:
            return parse(val[1:])
    else:
        return 0.0

=======
>>>>>>> parent of a681ec7... First working version
class LakeshoreWrapper(GPIBDeviceWrapper):

    @inlineCallbacks
    def temperature(self, channel='A'):
        """
        
        """
        command = "KRDG? " + channel
        yield self.write(command)
        
        output = yield self.read()
        returnValue(output)

<<<<<<< HEAD
=======
    def initialize(self):
        '''
        Provides a lookup table for waveform to GPIB lingo
        '''
        #self.lookup = {'sine':'SIN', 'square':'SQU', 'ramp':'RAMP', 'pulse':'PULS', 'noise':'NOIS', 'DC' : 'DC', 'USER':'USER'}


class LakeshoreServer(GPIBManagedServer):
    name = 'Lakeshore 340 Server' # Server name
    deviceName = 'Lakeshore 340' # Model string returned from *IDN?
    deviceWrapper = LakeshoreWrapper

    @setting(10, channel=['s'], returns=['*v[K]'])
    def temperature(self, c, channel='A'):
        dev = self.selectedDevice(c)
        val = yield dev.get_temperature_reading(channel)
        returnValue(val)

    @setting(11, channel=['s'], returns=['*v[K]'])
    def temperature_list(self, c, channel='A'):
        """
        Read channel temperatures.

        Returns a ValueList of the channel temperatures in Kelvin.
        """
        dev = self.selectedDevice(c)
        resp = yield dev.query('KRDG? ' + channel)
        vals = [parse(val) * _u.K for val in resp.split(',')]
        returnValue(vals)
=======
    @setting(0, 'get_temperature_reading', channel = 's', output = 'v')
    def get_temperature_reading(self, c, channel='A'):
        dev = self.selectedDevice(c)
        yield dev.get_temperature_reading(channel)

    @setting(12, channel=['s'], returns=['*v[V]'])
    def voltage_list(self, c, channel='A'):
        """
        Read channel voltages.

        Returns a ValueList of the channel voltages in Volts.
        """
        dev = self.selectedDevice(c)
        resp = yield dev.query('SRDG? ' + channel)
        vals = [parse(val) * _u.V for val in resp.split(',')]
        returnValue(vals)
        
__server__ = LakeshoreServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)

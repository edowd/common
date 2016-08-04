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
name = Lakeshore 340
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
import labrad.units as _u
from labrad.gpib import GPIBManagedServer, GPIBDeviceWrapper
from twisted.internet.defer import inlineCallbacks, returnValue

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

class LakeshoreWrapper(GPIBDeviceWrapper):

    @inlineCallbacks
    def get_temperature_reading(self, channel='A'):
        '''
        
        '''
        command = "KRDG? " + channel
        yield self.write(command)
        
        output = yield self.read()
        returnValue(output)

class LakeshoreServer(GPIBManagedServer):
    name = 'Lakeshore 340' # Server name
    deviceName = 'LSCI MODEL340' # Model string returned from *IDN?
    deviceWrapper = LakeshoreWrapper

    @setting(10, 'Temperatures', returns=['*v[K]'])
    def temperatures(self, c):
        """Read channel temperatures.

        Returns a ValueList of the channel temperatures in Kelvin.
        """
        dev = self.selectedDevice(c)
        resp = yield dev.query('KRDG? 0')
        vals = [parse(val) * _u.K for val in resp.split(',')]
        returnValue(vals)

    @setting(11, 'Voltages', returns=['*v[V]'])
    def voltages(self, c):
        """Read channel voltages.

        Returns a ValueList of the channel voltages in Volts.
        """
        dev = self.selectedDevice(c)
        resp = yield dev.query('SRDG? 0')
        vals = [parse(val) * _u.V for val in resp.split(',')]
        returnValue(vals)
__server__ = LakeshoreServer()

if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)

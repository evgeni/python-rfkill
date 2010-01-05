#!/usr/bin/env python
#
#       rfkill.py
#       
#   Copyright 2010 Evgeni Golov <evgeni@debian.org>
#   
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions
#   are met:
#   
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the  nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#   
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import dbus

class RFKillSwitch:

    def __init__ (self, dev):
        self.dev = dev
        self.interface = dbus.Interface(self.dev, 'org.freedesktop.Hal.Device')
        self.switch = dbus.Interface(self.dev, 'org.freedesktop.Hal.Device.KillSwitch')

    def get_name (self):
        return str(self.interface.GetProperty ('killswitch.name'))

    def get_state (self):
        return int(self.interface.GetProperty ('killswitch.state'))
    
    def set_state (self, state):
        self.switch.SetPower(state)
    
    def toggle_state (self):
        old_state = self.get_state()
        new_state = not old_state
        self.set_state(new_state)

    def get_type (self):
        return str(self.interface.GetProperty ('killswitch.type'))

def list_switches (ignore_list=[]):
    bus = dbus.SystemBus()
    hal_obj = bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
    hal = dbus.Interface(hal_obj, "org.freedesktop.Hal.Manager")
    switches = []
    for udi in hal.FindDeviceByCapability ("killswitch"):
        dev = bus.get_object('org.freedesktop.Hal', udi)
        s = RFKillSwitch (dev)
        if s.get_name() not in ignore_list:
            switches.append(s)
        else:
            del s
    return switches

if __name__ == '__main__':
    for sw in list_switches():
        n = sw.get_name()
        s = sw.get_state()
        t = sw.get_type()
        print "%s/%s: %i" % (t,n,s)

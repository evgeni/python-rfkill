#!/usr/bin/env python
#
#   rfkillgtk.py
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

import pygtk
pygtk.require('2.0')
import gtk

import rfkill

NAME_MAP = {
    'tpacpi_wwan_sw': 'ThinkPad WWAN',
    'tpacpi_bluetooth_sw': 'ThinkPad Bluetooth'
    }

IGNORE_LIST = [
    'hci0'
    ]
class RFKillGTKButton (gtk.Button):
    
    def __init__ (self, sw):
        self.sw = sw
        name = self.sw.get_name()
        if NAME_MAP.has_key(name):
            name = NAME_MAP[name]
        gtk.Button.__init__(self, name)
        self.set_use_underline(0)
        self.update()

    def update (self):
        img = gtk.Image()
        state = ('off','on')[self.sw.get_state()]
        img_file = 'icons/%s_%s.png' % (self.sw.get_type(), state)
        img.set_from_file(img_file)
        self.set_image(img)

class RFKillGTK:
    
    def __init__ (self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.vbox = gtk.VBox(homogeneous=True)
        self.buttons = []
        self.killall_button = gtk.Button("KILL 'EM ALL")
        self.killall_button.connect("clicked", self.toggle_all, None)
        self.vbox.pack_start(self.killall_button)
        for sw in rfkill.list_switches(IGNORE_LIST):
            b = RFKillGTKButton(sw)
            b.connect("clicked", self.toggle_one, None)
            self.buttons.append(b)
            self.vbox.pack_start(b)
        self.window.add(self.vbox)
        self.window.show_all()
        self.killall = 0

    def main (self):
        gtk.main()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def toggle_all (self, widget, data=None):
        for b in self.buttons:
            b.sw.set_state(self.killall)
            b.update()
        self.killall = not self.killall
        widget.set_label(("KILL 'EM ALL","START 'EM ALL")[self.killall])
            
    def toggle_one (self, widget, data=None):
        widget.sw.toggle_state()
        widget.update()

if __name__ == '__main__':
    r = RFKillGTK()
    r.main()

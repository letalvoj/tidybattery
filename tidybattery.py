#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       

import gtk
import gobject
import subprocess
import os

ACPI_CMD = 'acpi'
TIMEOUT = 10

class MainApp:

        last = 100

        def __init__(self):
                self.icon = gtk.StatusIcon()
                self.update_icon()
                gobject.timeout_add_seconds(TIMEOUT,self.update_icon)

        def get_battery_info(self):
                text = subprocess.check_output(ACPI_CMD).strip('\n')
                if not 'Battery' in text:
                        return {'state':"Unknown",
                                'percentage':0,
                                'tooltip':""
                                }
                data = text.split(',')
                return {'state':data[0].split(':')[1].strip(' '),
                                'percentage':int(data[1].strip(' %')),
                                'tooltip': text.split(':',1)[1][1:]
                                }

        def get_icon_name(self, state, percentage):
                if state == 'Discharging' or state == 'Unknown':
                        if percentage < 10:
                                return 'battery_empty'
                        elif percentage < 20:
                                return 'battery-caution'
                        elif percentage < 40:
                                return 'battery-low'
                        elif percentage < 60:
                                return 'battery_two_thirds'
                        elif percentage < 75:
                                return 'battery_third_fourth'
                        else:
                                return 'battery_full'
                elif state == 'Charged':
                        return 'battery_charged'
                else:
                        return 'battery_plugged'

        def notify_state(self, state, percentage):
                notify = 'notify-send -i battery-caution -t 5000 "Battery {info}" "less than {percent}% left"'
                if state == 'Discharging' or state == 'Unknown': 
                    if self.last > percentage:
                        if percentage == 5:
                            os.system(notify.format(info='critical', percent=percentage))
                        elif percentage == 10:
                            os.system(notify.format(info='low', percent=percentage))
                        elif percentage == 25:
                            os.system(notify.format(info='warning', percent=percentage))

        def update_icon(self):
                info = self.get_battery_info()
                icon_name = self.get_icon_name(info['state'],info['percentage'])
                self.icon.set_from_icon_name(icon_name)
                self.icon.set_tooltip_text(info['tooltip'])
                self.notify_state(info['state'],info['percentage'])
                self.last = info['percentage']
                return True

if __name__ == "__main__":
        try:
                MainApp()
                gtk.main()
        except KeyboardInterrupt:
                pass


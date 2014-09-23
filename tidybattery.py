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
import time
import re


ACPI_CMD = ['acpi', '-i']
TIMEOUT = 10

class MainApp:

        last_percentage = 100
        last_icon = ""

        def __init__(self):
                self.icon = gtk.StatusIcon()
                self.update_icon()
                gobject.timeout_add_seconds(TIMEOUT,self.update_icon)

        def get_battery_info(self):
                output = subprocess.check_output(ACPI_CMD).strip('\n')
                text = filter(lambda line: 'Battery' in line, output.split('\n'))
                batteries = len(text)/2

                if batteries == 0:
                    return {'states': ["Unknown"], 'percentage': 0.0, 'tooltip': "" }

                states = []
                overall_charge=0
                overall_capacity=0

                for b in range(0,batteries):
                    l1 = text[2*b][11:]
                    l2 = text[2*b + 1][11:]

                    a1 = l1.split(', ')
                    m2 = re.match(r"design capacity [0-9]+ mAh, last full capacity ([0-9]+) mAh = [0-9]+%", l2)

                    states.append(a1[0])
                    capacity = float(m2.group(1))
                    charge = float(a1[1][:-1]) / 100 * capacity

                    overall_charge += charge
                    overall_capacity += capacity

                percentage = overall_charge/overall_capacity * 100
                tooltip_lines = text[0::2]
                tooltip_lines.append("Overall charge: %.0f%s" % (percentage,'%'))

                return {'states':states, 'percentage':percentage, 'tooltip': "\n".join(tooltip_lines)}

        def get_icon_name(self, states, percentage):
                if 'Charged' in states:
                        return 'battery_charged'
                elif 'Discharging' in states:
                        if percentage < 10:
                                return 'battery_empty'
                        elif percentage < 20:
                                return 'battery-caution'
                        elif percentage < 40:
                                return 'battery-low'
                        elif percentage < 60:
                                return 'battery_two_thirds'
                        elif percentage < 80:
                                return 'battery_third_fourth'
                        else:
                                return 'battery_full'
                else:
                        return 'battery_plugged'

        def notify_state(self, states, percentage):
                notify = 'notify-send -i battery-caution -t 5000 "{info}" "less than {percent}% left"'
                if 'Discharging' in states:
                    if self.last_percentage > percentage:
                        if percentage == 5:
                            os.system(notify.format(info='Battery critical', percent=percentage))
                            time.sleep(5)
                            os.system('dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend > /dev/null &')
                        elif percentage == 10:
                            os.system(notify.format(info='Battery low', percent=percentage))
                        elif percentage == 25:
                            os.system(notify.format(info='Battery warning', percent=percentage))

        def get_resource_path(self, rel_path):
                dir_of_py_file = os.path.dirname(os.path.realpath(__file__))
                rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
                abs_path_to_resource = os.path.abspath(rel_path_to_resource)
                return abs_path_to_resource

        def update_icon(self):
                info = self.get_battery_info()
                icon = self.get_icon_name(info['states'],info['percentage'])
                
                if icon != self.last_icon:
                    icon_path = self.get_resource_path("./icons/%s.svg" % icon)
                    self.icon.set_from_file(icon_path)
                    self.last_icon = icon
                
                self.icon.set_tooltip_text(info['tooltip'])
                self.notify_state(info['states'],info['percentage'])
                self.last_percentage = info['percentage']
                return True

if __name__ == "__main__":
        try:
                MainApp()
                gtk.main()
        except KeyboardInterrupt:
                pass


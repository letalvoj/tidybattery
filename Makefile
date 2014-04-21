all:
	echo "Use with install or uninstall parameter only"

install: check
	cp -a tidybattery.py /usr/local/lib/tidybattery.py
	ln -s /usr/local/lib/tidybattery.py /usr/local/bin/tidybattery 
	chmod a+x /usr/local/lib/tidybattery.py

uninstall:
	rm /usr/local/lib/tidybattery.py || echo not there
	rm /usr/local/bin/tidybattery || echo not there

check:
	which notify-send
	which acpi

reinstall: uninstall install

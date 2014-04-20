all:
	echo "Use with install or uninstall parameter only"

install:
	cp -a tidybattery.py /usr/local/lib/tidybattery.py
	ln -s /usr/local/lib/tidybattery.py /usr/local/bin/tidybattery 
	chmod a+x /usr/local/lib/tidybattery.py

uninstall:
	rm /usr/local/lib/tidybattery.py
	rm /usr/local/bin/tidybattery

reinstall: uninstall install


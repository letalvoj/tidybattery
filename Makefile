all:
	echo "Use with install or uninstall parameter only"

install:
	chmod a+x tidybattery.py
	cp -a tidybattery.py /usr/local/lib/tidybattery.py
	ln -s /usr/local/lib/tidybattery.py /usr/local/bin/tidybattery 

uninstall:
	rm /usr/local/lib/tidybattery.py
	rm /usr/local/bin/tidybattery

reinstall: uninstall install


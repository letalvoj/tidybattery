INSTALL_DIR=/usr/local/lib/tidybattery
BIN_DIR=/usr/local/bin
all:
	echo "Use with install or uninstall parameter only"

install: check
	mkdir $(INSTALL_DIR)
	chmod a+x tidybattery.py
	cp -ra icons tidybattery.py $(INSTALL_DIR)
	ln -s $(INSTALL_DIR)/tidybattery.py $(BIN_DIR)/tidybattery 

uninstall:
	rm -rf $(INSTALL_DIR) || echo folder not there
	rm $(BIN_DIR)/tidybattery || echo file not there

check:
	which notify-send
	which acpi

reinstall: uninstall install



all : ui_gpio.py

ui_%.py : ui_%.ui 
	pyuic4 -i 0 $^ > $@

clean:
	rm -f *.pyc ui_*.py

deploy:
	scp run *py root@172.20.30.101:

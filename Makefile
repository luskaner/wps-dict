init:
	pip3 install -r requirements.txt

debian:
    apt-get install python3-gi
	apt-get install python3-requests
	apt-get install python3-colorama
	apt-get install python3-netaddr
	apt-get install python3-pyquery

### What is canakit-uk1104-api?
![A picture of device](http://www.canakit.com/media/catalog/product/cache/2/image/300x/5e06319eda06f020e43594a9c230972d/R/1/R1104.jpg)
This is canakit-uk1104-api, a RESTful API to control the functions on the Canakit UK1104 (1104) Data Acquisition Module.
This allows you to deploy a public facing API with the desired relay positions, and the microcontroller can poll for updates
using the computer it is attached to.

### What is the Canakit UK1104?
This is a cool little $50  USB Serial device which can control 4 relays. This software suite includes a client (for serial comms)
and a web-based API you could deploy anywhere for your pollers to connect to for relay status updates.

Information about the serial device:

	Name	: Canakit 4-Port USB Relay Controller with 6-Channel Temperature/Analog/Digital I/O Interface (Data Acquisition Module)
	Webpage	: http://www.canakit.com/4-port-usb-relay-controller.html
	Manual	: http://www.canakit.com/Media/Manuals/UK1104.pdf

The included class will support object based interaction with these serial commands:

	RELx.ON
	RELx.OFF
	RELx.TOGGLE
	RELx.GET
	RELS.ON
	RELS.OFF

### This Software
This software is broken into two parts, a Relay Poller Daemon and a Relay Server
##### Relay Status Poller Daemon
The folder relaypoller includes the software distribution that connects to the serial port. relaypoller.conf contains settings you may need to change.

This software polls a restful URL with your projects name and will call the API to change the relays.
##### Relay Server
This is a Flask based web server which stores the events.

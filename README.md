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

### Software Layout
There is two components to this system. A client that the Canakit runs (a deamonized process polling the board) and a seperate rest API server component, which can run over the network or on localhost. The API can be updated by remote clients by using the examples SEE EXAMPLE section.

#### Relay Poller
Found inside `relaypoller` tree. Acts as a restful client to the server. Runs as a deamon on the system connected to Canakit.
See README.md inside tree for instructions.
#### Relay Server
Found inside `relayserver` tree. Restful API service, that can run on the same system as the poller, or on a remote server of your choice. Gotta love networks. See README.md inside tree `relayserver` for setup instructions.

##### Examples
## Build new project
  curl -s -XGET localhost:5000/entity/projectboard1/ | python -m json.tool
	{
		"canakit1104": {
		    "light_system_project_name": "projectboard1", 
		    "relay": {
		        "1": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }, 
		        "2": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }, 
		        "3": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }, 
		        "4": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }
		    }
		}, 
		"x-i-made-this": "jonkelley@rackspace.com"
	}
## Build new project
  curl -s -XGET localhost:5000/entity/projectboard1/ | python -m json.tool
	{
		"canakit1104": {
		    "light_system_project_name": "projectboard1", 
		    "relay": {
		        "1": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }, 
		        "2": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }, 
		        "3": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }, 
		        "4": {
		            "lastchange": "2013-04-16 22:41:52.492750", 
		            "state": 0
		        }
		    }
		}, 
		"x-i-made-this": "jonkelley@rackspace.com"
	}

## Post relay number 1 to value 1
`curl -s -XPOST localhost:5000/entity/projectboard1/set/1/1`
## Post all relays to value 0
`curl -s -XPOST localhost:5000/entity/projectboard1/set/*/0`


##### Legal
This software and code is not written nor endorsed by Canakit Corporation, but by an individual author.
The Canakit Device, Canakit Name, Trademarks, Circuit Design and Implementation all © 2008 Cana Kit Corporation. All Rights Reserved.

### Relay Poller
![A picture of device](http://www.canakit.com/media/catalog/product/cache/2/image/300x/5e06319eda06f020e43594a9c230972d/R/1/R1104.jpg)

The relay poller is a http client that connects to the API as long as it's on the same network. You can run this on a computer with the API host on the same network, or you can run this on the same machine as the server too, I suppose.

## Basic Setup
1) You've already git cloned, congrats!
2) Edit relayserver.conf to reflect proper project name and project_uri, this is referenced in Step 4 under the RelayServer setup README.md
   If your relayserver is over the network... then change localhost to the network IP address.
3) Start poller with python relaypollerd.py
4) Process deamonizes, connects to your CANAKIT device, and your lights should be changing!!

### Relay Server
![A picture of device](http://www.canakit.com/media/catalog/product/cache/2/image/300x/5e06319eda06f020e43594a9c230972d/R/1/R1104.jpg)

The relay server is a restful API with a lightweight SQL database backend that is zero-configuration setup.
The basic premise of operation is:
* you POST relay values in
* your client pollers GET relay values out.

## Basic Usage, to trigger the project board.
1) You've already git cloned, congrats!
2) Edit relayserver.conf if desired
3) python app.py
4) Create a new project database skeleton:
   `curl -XGET localhost:5000/entity/projectboard1/`
   NOTE: This is also your url for [Poller]:project_uri in relaypoller.conf
4) Set relay 1 to value ON (hence set/1/1)
   `curl -XPOST localhost:5000/entity/lol/set/1/1 | python -m json.tool`
5) Set relay 2 to value ON (hence set/2/1)
   `curl -XPOST localhost:5000/entity/lol/set/2/1 | python -m json.tool`
6) Turn all relays OFF (hence set/*/0)
   `curl -XPOST localhost:5000/entity/lol/set/*/0 | python -m json.tool`
   
# TODO
WSGI Server Widget for use under Apache/Nginx


from flask import Blueprint
from flask import request   # Required to access request.method etc
from flask import Response  # Lets us get fancy with Responses.
module = Blueprint('relay', __name__)
import json

from classes.relay import relayobj #  sqlite lies within
import logging
log = logging.getLogger(__name__)


def jsontemplate(projectname,relay1,relay2,relay3,relay4,updated1,updated2,updated3,updated4):
    """ Auto JSON template generator """
    ilovecake =  {
                        "canakit1104": {
                        "light_system_project_name" : projectname,
                        "relay" : {
                                1: {
                                    "state": relay1,
                                    "lastchange" : updated1,
                                }, 
                                2: {
                                    "state": relay2,
                                    "lastchange" : updated2,
                                }, 
                                3: {
                                    "state": relay3,
                                    "lastchange" : updated3,
                                }, 
                                4: {
                                    "state": relay4,
                                    "lastchange" : updated4,
                                }, 
                            }
                        }, "x-i-made-this" : "jonkelley@rackspace.com"
                    }
    return ilovecake

@module.route('/entity/<projectname>.json', methods=['GET'])
@module.route('/entity/<projectname>/',     methods=['GET'])
def getrelay(projectname):
    """ This API call gets the current relay status """
    canakit = relayobj(projectname)
    if request.method == 'GET':
        return Response( json.dumps( jsontemplate(
                                projectname,
                                canakit.get_relaystate(1), canakit.get_relaystate(2),
                                canakit.get_relaystate(3), canakit.get_relaystate(4),
                                canakit.get_relayupdated(1),canakit.get_relayupdated(2),
                                canakit.get_relayupdated(3),canakit.get_relayupdated(4),
                            ) ),200,mimetype='application/json')

@module.route('/entity/<projectname>/set/<relayid>/<stateid>',      methods=['POST'])
@module.route('/entity/<projectname>.json/set/<relayid>/<stateid>', methods=['POST'])
def setrelay(projectname,relayid,stateid):
    """ This API call sets the relay state based on relay and project name """
    if request.method == 'POST':
        if int(relayid) > 4 or int(relayid) < 1:
            response =  { "???": "Invalid relay id: (" + relayid + ") is > 4"}
            return Response(json.dumps(response),420,mimetype='application/json')
        if int(stateid) > 2:
            response =  { "???": "Invalid relay state: (" + stateid + ") is > 2" }
            return Response(json.dumps(response),420,mimetype='application/json')
        canakit = relayobj(projectname)
        canakit.set_relay(relayid,stateid)
        return Response( json.dumps( jsontemplate(
                                projectname,
                                canakit.get_relaystate(1), canakit.get_relaystate(2),
                                canakit.get_relaystate(3), canakit.get_relaystate(4),
                                canakit.get_relayupdated(1),canakit.get_relayupdated(2),
                                canakit.get_relayupdated(3),canakit.get_relayupdated(4),
                            ) ),200,mimetype='application/json')

@module.route('/entity/<projectname>/set/*/<stateid>',      methods=['POST'])
@module.route('/entity/<projectname>.json/set/*/<stateid>', methods=['POST'])
def setrelays(projectname,stateid):
    """ This API call sets the relay state based on relay and project name """
    if request.method == 'POST':
        if int(stateid) > 2:
            response =  { "???": "Invalid relay state: (" + stateid + ") is > 2" }
            return Response(json.dumps(response),420,mimetype='application/json')
        canakit = relayobj(projectname)
        for i in [1,2,3,4]:
            canakit.set_relay(i,stateid)
        return Response( json.dumps( jsontemplate(
                                projectname,
                                canakit.get_relaystate(1), canakit.get_relaystate(2),
                                canakit.get_relaystate(3), canakit.get_relaystate(4),
                                canakit.get_relayupdated(1),canakit.get_relayupdated(2),
                                canakit.get_relayupdated(3),canakit.get_relayupdated(4),
                            ) ),200,mimetype='application/json')

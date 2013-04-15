#/usr/bin/env python
""" Based on modular app framework, modula: https://github.com/jonkelleyatrackspace/modula-api-skeleton """
########################################################################
# obligatory
from flask import Flask     # Everything kinda builds from here.
from flask import request   # Required to access request.method etc
from flask import Response  # Lets us get fancy with responses.
########################################################################
# converts http errors to json, nice.
from flask import jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response
########################################################################
# logging
from classes.logsystem import LogClass  # Logging is fanatical.
logclass = LogClass()                   # Instanciate or whatever you call it.
########################################################################

# Begin app
app = Flask('RelayServer')
# This ensures errors return as json.
for code in default_exceptions.iterkeys():
    app.error_handler_spec[None][code] = make_json_error
# Yay, we survived instanciation.
logclass.logger.info('Relayserver starting!')

# Test route.
@app.route('/',methods=['GET'])
def root():
    message = "{\n   \"message\": \"\033[1;34mACK -> %s, I am   \033[1;31mmodula\033[0m  \033[1;34m a modular flask based API\033[0m\" \n}" %( str(request.remote_addr) )
    return Response(message,200,mimetype='application/json')


import os, imp
def load_blueprints():
    """
        This code looks for any modules or packages in the given directory, loads them
        and then registers a blueprint - blueprints must be created with the name 'module'
        Implemented directory scan
        
        Bulk of the code taken from:
            https://github.com/smartboyathome/Cheshire-Engine/blob/master/ScoringServer/utils.py
    """
    logclass.logger.info('Registering blueprints!')
    path = 'blueprints'
    dir_list = os.listdir(path)
    mods = {}
    
    for fname in dir_list:
        if os.path.isdir(os.path.join(path, fname)) and os.path.exists(os.path.join(path, fname, '__init__.py')):
            try:
                logclass.logger.info('Registering blueprint (DIRECTORY) ... %s', fname)
                f, filename, descr = imp.find_module(fname, [path])
                mods[fname] = imp.load_module(fname, f, filename, descr)
                app.register_blueprint(getattr(mods[fname], 'module'))
            except:
                    logclass.logger.critical('Blueprint registration in subdir ('  + str(fname) + 
                    ') failed. Part of your API did not load. Recoverying...' , exc_info=True)
        elif os.path.isfile(os.path.join(path, fname)):
                name, ext = os.path.splitext(fname)
                if ext == '.py' and not name == '__init__':
                    try:
                        logclass.logger.info('Registering blueprint ... %s', fname)
                        f, filename, descr = imp.find_module(name, [path])
                        mods[fname] = imp.load_module(name, f, filename, descr)
                        app.register_blueprint(getattr(mods[fname], 'module'))
                    except:
                        logclass.logger.critical('Blueprint registration ('  + str(fname) + 
                        ') failed. Part of your API did not load. Skipping module...', exc_info=True)

load_blueprints()
# def load(app):
# from simple_page import simple_page
# app.register_blueprint(simple_page.module)

if __name__ == '__main__':
    app.run(debug=True)

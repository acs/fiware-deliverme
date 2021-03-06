# Copyright (C) 2015 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Implementation of FIWARE deliverME REST API
#
# Authors:
#   Alvaro del Castillo <acs@bitergia.com>

import crypt, json, logging, sys, traceback
from os import path, listdir, getcwd

from flask import Flask, request, Response, abort

app = Flask(__name__)

def check_login(user, passwd):
    check = False
    authfile = "auth.conf"
    try:
        with open(authfile) as f:
            content = f.readlines()
        for login in content:
            if len(login.split(":")) != 2: continue # Not a user line
            if login.split(":")[0] == user:
                userpw = login.split(":")[1][:-1] # remove \n
                print passwd, userpw, crypt.crypt(passwd, userpw)
                if crypt.crypt(passwd, userpw) == userpw:
                    check = True
                    break
    except:
        logging.error("Auth file %s not readable: " + authfile)
        traceback.print_exc(file=sys.stdout)
    return check

@app.route("/api/login",methods = ['GET'])
def login():
    """ Check login for the user """
    # Not sure if we should return a token so the server could check always auth
    # If not modifying the client could be enough to get access to the service
    user = request.args.get('username')
    passwd = request.args.get('password')

    if check_login(user, passwd):
        return ""
    else:
        abort(401)

@app.route("/api/deliverables/<dashboard>",methods = ['GET'])
def create_deliverable(deliverable):
    """ Create the deliverable and return a URL to access it """
    deliverable_url = ""
    return deliverable_url

@app.route("/api/deliverables",methods = ['GET'])
def get_dashboards():
    """Return a list with the deliverables available"""
    deliverables_path = '.'
    deliverables = [f for f in listdir(deliverables_path) if path.isfile(f) and f.endswith('.zip')]
    return json.dumps(deliverables)

if __name__ == "__main__":
    app.debug = True
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')
    app.run()

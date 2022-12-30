from flask import Flask, session, request, redirect
#from flask_session import Session

import pycurl
from io import BytesIO
import urllib
import json
import base64
import pprint

import random
import os

import client_config

app = Flask(__name__)

app.secret_key = os.urandom(28)




pp = pprint.PrettyPrinter(indent=4)

@app.route('/')
def hello():
    if (request.args.get('action') and request.args.get('action') == 'login'):
        return login()
    elif (request.args.get('action') and request.args.get('action') == 'logout'):
        return logout()
    elif request.args.get('code'):
        return exchange_token()
    elif (request.args.get('action') == None):
        return is_logged_in()
    



def is_logged_in():
    the_response = 'No Response'
    if(session.get('user_id',None)):
        the_response += '<h3> Logged In </h3> '
        the_response += '<p>User ID: '+ session.get('user_id') +'</p> '
        the_response += '<p>Email: '+ session.get('email') +'</p> '
        the_response += '<p><a href="?action=logout">Log Out</a></p>'

        the_response += '<h3> ID Token </h3> '
        the_response += '<pre> '
        
        data = api_request(client_config.user_info_url)
        the_response += str(data)
        the_response += '</pre> '


    else:
        the_response = """
                        <h3> Not Logged In </h3>
                        <p><a href="?action=login">Log In</a></p>
        """
    return the_response

def login():
    session['state'] = str(random.getrandbits(128))
    session['access_token'] = None
    params =  {
            'scope' : 'openid email ',
            'client_id': client_config.google_client_id,
            'redirect_uri': client_config.base_url,
            'state' : session['state'],
            'response_type' : 'code'
            }

    return redirect(client_config.authorize_url+'?' + urllib.parse.urlencode(params),302)
        

def logout():
    session['access_token'] = None
    session['user_id'] = None

            
    return redirect(client_config.base_url,302)

def exchange_token():
    if (request.args.get('state',None) == None) or (session.get('state',"no session state").strip() != request.args.get('state', "no request state").strip()):
        return redirect(client_config.base_url + '?error=invalid_state',302)


    #Exchange auth token for access token
    post_params = {
            'grant_type': 'authorization_code',
            'client_id' : client_config.google_client_id,
            'client_secret' : client_config.google_client_secret,
            'redirect_uri': client_config.base_url,
            'code' : request.args.get('code'),
            'state' : session.get('state',None)
            }
    data = api_request(client_config.token_url,post_params)

    jwt = data['id_token'].split('.')

    user_info = json.loads(base64.b64decode(jwt[1]))
    pp.pprint('use_info: ')

    pp.pprint(user_info)
    session['user_id'] = user_info['sub']
    session['email'] = user_info['email']

    session['access_token'] = data['access_token']
    session['id_token'] = data['id_token']
    session['user_info'] = user_info

    return redirect( client_config.base_url,302)




def api_request(url, post = None , headers = []):
    crl= pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(pycurl.VERBOSE, 1)

    if post:
        crl.setopt(crl.POSTFIELDS,urllib.parse.urlencode(post)) 
    headers = [
        'Accept: application/vnd.github.v3+json, application/json',
        'User-Agent: https://example-app.com'
        ]
    if session.get("access_token",None):
        headers += ['Authorization: Bearer '+session.get("access_token",None)]
    crl.setopt(crl.HTTPHEADER, headers)
    response = crl.perform_rs()
    #print('response from curl is : '+response)
    return json.loads(response)


if __name__ == '__main__':
    app.run()



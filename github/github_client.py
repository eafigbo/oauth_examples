import flask
from flask import Flask, session, request, redirect
#from flask_session import Session

import pycurl
from io import BytesIO
import urllib
import json

import random
import os

import client_config

app = Flask(__name__)

app.secret_key = os.urandom(28)
#if __name__ == '__main__':
#    app.run()


# Check Configuration section for more details
#SESSION_TYPE = 'redis'
#app.config.from_object(__name__)
#Session(app)




@app.route('/')
def hello():
    if (request.args.get('action') and request.args.get('action') == 'login'):
        return login()
    elif (request.args.get('action') and request.args.get('action') == 'logout'):
        return logout()
    elif request.args.get('code'):
        return exchange_token()
    elif (request.args.get('action') and request.args.get('action') == 'repos'):
        return get_repos()
    elif (request.args.get('action') == None):
        return is_logged_in()
    





def is_logged_in():
    the_response = 'No Response'
    if(session.get('access_token',None)):
        the_response = """
                        <h3> Logged In </h3>
                        <p><a href="?action=repos">View Repos</a></p>
                        <p><a href="?action=logout">Log Out</a></p>
        """
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
            'scope' : 'user public_repo',
            'response_type': 'code',
            'client_id': client_config.github_client_id,
            'redirect_uri': client_config.base_url,
            'state' : session['state']
            }

    return redirect(client_config.authorize_url+'?' + urllib.parse.urlencode(params),302)
        

def logout():
    session['access_token'] = None
            
    return redirect(client_config.base_url,302)

def exchange_token():
    if (request.args.get('state',None) == None) or (session.get('state',"no session state").strip() != request.args.get('state', "no request state").strip()):
        return redirect(client_config.base_url + '?error=invalid_state',302)


    #Exchange auth token for access token
    post_params = {
            'grant_type': 'authorization_code',
            'client_id' : client_config.github_client_id,
            'client_secret' : client_config.github_client_secret,
            'redirect_uri': client_config.base_url,
            'code' : request.args.get('code'),
            'state' : session.get('state',None)
            }
    token = api_request(client_config.token_url,post_params)
    
    session['access_token'] = token['access_token']
    return redirect( client_config.base_url,302)


def get_repos():
    the_response =''
    params = {
            'sort': 'created',
            'direction' : 'desc'
            }
    repos = api_request(client_config.api_url_base + 'user/repos?' + urllib.parse.urlencode(params))
    the_response = '<ul>'
    for repo in repos:
        the_response += '<li><a href="'+ repo['html_url'] + '">'+ repo['name'] + '</a></li>'
    the_response +='</ul>'

    if (request.args.get('action') == None):
        if (session.get('access_token',None)):
            the_response += """
            <h3>Logged In</h3>
            <p><a href="?action=repos"> View Repos</a>
            <p><a href="?action=logout"> Log Out</a>
            """
        else:
            the_response += """
            <h3>Not Logged In</h3>
            <p><a href="?action=login"> Log In</a>
            """
    return the_response





def api_request(url, post = None , headers = []):
    crl= pycurl.Curl()
    crl.setopt(crl.URL, url)
    #crl.setopt(pycurl.VERBOSE, 1)

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



from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from architectureDecisions.settings import *
import logging
import logging.handlers

if not DEBUG:
    #Logging
    log_path = "/volume/log"
    LOG_FILENAME = log_path + "/" + "architecture-decisions.log"
    logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=7)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)


@csrf_exempt
def authenticate(request):
    body = json.loads(request.body.decode('utf-8'))
    headers = {'oauth_consumer_key': oauth_consumer_key,
               'oauth_consumer_secret': oauth_secret_key,
               "Content-Type": "application/json"}
    payload = {"username": body["user"],
               "password": body["password"]}
    req = requests.post(authenticatorAPI + "/authenticate", data=json.dumps(payload), headers=headers)
    json_response = json.loads(req.content.decode('utf-8'))
    if req.status_code == 200:
        set_session(json_response, body, request)
        return JsonResponse({"authenticated": True}, safe=False)
    if not DEBUG:
        logging.info("Authentication failed - " + "Status code: " + str(req.status_code) + " User: " + body["user"])
    return JsonResponse({"authenticated": False}, safe=False)


def set_session(json_response, body,  request):
    access_token = json_response["accessToken"]
    request.session["username"] = body["user"]
    request.session["jwt"] = json_response["jwt"]
    request.session["access_token"] = access_token


def authorization(request):
    jwt_token = request.session.get("jwt")
    jwt_content = (jwt_token.split("."))[1]
    jwt_content += '=' * (-len(jwt_content) % 4)
    decoded = jwt_content.decode("base64")
    request.session["admin"] = False
    if adminGroup in decoded:
        request.session["admin"] = True
    else:
        request.session["admin"] = False
    return request.session["admin"]


def logout(request):
    try:
        access_token = request.session["access_token"]
        request.session.flush()
        revoke_session(access_token)
    except KeyError:
        pass
    return render(request, 'login.html', {})


def revoke_session(access_token):
    headers = {'oauth_consumer_key': oauth_consumer_key,
               'oauth_consumer_secret': oauth_secret_key,
               "Content-Type": "application/json"}
    payload = {"token": access_token}
    req = requests.post(authenticatorAPI + "/revoke", data=json.dumps(payload), headers=headers)


def authenticated(request):
    try:
        request.session["access_token"]
        return True
    except KeyError:
        return False

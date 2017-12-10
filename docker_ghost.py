from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .celery import app

import os, sys, json, docker

from .docker_container import ghost_container

import logging
from .logger import getlogger
#logger = getlogger(logging.DEBUG, logging.StreamHandler())
logger = getlogger(logging.DEBUG)

#@csrf_exempt
def ghost_api(request):
    url = None
    output = ""
    option = {}

    received = {}
    if request.method == "POST":
        try:
            body = request.body.decode()
            received = json.loads(body)
        except Exception as e:
            logger.debug(str(e))
            #return HttpResponse(str(e), status=400)
            return JsonResponse({"error":str(e)})
    elif request.method == "GET":
        received = request.GET

    if received:
        if "url" in received:
            url = received["url"]
        if "method" in received:
            option["method"] = received["method"]
            if option["method"] == "POST" and "body" in received:
                option["body"] = received["post_data"]
        if "user_agent" in received:
            option["user_agent"] = received["user_agent"]
        if "timeout" in received:
            option["wait_timeout"] = received["timeout"]
        if "headers" in received:
            option["headers"] = received["headers"]
        if "proxy" in received:
            option["proxy"] = received["proxy"]
        if "serialize" in received:
            option["serialize"] = received["serialize"]
        if "no_remove" in received:
            option["no_remove"] = True

    response = None
    if url:
        cli = docker.Client(base_url='unix://var/run/docker.sock')
        cid = ghost_container(cli, image="myghost:latest")
        try:
            if option:
                option = json.dumps(option)
            #res = run_ghost.delay(cid, url, option=option)
            res = run_ghost(cid, url, option=option)
            #response = JsonResponse(res.get())
            response = JsonResponse(json.loads(res))
        except Exception as e:
            logger.error(str(e))
            response = JsonResponse({
                "error":str(e),
            })
        if "no_remove" in option:
            cli.stop(cid, timeout=300)
            cli.remove_container(cid, force=True)

    if response:
        return response

    #return HttpResponse("Invalid Request", status=400)
    return JsonResponse({"error":"Invalid Request"})

@app.task(soft_time_limit=3600)
def run_ghost(cid, url, option={}):
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    logger.debug(cid)
    response = cli.start(container=cid)
    command = ["python3", "run_ghost.py", url, cid]
    if option:
        command.append(option)
    logger.debug(command)
    e = cli.exec_create(cid, command)
    for line in cli.exec_start(e["Id"], stream=True):
        logger.debug(line)
    command = ["cat", "ghost.json"]
    e = cli.exec_create(cid, command)
    logger.debug(e)
    result = cli.exec_start(e["Id"], stream=False)
    return result

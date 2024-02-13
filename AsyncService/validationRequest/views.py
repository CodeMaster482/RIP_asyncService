from django.shortcuts import render

import json
import time
import random
import requests

from concurrent import futures

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

executor = futures.ThreadPoolExecutor(max_workers=1)

global cnt, sleep_const

ServerToken = 'qwerty'
url = 'http://127.0.0.1:8080/api/operations/user-form-finish'

cnt = 0
sleep_const = 2

def get_random_status():
    if random.random() < 0.5:
        return 'одобрен'
    else:
        return 'отклонен'
    
def modify_body(body):
    time.sleep(sleep_const)
    body['status'] = get_random_status()
    body['Server_Token'] = ServerToken
    return body

def status_callback(task):
    try:
        result = task.result()
        print(result)
    except futures._base.CancelledError:
        return
    requests.put(url, data=json.dumps(result), timeout=3)

@api_view(['Put'])
def validRequest(request):
    r_body = json.loads(request.body)
    task = executor.submit(modify_body, r_body)
    task.add_done_callback(status_callback)
    return Response(status=status.HTTP_200_OK)

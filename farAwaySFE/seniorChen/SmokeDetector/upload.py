# coding: utf-8
import requests
import os
import json

# ip = "192.168.0.25:8080"
ip = "localhost:8080/blacksmoke"
token = ""


def initToken():
    global token
    url = f"http://{ip}/api/v1/oauth/token"
    jsondata = {
        "clientId": "098f6bcd4621d373cade4e832627b4f6",
        "userName": "admin",
        "password": "sfe5188",
        "captchaCode": "232",
        "captchaValue": "232"
    }

    try:
        retval = requests.post(url, json=jsondata).text
        data = json.loads(retval)
        token = data["content"]["access_token"]
    except:
        print(retval.text)


def upload(data, filenames):
    url = f"http://{ip}/api/v1/dataReceive/uploadsSmokeMessage"
    headers = {"Authorization": f"bearer {token}"}

    files = {}
    for i, f in enumerate(filenames):
        files[f"file{i+1}"] = open(f, "rb")

    response = requests.request("POST", url, data=data, files=files, headers=headers)
    try:
        # print(response.text)
        data = json.loads(response.text)
    except:
        return False

    if data.get("errcode") == 0:
        return True
    print(response.text)
    return False


if __name__ == "__main__":
    data = {
        "stNumber": "1",
        "stName": "test",
        "lineNo": "1",
        "ringelmanEmittance": "3",
        "plate": "粤A78541",
        "plateColor": "蓝色",
        "vehicleType": "0",
        "vehicleOwnerShip": "1",
        "greenYellowCar": "0",
        "throughTime": "1505359864",
        "remarks": ""
    }

    initToken()
    print(token)
    # print(upload(data, filenames=["1/0.jpg", "1/1.jpg", "1/video.mp4"]))

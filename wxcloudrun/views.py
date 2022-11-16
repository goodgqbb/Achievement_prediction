from datetime import datetime
from flask import render_template, request,Flask
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import pkuseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
import  os
import jieba
import json
import requests
from flask import Flask, request, make_response
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
API_KEY = "3bZkFHFfLOUg091GPgRkeOVk"
SECRET_KEY = "V8P7KmzmvKSKWt4abbLLo1RmbqoC0qTz"
def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

@app.route('/', methods=['POST'])
def upload():
    
    text = request.json.get('text')
    try:
        url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + get_access_token()
        payload = json.dumps({
            "text": text
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': '/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(json.dumps(response.json()))
        if response['items'][0]['positive_prob']>=response['items'][0]['negative_prob']:
            return json.dumps(1, ensure_ascii=False)
        else :
            return json.dumps(0, ensure_ascii=False)

    except TencentCloudSDKException as err:
        print(err)
        return json.dumps('error!!!!', ensure_ascii=False)

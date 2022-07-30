from global_variables import *
from typing import Optional
from requests import Response
import requests
import json



def create_headers(extra_hdrs):
    headers = { "Finicity-App-Key" : app_key,
                "Content-Type" : "application/json",
                "Accept" : "application/json",
                }
    if extra_hdrs:
        headers.update(extra_headers)
    return headers



def create_data_for_token():
    data = {
            "partnerId" : partner_id,
            "partnerSecret" : partner_secret,
            }
    return data



def post(path:str, 
        data: Optional[dict],
        extra_headers: Optional[dict] = None,
        ) -> Response:
    url = base_url + path
    headers = create_headers(extra_headers)
    response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data), 
            )
    return response



def create_token(path:str) -> Response:
    path = path_map[path]
    data = create_data_for_token()

    response = post(path, data)
    if response.status_code == 200:
        return response.json()['token']
    else:
        raise Exception(f"authentication issue "
        "{response.status_code}: {response.content}")





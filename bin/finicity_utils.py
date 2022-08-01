from global_variables import *
from typing import Optional
from requests import Response
import requests
import json
import datetime


def list_to_dq_str(xs):
    return "|".join([ '"' + i + '"' for i in xs ])



def write_log(file_name:str, content:str):
    with open(file_name, 'a+') as fwp:
        fwp.write(content + "\n")



def create_headers(extra_hdrs):
    headers = { "Finicity-App-Key" : app_key,
                "Content-Type" : "application/json",
                "Accept" : "application/json",
                }
    if extra_hdrs:
        headers.update(extra_hdrs)
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


def post_v1(path:str,
        params:  Optional[dict],
        data: Optional[dict],
        extra_headers: Optional[dict] = None,
        ) -> Response:
    url = base_url + path
    headers = create_headers(extra_headers)
    response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            params=params,
            )
    return response




def get(path: str, 
        params: Optional[dict] = None, 
        extra_headers: Optional[dict] = None,
        ) -> Response:
    url = base_url + path
    headers = create_headers(extra_headers)
    response = requests.get(
            url, 
            headers=headers, 
            params=params
            )
    return response


def delete(path:str,
        extra_headers: Optional[dict] = None,
        ) -> Response:
    url = base_url + path
    headers = create_headers(extra_headers)
    response = requests.delete(
            url,
            headers=headers,
            )
    return response


def create_token(path:str) -> str:
    path = path_map[path]
    data = create_data_for_token()
    file_name = f_log + token_file
    cur_time = datetime.datetime.now()

    response = post(path, data)
    if response.status_code == 200:
        token = response.json()['token']
        content_xs = [ 
                token,  
                str(cur_time), 
                str(response.status_code),
                "", 
                "SUCCESS"
                ]
        content = list_to_dq_str(content_xs)
        write_log(file_name, content)
        return token
    else:
        content_xs = [ 
                "",  
                str(cur_time), 
                str(response.status_code),
                str(response.content),
                "FAILED" 
                ]
        content = list_to_dq_str(content_xs)
        write_log(file_name, content)
        raise Exception(f"authentication issue "
        f"{response.status_code}: {response.content}")


def add_customer(path:str, token:str, data: Optional[dict]):
    path = path_map[path]
    extra_header = { "Finicity-App-Token" : token }
    file_name = f_log + add_cust_file
    cur_time = datetime.datetime.now()

    response = post(path, data, extra_header)
    username = data.get('username','')
    firstname = data.get('firstName','')
    lastname = data.get('lastName','')

    if response.status_code == 200 or response.status_code == 201:
        resp = response.json()
        f_customer_id = resp['id']
        f_username = resp['username']
        f_created_date = resp['createdDate']

        content_xs = [ 
                token, 
                username, 
                firstname, 
                lastname,  
                str(cur_time), 
                f_customer_id, 
                f_username, 
                f_created_date, 
                str(response.status_code),
                "",
                "SUCCESS" 
                ]
        content = list_to_dq_str(content_xs)

        write_log(file_name, content)
        return f_customer_id, f_username, f_created_date
    else:
        content_xs = [ 
                token, 
                username, 
                firstname, 
                lastname, 
                str(cur_time), 
                "", 
                "", 
                "", 
                str(response.status_code),
                str(response.content),
                "FAILED"
                ]
        content = list_to_dq_str(content_xs)
        write_log(file_name, content)
        raise Exception(f"adding customer  issue "
        f"{response.status_code}: {response.content}")



def get_customers(path:str, token:str, params: Optional[dict]):
    path = path_map[path]
    extra_header = { "Finicity-App-Token" : token }
    cur_time = datetime.datetime.now()
    cur_time1 = cur_time.strftime("%Y%m%d_%H%M%S")
    file_name = f_log + cur_time1 +"_"+  get_customers_file

    response = get(path, params, extra_header)
    if response.status_code == 200 or response.status_code == 201:
        resp = response.json()
        limit = params.get('limit',25)
        start = 1
        f_found = resp['found']
        f_more_avaliable = resp['moreAvailable']
        loop_cnt = int(f_found / int(limit)) + 1

        final_xs = []
        for i in range(1,loop_cnt+1):
            params1 = { 'start' : start, 'limit' : limit }
            params.update(params1)
            response1 = get(path, params, extra_header)
            start = start + limit 
            if response1.status_code == 200 or response1.status_code == 201:
                resp1 = response1.json()
                customers = resp1['customers']
                if customers:
                    cust_element = [ 
                            ( i['id'] ,
                            i['username'] , 
                            i['type'], 
                            i['createdDate'])
                            for i in customers
                            ]
                    for j in cust_element:
                        final_xs.append(j)
                        content = list_to_dq_str(list(j))
                        write_log(file_name, content)
            else:
                 raise Exception(f"get customers  issue "
                         f"{response.status_code}: {response.content}")
        return final_xs


    else:
        raise Exception(f"adding customer  issue "
        f"{response.status_code}: {response.content}")


def get_customer_by_id(
        path:str, 
        token:str, 
        customer_id:str
        ):
    path = path_map[path] + "/" + customer_id
    extra_header = { "Finicity-App-Token" : token }
    cur_time = datetime.datetime.now()
    cur_time1 = cur_time.strftime("%Y%m%d_%H%M%S")
    file_name = f_log + cur_time1 +"_"+  get_customers_file
    params={}

    response = get(path, params, extra_header)
    if response.status_code == 200 or response.status_code == 201:
        resp = response.json()
        id1 = resp.get('id','')
        username = resp.get('username','')
        firstname = resp.get('firstName','')
        lastname = resp.get('lastName','')
        type1 = resp.get('type','')
        created_date = resp.get('createdDate','')
        xs = [ 
                id1, username,
                firstname, lastname,
                type1, created_date
                ]
        return xs 
    else:
        raise Exception(f"get customer by id issue "
        f"{response.status_code}: {response.content}")


def delete_customer_by_id(
        path:str,
        token:str,
        customer_id:str
        ):
    path = path_map[path] + "/" + customer_id
    extra_header = { "Finicity-App-Token" : token }
    cur_time = datetime.datetime.now()
    cur_time1 = cur_time.strftime("%Y%m%d_%H%M%S")
    file_name = f_log + cur_time1 +"_"+  delete_customers_file

    response = delete(path, extra_header)
    if response.status_code == 204:
        content_xs = [
                token,
                customer_id,
                str(cur_time),
                str(response.status_code),
                str(response.content),
                "SUCCESS"
                ]
        content = list_to_dq_str(content_xs)
        write_log(file_name, content)

    else:
        content_xs = [
                token,
                customer_id,
                str(cur_time),
                str(response.status_code),
                str(response.content),
                "FAILED"
                ]
        content = list_to_dq_str(content_xs)
        write_log(file_name, content)
        raise Exception(f"get customer by id issue "
        f"{response.status_code}: {response.content}")


def generate_url(path:str, token:str, customer_id, data: Optional[dict]=None):
    path = path_map[path]
    extra_header = { "Finicity-App-Token" : token }
    file_name = f_log + generate_url_file
    cur_time = datetime.datetime.now()

    data1 = {"partnerId" : partner_id,
             "customerId": customer_id
            }

    data = data1 if not data else data.update(data1)

    response = post(path, data, extra_header)
    print(response.json())
    customer_id = data.get('customerId','')
    if response.status_code == 200 or response.status_code == 201:
        resp = response.json()
        link = resp.get('link','')

        content_xs = [
                token,
                customer_id,
                str(cur_time),
                str(response.status_code),
                "",
                "SUCCESS"
                ]
        content = list_to_dq_str(content_xs)

        write_log(file_name, content)
        return link
    else:
        content_xs = [
                token,
                customer_id,
                str(cur_time),
                str(response.status_code),
                str(response.content),
                "FAILED"
                ]
        content = list_to_dq_str(content_xs)
        write_log(file_name, content)
        raise Exception(f"generate_url issue "
        f"{response.status_code}: {response.content}")



def trnx_rprt(
        path:str,
        token,
        customer_id, 
        params: Optional[dict]=None, 
        data: Optional[dict]=None):
    path = path_map[path] + "/" + customer_id + "/transactions"
    print(path)
    extra_header = { "Finicity-App-Token" : token }
    cur_time = datetime.datetime.now()
    cur_time1 = cur_time.strftime("%Y%m%d_%H%M%S")
    file_name = f_log + cur_time1 + "_" + trnx_rprt_file

    response = post_v1(path, params, data, extra_header)
    print(response.json())
    if response.status_code == 200 or response.status_code == 201:
        resp = response.json()
        return resp
    else:
        raise Exception(f"transactionreport  issue "
        f"{response.status_code}: {response.content}")

from datetime import datetime

import pytest
import requests
import json
import allure

@allure.feature("按线路名称查询")
def test_linename_query(xingbo_get_token):
    url = "http://10.10.106.250:29999/api/line/feeders/page"
    headers = {
        'Authorization': xingbo_get_token
    }
    filename = "F002"
    raw_data = {"deptIds":[],"feederIds":[filename],"feederTypes":[],"pageNum":1,"pageSize":20}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for item in response_dict['data']['list']:
            item_feederId = item.get("feederId")
            assert filename in item_feederId
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request failed: {e}")
@allure.feature("按线路名称查询")
def test_linetype_query(xingbo_get_token):
    url = "http://10.10.106.250:29999/api/line/feeders/page"
    headers = {
        'Authorization': xingbo_get_token
    }
    filetype = "1"
    raw_data = {"deptIds":[],"feederIds":[],"feederTypes":[filetype],"pageNum":1,"pageSize":20}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for item in response_dict['data']['list']:
            item_feederType = item.get("feederType")
            assert filetype == str(item_feederType)
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request failed: {e}")
@allure.feature("分页切换")
def test_paging_query(xingbo_get_token):
    url = "http://10.10.106.250:29999/api/line/feeders/page"
    headers = {
        'Authorization': xingbo_get_token
    }
    pageSize = "10"
    raw_data = {"deptIds":[],"feederIds":[],"feederTypes":[],"pageNum":1,"pageSize":pageSize}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        pages = response_dict['data']['pages']
        total = response_dict['data']['total']
        if int(total) % int(pageSize) != 0:
            assert int(total) // int(pageSize) + 1 == int(pages)
        else:
            assert int(total) // int(pageSize) == int(pages)
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request failed: {e}")
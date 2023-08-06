# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@version    : v1.0
@author     : fangzheng
@contact    : fangzheng@rp-pet.cn
@software   : PyCharm
@filename   : Azkaban.py
@create time: 2023/4/7 4:00 PM
@modify time: 2023/4/7 4:00 PM
@describe   : azkaban工具类
-------------------------------------------------
"""

import requests
import json


class Azkaban:
    def __init__(self, username, password, url):
        self.url = url
        self.username = username
        self.password = password
        self.session = self.get_session_id()

    def get_session_id(self):
        data = {
            "action": "login",
            "username": self.username,
            "password": self.password
        }
        res = requests.post(self.url, data)
        if res.status_code == 200:
            response = json.loads(res.text)
            return response['session.id']
        return None

    def _get(self, params, url=""):
        params['session.id'] = self.session
        response = requests.get(self.url + "/" + url, params=params)
        return json.loads(response.text)

    def fetch_exec_flow(self, exec_id):
        """
        获取Execution详细执行信息
        :param exec_id:
        :return:
        """
        data = {
            "ajax": "fetchexecflow",
            "execid": f'{exec_id}'
        }
        result = self._get(params=data, url="executor")
        return result

    def get_running(self, project, flow):
        """
        获取正在运行的Executions
        :param project:项目名称
        :param flow:流名称
        :return:
        """
        data = {
            "ajax": "getRunning",
            "project": f'{project}',
            "flow": f'{flow}'
        }
        result = self._get(params=data, url="executor")
        return result

    def fetch_project_flows(self, project):
        """
        获取项目所有flow信息
        :param project:项目名称
        :return:
        """
        data = {
            "ajax": "fetchprojectflows",
            "project": f'{project}'
        }
        result = self._get(params=data, url="manager")
        return result

    def fetch_flow_jobs(self, project, flow):
        """
        获取Flow的所有作业
        :param project:
        :param flow:
        :return:
        """
        data = {
            "ajax": "fetchflowgraph",
            "project": f'{project}',
            "flow": f'{flow}',
        }
        result = self._get(params=data, url="manager")
        return result

    def fetch_flow_executions(self, project, flow, start, length):
        """
        给定项目名称和特定的流，此API调用提供相应执行的列表。这些执行是按照提交时间顺序排序的。
        此外，还需要参数来指定列表的起始索引和长度。这最初是用来处理分页的。
        :param project:
        :param flow:
        :param start:起始索引
        :param length:长度
        :return:
        """
        data = {
            "ajax": "fetchFlowExecutions",
            "project": f'{project}',
            "flow": f'{flow}',
            "start": f'{start}',
            "length": f'{length}'
        }
        result = self._get(params=data, url="manager")
        return result


if __name__ == '__main__':
    azkaban = Azkaban("azkaban", "azkaban", "http://10.202.1.6:8084")
    print(azkaban.fetch_exec_flow(264))
    print(azkaban.get_running(project="test", flow="datawarehouse_end"))
    print(azkaban.fetch_project_flows("datawarehouse"))
    print(azkaban.fetch_flow_jobs(project="datawarehouse", flow="datawarehouse_end"))

    print(azkaban.fetch_flow_executions(project="test", flow="datawarehouse_end", start=0, length=1))
    print(azkaban.fetch_flow_jobs(project="test", flow="datawarehouse_end"))



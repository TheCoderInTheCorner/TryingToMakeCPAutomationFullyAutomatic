import requests
from bs4 import BeautifulSoup
import subprocess

url = "https://www.uscyberpatriot.org/Pages/Readme/cp17_tr2_m_ubu22_readme_jsgrxe68wc.aspx"
response = requests.get(url)

whoami = 'perry'
#whoami = subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout
whoami.strip()
#print(whoami.stdout)


# Retrieving the html text from the cyberpatriots website
if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    htmlText = soup.get_text()
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")


# Cleaning the Data
if whoami in htmlText:
    AuthorizedUsers = htmlText[htmlText.find(whoami):htmlText.find('Competition Guidelines')]
    AuthorizedUsers = AuthorizedUsers.splitlines()

for i in AuthorizedUsers:
    AuthorizedUsers[AuthorizedUsers.index(i)] = i.strip()

AuthorizedUsers = [item for item in AuthorizedUsers if 'password' not in item and item != '' and item != 'Authorized Users:']
AuthorizedUsers.pop(0)

print(AuthorizedUsers)

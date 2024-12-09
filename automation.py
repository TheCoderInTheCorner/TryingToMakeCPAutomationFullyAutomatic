import subprocess
import requests
from bs4 import BeautifulSoup

url = "https://www.uscyberpatriot.org/Pages/Readme/cp17_tr2_m_ubu22_readme_jsgrxe68wc.aspx"
response = requests.get(url)

whoami = 'perry'
#whoami = subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout
whoami.strip()


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

# Deleting and Adding Users
AuthorizedUsers = set(AuthorizedUsers)
AllUsers = subprocess.run('ls /home', shell=True, capture_output=True, text=True).stdout.splitlines()
for i in AllUsers:
    AllUsers[AllUsers.index(i)] = i.strip()
AllUsers = set(AllUsers)

usersToRemove=AllUsers.difference(AuthorizedUsers)
usersToAdd=AuthorizedUsers.difference(AllUsers)

'''
HEY!! USE ANSI ESCAPE CODES TO MAKE THIS LOOK GOOD LATER
'''
print(f'Found {len(usersToAdd)} Users That Need To Be Added') #Using ANSI escape codes
for i in usersToAdd:
    ans=input(f'Would You Like To Add User {i}?').lower()
    if ans == 'y':
        cmd = 'sudo adduser ' + i
        adding_User=subprocess.run(cmd, shell=True)
    else:
        print(f'DID NOT ADD USER {i}')

print(f'FOUND {len(usersToAdd)} USERS THAT NEED TO BE DELETED')

whoami = subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout
whoami.strip()
for i in usersToRemove:
    ans=input(f'WOULD YOU LIKE TO DELETE {i}?').lower()
    if ans == 'y':
        if i.strip() != whoami:
            cmd = 'sudo deluser ' + i + ' --remove-home'
            deleting_User=subprocess.run(cmd, shell=True)
        else:
            print('YOU CANNOT DELETE YOURSELF')
    else:
        print(f'DID NOT DELETE USER {i}')

import subprocess
from bs4 import BeautifulSoup
import requests

'''


Created By Basu Khadka On 12/9/2024 7:38PM

This Linux Hardening Script Will Accomplish The Following

[1]. Delete and add users based off of readme link
[2]. UFW settings
[3]. Find and delete forbidden media files
[4]. Try to find a list of common "hacking" tools
[5]. Fix insecure permissions on shadow file
[6].
[7].
[8].
[9].
[10].


'''


# =============== Functions ===============

def get_readme_text(url: str):
    response = requests.get(url)

    # Retrieving the html text from the cyberpatriots website
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text()
    else:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")


def strip_all_items_in_list(targetList: list):
    for i in range(len(targetList)):
        targetList[i] = targetList[i].strip()


def return_code(command, passed, failed):
    if command.returncode == 0:
        print("-"*20)
        print(passed)
        print("-"*20)
    else:
        print("!"*20)
        print(failed)
        print("!"*20)
# =========================================


# =============== User Adding And Deleting ===============

whoami = 'perry'
# whoami = subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout
whoami.strip()

# getting text, getting authorized users, and cleaning data
readMeText = get_readme_text('https://www.uscyberpatriot.org/Pages/Readme/cp17_tr2_m_ubu22_readme_jsgrxe68wc.aspx')  # !!!!!!!!!! CHANGE THE URL !!!!!!!!!!
authorizedUsers = readMeText[readMeText.find(whoami):readMeText.find('Competition Guidelines')]
authorizedUsers = authorizedUsers.splitlines()

# cleaning data
authorizedUsers = [item for item in authorizedUsers if 'password' not in item and item != '' and item != 'Authorized Users:']
authorizedUsers.pop(0)
strip_all_items_in_list(authorizedUsers)

# getting list of all users on computer
allUsers = subprocess.run('ls /home', shell=True, capture_output=True, text=True).stdout.splitlines()
strip_all_items_in_list(allUsers)

# converting lists to set
authorizedUsers = set(authorizedUsers)
allUsers = set(allUsers)

# users to remove and those to add
usersToRemove = allUsers.difference(authorizedUsers)
usersToAdd = authorizedUsers.difference(allUsers)

# Actually Deleting And Adding Users

# Adding Users
print(f'\033[1;32;5mFound {len(usersToAdd)} Users To Add\033[0m')
for i in usersToAdd:
    ans = input(f'Would You Like To Add User {i} (y/n)?').lower()
    while ans not in ['y', 'n']:
        ans = input(f'WOULD YOU LIKE TO DELETE {i}?').lower()
    if ans == 'y':
        cmd = 'sudo adduser ' + i
        addingUser = subprocess.run(cmd, shell=True)
        return_code(addingUser, f'\033[1;32mSuccessfully Added User {i}\033[0m', f'\033[1;91mERROR: COULD NOT ADD USER {i}\033[0m')
    else:
        print(f'\033[1;91mDID NOT ADD USER {i}\033[0m')

# SAFE GUARD TO MAKE SURE YOU DO NOT DELETE YOUR SELF
usersToRemove.discard(whoami)
#####################################################

# deleting users
print(f'\033[1;91mFOUND {len(usersToAdd)} USERS THAT NEED TO BE DELETED\033[0m')
for i in usersToRemove:
    ans = input(f'WOULD YOU LIKE TO DELETE {i}?').lower()
    while ans not in ['y', 'n']:
        ans = input(f'WOULD YOU LIKE TO DELETE {i}?').lower()
    if ans == 'y':
        cmd = f'sudo deluser {i} --remove-home'
        deletingUser = subprocess.run(cmd, shell=True)
        return_code(deletingUser, f'\033[32mSuccessfully \033[1;91mDELETED\033[0;32m User {i}\033[0m', f'\033[1;91mERROR: COULD NOT ADD USER {i}\033[0m')
    else:
        print(f'\033[1;32mDID NOT DELETE USER {i}')



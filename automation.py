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


def get_prohibited_files(rmv:bool):
    files = subprocess.run("sudo find /home \( -iname '*.mp3' -o -iname '*.mp4' -o -iname '*.mov' -o -iname '*.wav' \)",shell=True,capture_output=True,text=True)
    
    if(not rmv):
        return files.stdout
    if(rmv):
        deletedFiles=subprocess.run("sudo find home \( -iname '*.mp3' -o -iname '*.mp4' -o -iname '*.mov' -o -iname '*.wav' \) -exec rm {} + >/dev/null",shell=True)
        returnCode(deletedFiles,"Succesfully Deleted Files","FAILED to delete files")
# =========================================


# =============== User Adding And Deleting ===============

#whoami = 'perry'
thisIsWhoYouAre = subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout
thisIsWhoYouAre = thisIsWhoYouAre.strip()

# getting text, getting authorized users, and cleaning data
readMeText = get_readme_text('https://www.uscyberpatriot.org/Pages/Readme/cp17_tr2_m_ubu22_readme_jsgrxe68wc.aspx')  # !!!!!!!!!! CHANGE THE URL !!!!!!!!!!
authorizedUsers = readMeText[readMeText.find(thisIsWhoYouAre):readMeText.find('Competition Guidelines')]
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
        ans = input(f'WOULD YOU LIKE TO ADD {i}?').lower()
    if ans == 'y':
        cmd = f"sudo adduser --disabled-password --gecos '' {i}"# --gecos sets all the room number thing to '' 
        addingUser = subprocess.run(cmd, shell=True, check=True)
        return_code(addingUser,f'\033[1;32mSuccessfully Added User {i}\033[0m',f'\033[1;91mERROR: COULD NOT ADD USER {i}\033[0m')
        cmd = f"echo '{i}:Cy|)3R!)^TR!0T$' | sudo chpasswd"
        settingPasswd = subprocess.run(cmd, shell=True, check=True)
        return_code(settingPasswd, f'\033[1;32mSuccessfully Added Password For User {i}\033[0m', f'\033[1;91mERROR: COULD NOT ADD PASSWORD FOR USER {i}\033[0m')
    else:
        print(f'\033[1;91mDID NOT ADD USER {i}\033[0m')

# SAFE GUARD TO MAKE SURE YOU DO NOT DELETE YOUR SELF
usersToRemove.discard(thisIsWhoYouAre)
#####################################################

# deleting users
print(f'\033[1;91;5mFOUND {len(usersToRemove)} USERS THAT NEED TO BE DELETED\033[0m')
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


# =============== UFW Config ===============
print('\033[32mUFW DEFAULT DENY INCOMING\033[0m')
defaultDenyIncoming = subprocess.run('sudo ufw default deny incoming', shell=True)
return_code(defaultDenyIncoming, 'SUCCESFULY SET UFW INCOMING TO DENY','ERROR:COULD NOT SET DEFAULT INCOMING TO DENY')

print('\033[1;32mUFW DEFAULT ALLOW OUTGOING\033[0m')
defaultAllowOutgoing = subprocess.run('sudo ufw default allow outgoing', shell=True)
return_code(defaultAllowOutgoing, 'SUCCESFULLY SET UFW OUTGOING TO ALLOW', 'ERROR: COULD NOT SET DEFAULT OUTGOING TO ALLOW')

print('\033[1;32mUFW ENABLE\033[0m')
enableUFW = subprocess.run('sudo ufw enable', shell=True)
return_code(enableUFW, 'SUCCESFULLY ENABLED UFW', 'ERROR: COULD NOT SUCCESFULLY ENBLE UFW')

# =============== Finding Media Files ===============
prohibitedFiles = get_prohibited_files(False)
print(f'FOUND THESE PROHIBITED FILES: {prohibitedFiles}')
if(prohibitedFiles != ''):
    delete = input('Delete Prohibited Files (y/n)?').lower()
    while delete not in ['y','n']:
        delete = input('Delete Prohibited Files (y/n)?').lower()
    if(delete == 'y'):
        get_prohibited_files(True)
        return_code(get_prohibited_files,'\033[1;32mDELETED THE PROHIBITED FILES\033[0m','\033[1;91mERROR:COULD NOT DELETE THOSE FILES\033[0m')
    else:
        print('\033[1;32mDID NOT DELETE THOSE FILES\033[0m;')
else:
    print('\033[1;32mNo Prohibited Files Found\033[0m')

# =============== Insecure Permissions On Shadow File ==================
InsecurePermissions = subprocess.run('sudo chmod 640 /etc/shadow', shell=True)
return_code(InsecurePermissions, '\033[1;32mSUCCESFULLY SET PERMISSION ON SHADOW FILE\033[0m', '\033[1;91mERROR: COULD NOT SET PERMISSION ON SHADOW FLIE\033[0m')

# =============== Disabling IPv4 Port Forwarding
NewLine = "net.ipv4.ip_forward=0"
cmd = f"sudo sed -i '/net.ipv4.ip_forward=/c\{NewLine}' /etc/sysctl.conf"
disableIPv4Forwarding = subprocess.run(cmd,shell=True)
return_code(disableIPv4Forwarding,'\033[1;32mSUCCESFULLY DISABLED IPv4 FORWARDING\033[0m','\033[1;91mERROR:COULD NOT SUCCESFULLY DISABLE IPv4 PORT FORWARDING\033[0m')

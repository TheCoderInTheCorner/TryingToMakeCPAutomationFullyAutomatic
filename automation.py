import subprocess
from bs4 import BeautifulSoup
import requests

'''
Created By Basu Khadka On 12/9/2024 7:38PM

This Linux Hardening Script Will Accomplish The Following

[1]. Delete and add users based off of readme link
[2]. UFW settings
[3]. Find and delete forbidden media files
[4]. !!!STILL WORKING ON!!!: Try to find a list of common "hacking" tools
[5]. Fix insecure permissions on shadow file
[6]. Makes Machine Remember Last 5 Passwords
[7]. Min and Max Passwd age
[8]. Promoting and Demoting Admins
[9]. Actually makes all users have a max and min password len
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


# =============== Warnings and Checks ==================
print("\033[1;33m===================== !IMPORTANT! =====================\033[0m")

print("\033[1;91m!!!Here are some things to consider before running this script!!!\033[0m")
print("1. In the readme, your name is the first name in authorized users\n\033[1;91m2. MAKE SURE YOU CHANGE THE README URL\033[0m\n3. DONT DO SUDO PYTHON ./AUTOMATION.PY JUST DO PYTHON ./AUTOMATION.PY\n")

print("\033[1;33m=====================================================\033[0m")


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

# =============== Disabling IPv4 Port Forwarding =================
NewLine = "net.ipv4.ip_forward=0"
cmd = f"sudo sed -i '/net.ipv4.ip_forward=/c\{NewLine}' /etc/sysctl.conf"
disableIPv4Forwarding = subprocess.run(cmd,shell=True)
return_code(disableIPv4Forwarding,'\033[1;32mSUCCESFULLY DISABLED IPv4 FORWARDING\033[0m','\033[1;91mERROR:COULD NOT SUCCESFULLY DISABLE IPv4 PORT FORWARDING\033[0m')

# =============== PAM Files ==================
cmd = "sudo sed -i '/PASS_MAX_DAYS/c\PASS_MAX_DAYS   90' /etc/login.defs"
SetMaxAge = subprocess.run(cmd,shell=True)
return_code(SetMaxAge,"\033[1;32mSUCCESFULLY SET MAX PASSWD AGE\033[0m","\033[1;91mERROR:COULD NOT SUCCESFULLY SET MAX PASSWD AGE\033[0m")

cmd = "sudo sed -i '/PASS_MIN_DAYS/c\PASS_MIN_DAYS   7' /etc/login.defs"
SetMinAge = subprocess.run(cmd,shell=True)
return_code(SetMinAge,"\033[1;32mSUCCESFULLY SET MIN PASSWD AGE\033[0m","\033[1;91mERROR:COULD NOT SUCCESFULLY SET MIN PASSWD AGE\033[0m")

extra = "1"
cmd = f"sudo sed -i '/pam_unix.so/s/\(pam_unix.so\)/\{extra} remember=5/' /etc/pam.d/common-password"
SetR5 = input('\033[1;32mSet remember to 5 (y/n)?\033[0m').lower()
while SetR5 not in ['y','n']:
    SetR5 = input('\033[1;32mSet remember to 5 (y/n)?\033[0m').lower()

if(SetR5 == 'y'):
    SetRememberToFive = subprocess.run(cmd,shell=True)
    return_code(SetRememberToFive,"\033[1;32mSUCCESFULLY SET REMEMBER TO 5\033[0m","\033[1;91mERROR:COULD NOT SUCCESFULLY SET REMEMBER TO 5\033[0m")
else:
    print('\033[1;91mDID NOT SET REMEMBER TO 5\033[0m')

# =============== Admin Privelages ==================

# Getting List Of Authorized Admin

authorizedAdmin = readMeText[readMeText.find(thisIsWhoYouAre):readMeText.find('Authorized Users')]
authorizedAdmin = authorizedAdmin.splitlines()

# cleaning data
authorizedAdmin = [item for item in authorizedAdmin if 'password' not in item and item != '' and item != 'Authorized Users:']
authorizedAdmin[authorizedAdmin.index(f'{thisIsWhoYouAre} (you)')] = thisIsWhoYouAre
strip_all_items_in_list(authorizedAdmin)

# Getting List Of All Admin
allAdmins = subprocess.run('getent group sudo | cut -d: -f4',shell=True,capture_output=True,text=True).stdout
allAdmins = allAdmins.split(',')
strip_all_items_in_list(allAdmins)

# Promotions and demotions
allAdmins = set(allAdmins)
authorizedAdmin = set(authorizedAdmin)

promote = authorizedAdmin.difference(allAdmins)
demote = allAdmins.difference(authorizedAdmin)

print(f"\033[1;32;5mFOUND {len(promote)} USERS TO PROMOTE TO ADMIN PRIVELAGE\033[0m")

# Promoting Users
for i in promote:
    promoteOrNo = input(f'\033[1;32mDO YOU WANT TO PROMOTE USER {i} TO ADMIN PRIVELAGE (y/n)?\033[0m').lower()
    while promoteOrNo not in ['y','n']:
        promoteOrNo = input(f'\033[1;32mDO YOU WANT TO PROMOTE USER {i} TO ADMIN PRIVELAGE (y/n)?\033[0m').lower()
    if(promoteOrNo == 'y'):
        promoteUser = subprocess.run(f'sudo usermod -aG sudo {i}', shell=True)
        return_code(promoteUser,f'\033[1;32mSUCCESFULLY PROMOTED USER {i} TO ADMIN PRIVELAGES\033[0m',f'\033[1;91mERROR COULD NOT PROMOTE USER {i} TO ADMIN PRIVELAGES\033[0m')
    else:
        print(f"\033[1;91mDID NOT PROMOTE USER {i} TO ADMIN PRIVELAGES\033[0m")

# Demoting Users
for i in demote:
    demoteOrNo = input(f'\033[1;91mDO YOU WANT TO DEMOTE USER {i} FROM ADMIN PRIVELAGES (y/n)?\033[0m').lower()
    while demoteOrNo not in ['y','n']:
        demoteOrNo = input(f'\033[1;91mDO YOU WANT TO DEMOTE USER {i} FROM ADMIN PRIVELAGES (y/n)?\033[0m').lower()
    if(demoteOrNo == 'y'):
        demoteUser = subprocess.run(f'sudo deluser {i} sudo', shell=True)
        return_code(demoteUser,f'\033[1;91mSUCCESFULLY DEMOTED USER {i} FROM ADMIN PRIVELAGES\033[0m',f'\033[1;91mERROR COULD NOT DEMOTE USER {i} FROM ADMIN PRIVELAGES\033[0m')
    else:
        print(f'\033[1;32mDID NOT DEMOTE USER {i}\033[0m')

# =============== Enforcing Max and Min Password Days ==================
allUsers = subprocess.run('ls /home', shell=True, capture_output=True, text=True).stdout.splitlines()
strip_all_items_in_list(allUsers)

for i in allUsers:
    cmd = f"sudo chage -M 90 {i}"
    setMax = subprocess.run(cmd,shell=True)
    return_code(setMax,f"\033[1;32mSUCCCESFULLY SET MAX PASSWORD LENGTH FOR USER {i}\033[0m;",f"\033[1;32mCOULD NOT SUCCESFULLY SET MAX PASSWD FOR USER {i}\033[0m")    
    cmd = f"sudo chage -m 7 {i}"
    setMax = subprocess.run(cmd,shell=True)
    return_code(setMax,f"\033[1;32mSUCCCESFULLY SET MIN PASSWORD LENGTH FOR USER {i}\033[0m;",f"\033[1;32mCOULD NOT SUCCESFULLY SET MIN PASSWD FOR USER {i}\033[0m")


# %%
# IMPORT SECTION
import json, getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException

# %%
# INTO PRINT
print(open('data/paint.txt', 'r', encoding='utf8').read())
print('\n=============')
print('by: Affan Kasemsan')
print('GitHub: https://github.com/GoRyuuO')
print('Source: https://github.com/GoRyuuO/psu-auto-evaluate.git\n')

# %%
# LOAD CONFIG
def config_load():
    global EDGE_PATH, SITE, HEADLESS, DEFAULT_POINT, LANGUAGE
    with open('data/eva-config.json', 'r') as fp:
        config = json.load(fp)
    EDGE_PATH = config['edge-webdriver']
    SITE = config['evaluate-site']
    HEADLESS = bool(config['headless-mode'])
    DEFAULT_POINT = config['default-score'] # Max = 4, Min = 1
    LANGUAGE = config['language']
    if DEFAULT_POINT not in range(1,5): raise ValueError('Wrong score range score must be between 1 and 4')
config_load()

# %%
# Webdriver Load
headless = Options()
headless.headless = HEADLESS
headless.add_argument("--log-level=3")

try:
    driver = webdriver.Edge(EDGE_PATH, options=headless)
except:
    print('"msedgedriver.exe" file is missing.')
    print('and be sure MSEdge is installed in your PC.')

# %%
# FUNCTION DEFINED
def get_account():
    global USER, PSWD 
    print('\n=====Enter PSU Passport=====')
    USER = input('Username: ')
    PSWD = getpass.getpass('Password: ')
    print('=============================\n')

def login(USER, PASSWORD):
    try:
        driver.get(SITE)
        driver.find_element(By.ID, 'username').send_keys(USER)
        driver.find_element(By.ID, 'password').send_keys(PASSWORD)
        driver.find_element(By.NAME, 'submit').click()
        driver.find_element(By.NAME, 'Submit').click()
        return True
    except UnexpectedAlertPresentException:
        print('Please input correct password/You can not use this system', end='')
        return False

def get_state():
    """Get state:bool to check is that login before.

    Returns: bool
    """
    try:
        driver.find_element(By.ID, 'username')
        print("Login first.")
        return False
    except NoSuchElementException:
        return True

def get_user_semester(state:bool):
    if state == False: return
    info = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/center/table/tbody/tr/td/table/tbody/tr[1]/td[2]')
    print('\n==================')
    print('User:', USER)
    print('Semester:', '-'.join([x for x in [info.text.split(' ')[1], info.text.split(' ')[3]]]))
    print('==================\n')

def get_current_staff_eva(state:bool):
    if state == False: return
    current_eva = driver.find_element(By.CSS_SELECTOR, 'body > table > tbody > tr:nth-child(2) > td > center > table > tbody > tr > td > table > tbody > tr:nth-child(6) > td > table > tbody > tr:nth-child(3)').text.split('\n')
    subject = 'วิชา: (' + ') '.join([current_eva[0], current_eva[1].split(' ')[0]])
    name = ' '.join(current_eva[1].split(' ')[1:])
    print(subject, name, sep='\nอาจารย์ผู้สอน: ')
    print('img: ' + driver.find_element(By.CSS_SELECTOR, 'div > img').get_attribute('src'))
    print('==================')

def start_evalute(state:bool):
    """Start auto evaluate teachers

    Args:
        state (bool): Check that you are login before.
    """
    if state == False: return
    for i in range(0,8):
        driver.find_element(By.NAME, f'ra_scale{i}').click()
    driver.find_element(By.ID, 'frmEva').submit()
    
    alrt = Alert(driver)
    print(alrt.text)
    alrt.accept()

def auto_evaluate():
    eva_btn = driver.find_elements(By.TAG_NAME, 'a')
    while eva_btn[9].text == 'เริ่มประเมิน':
        get_current_staff_eva(get_state())
        eva_btn[9].click()
        start_evalute(get_state())
        eva_btn = driver.find_elements(By.TAG_NAME, 'a')
    else: 
        print('==================')
        print('All done.')
        print('==================\n')
        driver.quit()

# %%
# LOGIN AND [ GET USER SEMESTER ] [ 3 TRY | Cancel by ESC ]
count = 0
while count <3:
    get_account()
    if login(USER,PSWD):
        get_user_semester(get_state())
        break
    else:
        count+=1
        print(' | ('+ str(3-count) +' time left)')
    if USER == '' and PSWD == '':
        print('Cancel by user')
        break


# %%
# AUTO EVALUATE AND MAIN PROGRAM
auto_evaluate()

exit(1)



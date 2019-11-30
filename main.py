import datetime
import threading
import time

from selenium import webdriver
from termcolor import cprint
import warnings

from CenterPack import CenterPack
from RequestThread import RequestThread

warnings.filterwarnings("ignore")

tabs_number = 1
cycle_time = 4   #secs, ineger only

print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_yellow = lambda x: cprint(x, 'yellow')
print_blue = lambda x: cprint(x, 'blue')

center_pack = CenterPack()
center_pack.set_cycle_time(cycle_time)

def login(browser):
    form = browser.find_element_by_id("new_student")
    if form == None:
        print_red("form not found! may be page address was changed!")

    try:
        usernameInput = browser.find_element_by_id("student_student_identifier")
        passwordInput = browser.find_element_by_id("student_password")
    except:
        print_red('incorrect page')
        return False
    while (True):
        try:
            print_blue('student id:')
            id = int(input())
            usernameInput.clear()
            usernameInput.send_keys(id)
            print_blue('password:')
            password = input()
            passwordInput.clear()
            passwordInput.send_keys(password)

        except:
            print_red('incorrect characters...')
            continue

        form.submit()

        try:
            form = browser.find_element_by_id("new_student")
            usernameInput = browser.find_element_by_id("student_student_identifier")
            passwordInput = browser.find_element_by_id("student_password")
            print_red('incorrect id or password')
        except:
            center_pack.set_user_and_pass_and_cycle_time(id, password)
            print_green('\n\nlogin successfully!')
            return True


print_yellow('connecting...')

options = webdriver.ChromeOptions()
options.add_argument("headless")

try:
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
except:
    print_red('selenium not installed!')

try:
    driver.get('https://sso.stu.sharif.ir/students/sign_in')
except:
    print_red('no connection!')

print_green('connected!')

if (not login(driver)):
    print_red('system not response ;)')
    exit()

driver.close()

threads = []

for i in range(tabs_number):
    thread = RequestThread(center_pack)
    thread.set_timing_options(cycle_time, i * cycle_time / tabs_number)
    threads.append(thread)
    thread.start()

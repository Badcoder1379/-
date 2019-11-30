import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

import CenterPack


class RequestThread(threading.Thread):
    def __init__(self, center_pack: CenterPack):
        threading.Thread.__init__(self)
        self.center_pack = center_pack
        self.username = center_pack.get_username()
        self.password = center_pack.get_password()
        self.requesting = False
        self.cycle_time = None
        self.special_time = None

        options = webdriver.ChromeOptions()
        # options.add_argument("headless")

        self.driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

    def go_to_dining_page(self):
        self.driver.get('https://sso.stu.sharif.ir/students/sign_in')

    def run(self):
        self.go_to_buy_page()
        self.login()
        self.go_to_buy_page()
        self.start_requesting()

    def login(self):
        form = self.driver.find_element_by_id("new_student")

        username_input = self.driver.find_element_by_id("student_student_identifier")
        password_input = self.driver.find_element_by_id("student_password")

        username_input.clear()
        username_input.send_keys(self.username)

        password_input.clear()
        password_input.send_keys(self.password)

        form.submit()

    def go_to_buy_page(self):
        self.driver.get('https://dining.sharif.ir/admin/food/food-reserve/reserve')
        self.driver.get('https://dining.sharif.ir/admin/food/food-reserve/reserve')

    def get_time_now(self):
        t = time.time()
        correct = int(t)
        t -= correct
        correct = correct % self.center_pack.get_cycle_time()
        t = t + correct
        return t

    def get_time_to_wait(self):
        now = self.get_time_now()
        if now < self.special_time:
            return self.special_time - now
        else:
            return (self.center_pack.get_cycle_time() - now) + self.special_time

    def set_timing_options(self, cycle_time, special_time):
        self.special_time = special_time
        self.cycle_time = cycle_time

    def start_requesting(self):
        self.requesting = True

        while (self.requesting):

            try:
                spans1 = self.driver.find_elements_by_class_name('fa-cutlery')
                spans2 = self.driver.find_elements_by_class_name('cursor_pointer')
                spans3 = self.driver.find_elements_by_class_name('has_tooltip')

                common_list = []
                for span in spans1:
                    if spans2.__contains__(span):
                        common_list.append(span)
                for span in common_list:
                    if not spans3.__contains__(span):
                        common_list.remove(span)

                if len(common_list) > 0:
                    self.center_pack.success_buy()
                else:
                    raise Exception('not find span')

                for buy_span in common_list:
                    buy_span.click()

            except:
                now = self.get_time_from_site()
                self.center_pack.not_successs_requeset(now)

                wait_time = self.get_time_to_wait()
                time.sleep(wait_time)

                self.driver.get('https://dining.sharif.ir/admin/food/food-reserve/reserve')

            self.requesting = self.center_pack.get_requesting()
        self.driver.close()

    def get_time_from_site(self):

        hourDiv = self.driver.find_element_by_id('hours')
        secDiv = self.driver.find_element_by_id('min')
        minDiv = self.driver.find_element_by_id('min')

        return (hourDiv.text + ':' + minDiv.text + ':' + secDiv.text)

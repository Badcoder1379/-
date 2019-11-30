import threading
import time

from termcolor import cprint

print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_yellow = lambda x: cprint(x, 'yellow')
print_blue = lambda x: cprint(x, 'blue')


class CenterPack:
    def __int__(self):
        self.lock = None
        self.username = None
        self.password = None
        self.requesting = None
        self.cycle_time = None

    def set_user_and_pass_and_cycle_time(self, username, password):
        self.username = username
        self.password = password
        self.requesting = True
        self.lock = threading.Lock()

    def set_cycle_time(self, cycle_time):
        self.cycle_time = cycle_time

    def get_cycle_time(self):
        return self.cycle_time

    def success_buy(self):
        print_green('---------------------------')
        print_green('day buy was successfully...')
        print_green('congratulations')
        print_green('---------------------------')
        with self.lock:
            self.requesting = False

    def not_successs_requeset(self, time):
        print_red('not success request at ' + time + ' in dining, main time: ' + str(self.get_time_now()))
        print_red('--------------------------------------------------------------------------------------')

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_requesting(self):
        with self.lock:
            return self.requesting

    def finish_requesting(self):

        self.requesting = False
        print_green('finish requesting ...')


    def get_time_now(self):
        t = time.time()
        correct = int(t)
        t -= correct
        correct = correct % 1000
        t = t + correct
        return t


import numpy as np
from collections import deque
import matplotlib.pyplot as plt

def time_generator(mean_val):
    return np.random.exponential(mean_val)

def time_gene(base, sig):
    if(sig == 0):
        temp = []
        current = 0
        for i in range(30):
            new_val = time_generator(base)
            temp.append(current+ new_val)
            current = current+ new_val
    else:
        temp = []
        for i in range(30):
            new_val = time_generator(base)
            temp.append(new_val)
    return temp

arrival_time = time_gene(6.0, 0)
service_time = time_gene(9.0, 1)


class market_queue_problem:
    def __init__(self, arrival_time, service_time):
        self.delay_list = deque()
        self.current_service = deque()
        self.complete_time = []
        self.delay_time = []
        self.wait_time = []
        self.wait = 0
        self.clock = 0
        self.window_count = 0
        self.idel_window = 0
        self.i = 0

    def compute_wait(self):
        arr = arrival_time[self.i]
        sev = service_time[self.i]
        if (self.i == 0):
            delay = 0
            begin = arr
        else:
            if (arr < self.complete_time[self.i - 1]):
                delay = self.complete_time[self.i - 1] - arr
                begin = arr + delay
            else:
                delay = 0
                begin = arr

        complete = arr + sev + delay
        wait = sev + delay

        self.complete_time.append(complete)
        self.delay_time.append(delay)
        self.wait_time.append(wait)

        return [arr, delay, begin, sev, wait, complete]

    def check_new_arrival(self):
        if (self.clock >= arrival_time[self.i]):
            return True
        else:
            return False

    def check_new_leave(self):
        for cus in self.current_service:
            if (self.clock >= cus[-1]):
                return True
                break
        return False

    def main_fun(self):
        while (self.clock < 9999):
            # idel window count
            if (self.window_count > len(self.current_service)):
                self.idel_window = self.window_count - len(self.current_service)
            else:
                self.idel_window = 0
            if(self.i<30):
                new_arr = self.check_new_arrival()
            if (new_arr):
                cust = self.compute_wait()
                self.delay_list.appendleft(cust)
                while (self.idel_window != 0):
                    if (len(self.delay_list) != 0):
                        self.idel_window = self.idel_window - 1
                        self.current_service.appendleft(self.delay_list[0])
                        self.delay_list.pop()
                    else:
                        self.window_count = len(self.current_service)
                        self.idel_window = 0

                if (len(self.delay_list) >= 3):
                    if (self.window_count < 6):
                        self.window_count = self.window_count + 1  # open a new window
                        self.current_service.appendleft(self.delay_list[0])
                        self.delay_list.pop()
                        print("open a new window")
                else:
                    if (self.window_count == 0):
                        self.window_count = self.window_count + 1
                        self.current_service.appendleft(self.delay_list[0])
                        self.delay_list.pop()

                self.i = self.i + 1
                print("*********************************************************************")
                print("new arrival")
                print("clock:", self.clock, "\n",
                      "customer:", self.i, "\n",
                      "service windows:", self.window_count, ",", "\n",
                      # "number of idle service windows:", self.idel_window, ",", "\n",
                      "current served customer number:", len(self.current_service), ",", "\n",
                      "arrive time, service time, delay time, wait time,ct:", cust[0], cust[3], cust[1], cust[4],
                      cust[5], "\n",
                      "delay list:", len(self.delay_list))
                new_arr = False

            new_lea = self.check_new_leave()
            if (new_lea):
                cust = self.current_service[0]
                self.current_service.pop()
                if (len(self.delay_list) != 0):
                    self.current_service.appendleft(self.delay_list[0])
                    self.delay_list.pop()
                else:
                    print("close a  window")
                    self.idel_window = 0
                    self.window_count = len(self.current_service)
                print("*********************************************************************")
                print("leave")
                print("clock:", self.clock, "\n",
                      "customer:", self.i, "\n",
                      "service windows:", self.window_count, ",", "\n",
                      # "number of idle service windows:", self.idel_window, ",", "\n",
                      "current served customer number:", len(self.current_service), ",", "\n",
                      "arrive time, service time, delay time, wait time,ct:", cust[0], cust[3], cust[1], cust[4],
                      cust[5], "\n",
                      "delay list:", len(self.delay_list))

            self.clock = self.clock + 1
        total_wait = 0
        for ele in self.wait_time:
            total_wait = total_wait + ele
        return total_wait / 30

obj = market_queue_problem(arrival_time, service_time)
ave = obj.main_fun()
print("===================================================================")
print("average wait time is: ", ave)











































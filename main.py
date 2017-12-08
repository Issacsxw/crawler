from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
from crawler_function import *
from get_routes import *
import json
import os
import multiprocessing


def son_processing(start, end):
    while True:
        driver = startSession()
        if driver is not None:
            break
    routes = Routes[start:end]
    while len(routes) != 0:
        for route in routes:
            Basic = SearchRoute_10AM(driver, route[0], route[1])
            if len(Basic) != 0:
                file_name = 'result/'+route[0]+"-"+route[1]+".json"
                with open(file_name, 'w') as f:
                    json.dump(Basic, f)
                routes.remove(route)
                print(len(routes))
    driver.close()


if __name__ == '__main__':
    Routes = GetRoutes(28)
    process = []
    for i in range(5):
        # start,end=0,len(Routes)
        start, end = (i*int(len(Routes)/5), (i+1)*int(len(Routes)/5))
        t = multiprocessing.Process(target=son_processing, args=(start, end))
        process.append(t)
    for i in range(5):
        process[i].start()
    for i in range(5):
        process[i].join()

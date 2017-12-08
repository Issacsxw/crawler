from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display


def startSession() -> webdriver:
    """准备一个driver用于后面的爬虫"""
    url = 'https://www.google.com/maps/'
    display = Display(visible=0,size=(800,600))
    display.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--diasble-gpu')
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--proxy-server=http://127.0.0.1:1080')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:
        # 打开浏览器
        driver.get(url)
        time.sleep(30)
        # 输入框
        locator = (By.ID, 'searchbox-directions')
        WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
        el = driver.find_element_by_id("searchbox-directions")
        el.click()
        # 选择交通工具
        locator = (By.XPATH, '//div[@data-travel_mode=3]')
        WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
        button = driver.find_element_by_xpath('//div[@data-travel_mode=3]')
        button.click()
        # 选择时间
        locator = (By.CLASS_NAME, 'goog-menu-button-inner-box')
        WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
        button = driver.find_element_by_class_name("goog-menu-button-inner-box")
        button.click()
        # 选择离开时间（早十点）
        locator = (By.ID, ':1')
        WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
        button = driver.find_element_by_id(":1")
        button.click()
        locator = (By.NAME, 'transit-time')
        WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
        keyin = driver.find_element_by_name("transit-time")
        keyin.clear()
        keyin.send_keys("10:00 AM")
        return driver
    except:
        print("Error while Start a session")
        return None


def SearchRoute_10AM(driver, start, end) -> list:
    '''
    :driver: 已经准备好的网页驱动
    :param start: 出发地点，字符型
    :param end: 目的地，字符型
    :return: 返回所有线路信息的列表
    '''
    try:
        # 输入起点和终点
        locator = (By.ID, 'directions-searchbox-0')
        WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
        el = driver.find_element_by_id("directions-searchbox-0")
        el = el.find_element_by_class_name("tactile-searchbox-input")
        el.clear()
        el.send_keys(start)
        el = driver.find_element_by_id("directions-searchbox-1")
        el = el.find_element_by_class_name("tactile-searchbox-input")
        el.clear()
        el.send_keys(end)
        el.send_keys(Keys.ENTER)
        time.sleep(2)
        cache = GetInfo(driver)
        if cache == "None":
            Basic = ["None"]
            return Basic
        else:
            Basic, Detail = cache
            for i in range(len(Basic)):
                Basic[i] = Convert2Dic(Basic[i])
                Basic[i]['详情'] = Detail[i]
    except:
        Basic = []
    return Basic


def GetInfo(driver):
    '''
    drive: 传入一个driver，这个driver是选好起止地点，交通方式，出发时间后得到的driver
    return： 得到两个列表，一个包含每条路线的基本信息，一个包含每条路线的详细信息;
    '''
    index = 0
    Basic, Detail = [], []
    while True:
        try:
            driver.find_element_by_class_name("section-directions-error-primary-text")
            return None
        except:
            pass
        action = webdriver.ActionChains(driver)
        try:
            if index == 0:
                #拿基本数据
                locator = (By.XPATH, '//div[@data-trip-index='+str(index)+']')
                WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
                submenu = driver.find_element_by_xpath('//div[@data-trip-index='+str(index)+']')
                Basic.append(submenu.text)
                action.move_to_element(submenu)
                action.click(submenu)
                action.perform()
                locator = (By.CLASS_NAME, 'transit-mode-body')
                WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
                el = driver.find_element_by_class_name("transit-mode-body")
                Detail.append(el.text)
                while True:
                    back = driver.find_element_by_class_name('section-trip-header-back')
                    back.click()
                    index += 1
            else:
                submenu = driver.find_element_by_xpath('//div[@data-trip-index='+str(index)+']')
                action.move_to_element(submenu)
                action.click(submenu)
                action.perform()
                #拿基本数据
                Basic.append(submenu.text)
                action.perform()
                #拿详细数据
                locator = (By.CLASS_NAME, 'transit-mode-body')
                WebDriverWait(driver, 5, 0.5,).until(EC.presence_of_all_elements_located(locator))
                el = driver.find_element_by_class_name("transit-mode-body")
                Detail.append(el.text)
                while True:
                    back = driver.find_element_by_class_name('section-trip-header-back')
                    back.click()
                    index += 1
        except:
            break
    return Basic, Detail


def Convert2Dic(basic_info):
    # 把基本信息放入字典
    basic_info = basic_info.split('\n')
    a_dic = {
        '预计行程时间': 0,
        '行程起止时间': 0,
        '主要经过线路': 0,
        '出发时间和站点': 0,
        '预计花费': 0,
        '步行时常': 0,
        '详情': 0
    }
    a_dic['预计行程时间'] = basic_info[0]
    a_dic['行程起止时间'] = basic_info[1]
    a_dic['主要经过线路'] = basic_info[2]
    a_dic['出发时间和站点'] = basic_info[3]
    a_dic['预计花费'] = basic_info[4].split(' ')[0]
    a_dic['步行时常'] = basic_info[4].split(' ')[1]
    return a_dic


if __name__ == '__main__':
    while True:
        driver = startSession()
        if driver is not None:
            break
    Basic = SearchRoute_10AM(driver, "大阪", "京都")
    print(Basic)

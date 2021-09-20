from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import load_workbook

options = webdriver.ChromeOptions()
#add configuration
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
#options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
options.add_experimental_option('excludeSwitches', ['enable-automation'])


def crawlMainpage(options):
    # create a browser instance
    driver = webdriver.Chrome(options=options)
    for i in range(10):
        driver.get("https://www.tiktok.com/foryou?lang=en")  # refresh
    # open workbook
    path = 'D://cs//python2021//projects//TiktokMainpages.xlsx'
    wb = load_workbook(path)
    ws = wb.active
    time.sleep(10)
    i = 1  # initialize calculator
    while i < 40:
        time.sleep(2)
        print(str(i)+' on the page:')
        try:
            # select span element with class name ‘lazyload-wrapper’
            # con = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']') if use another variable, data would remain the first span element
            name = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[1]//h3[1]").text
        except:
            driver.quit()
            time.sleep(1)
            # create a browser instance
            driver = webdriver.Chrome(options=options)
            for i in range(10):
                driver.get("https://www.tiktok.com/foryou?lang=en")  # refresh several times
            time.sleep(10)
            i = 1  # reinitialize calculator
            print(str(i) + ' on the page:')
            name = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[1]//h3[1]").text
        homepage = 'https://www.tiktok.com/@' + str(name) + '?lang=en'
        try:
            desc = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[2]//strong[1]").text
            if desc[0] == '#':
                des = ''
        except:
            desc = ''
        try:
            tags = driver.find_elements_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[2]//a//strong")  # may have no strong tag
            if len(tags) != 0:
                for j in range(len(tags)):
                    tags[j] = tags[j].text
                    if tags[j][0] != '#':
                        tags[j] = ''
                for t in tags:
                    if len(t) == 0:
                        tags.remove(t)
        except:
            tags = []
        try:
            musicName = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[4]//h4//a//div").text
        except:
            musicName = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[3]//h4//a//div").text
        try:
            videoLink = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[1]//a").get_attribute('href')
        except:
            videoLink = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[4]//div[1]//a").get_attribute('href')
        try:
            likes = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[2]//div[1]//strong").text
        except:
            likes = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[4]//div[2]//div[1]//strong").text
        try:
            comments = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[2]//div[2]//strong").text
        except:
            comments = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[4]//div[2]//div[2]//strong").text
        try:
            forwards = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[2]//div[3]//strong").text
        except:
            forwards = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[4]//div[2]//div[3]//strong").text
        print([name, homepage, desc, tags, musicName, videoLink, likes, comments, forwards])
        ws.append([name, homepage, desc, str(tags), musicName, videoLink, likes, comments, forwards])
        wb.save(path)
        wb.close()
        print('recording complete')
        print('-----------------------------------------------')
        i += 1  # calculator added by 1
        time.sleep(3)
    driver.quit()


crawlMainpage(options)


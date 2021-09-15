from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import load_workbook

options = webdriver.ChromeOptions()
#添加配置，反反爬
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
#options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
options.add_experimental_option('excludeSwitches', ['enable-automation'])


def crawlMainpage(options):
    # 创建窗口实例
    driver = webdriver.Chrome(options=options)
    for i in range(10):
        driver.get("https://www.tiktok.com/foryou?lang=en")  # 访问网页,多刷新几次
    #打开工作表
    path = 'D://cs//python2021//projects//TiktokMainpages.xlsx'
    wb = load_workbook(path)
    ws = wb.active
    time.sleep(10)
    i = 1  #初始化计数器
    while i < 31:   #一页最多刷新出30个视频
        time.sleep(2)
        print(str(i)+' on the page:')
        try:
            # 选取class名为‘lazyload-wrapper’的span元素
            name = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[1]//h3[1]").text
        except:
            driver.quit()
            time.sleep(1)
            # 创建窗口实例
            driver = webdriver.Chrome(options=options)
            for i in range(10):
                driver.get("https://www.tiktok.com/foryou?lang=en")  # 访问网页,多刷新几次得到新的内容
            time.sleep(10)
            i = 1  #重新初始化计数器
            print(str(i) + ' on the page:')
            name = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[1]//h3[1]").text
        homepage = 'https://www.tiktok.com/@' + str(name) + '?lang=en'
        desc = ''
        try:
            desc = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[2]//strong[1]").text
        except:
            desc = ''
        tags = []
        try:
            tags = driver.find_elements_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[2]//a//strong")  #可能没有strong标签
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
            musicName = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']" + '[' + str(i) + ']' + "//div//div//div[3]//h4//a//div").text
        try:
            videoLink = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[1]//a").get_attribute('href')
        except:
            videoLink = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']" + '[' + str(i) + ']' + "//div//div//div[4]//div[1]//a").get_attribute('href')
        try:
            likes = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[2]//div[1]//strong").text
        except:
            likes = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']" + '[' + str(i) + ']' + "//div//div//div[4]//div[2]//div[1]//strong").text
        try:
            comments = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[2]//div[2]//strong").text
        except:
            comments = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']" + '[' + str(i) + ']' + "//div//div//div[4]//div[2]//div[2]//strong").text
        try:
            forwards = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']"+'['+str(i)+']'+"//div//div//div[5]//div[2]//div[3]//strong").text
        except:
            forwards = driver.find_element_by_xpath("//span[@class='lazyload-wrapper']" + '[' + str(i) + ']' + "//div//div//div[4]//div[2]//div[3]//strong").text
        print([name, homepage, desc, tags, musicName, videoLink, likes, comments, forwards])
        ws.append([name, homepage, desc, str(tags), musicName, videoLink, likes, comments, forwards])
        wb.save(path)
        wb.close()
        print('写入完成')
        print('-----------------------------------------------')
        i += 1  #计数器
        time.sleep(3)
    driver.quit()


crawlMainpage(options)


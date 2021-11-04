from selenium import webdriver
import time
from openpyxl import load_workbook


options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])


def nameVideoCrawl(options):
    path = 'D://cs//python2021//projects/tiktokNameVideos.xlsx'
    wb = load_workbook(path)
    ws = wb.active
    driver = webdriver.Chrome(options=options)
    q_l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for q in q_l:
        for i in range(1, 11):
            print('the ' + str(i) + ' user: ')
            try:
                driver.get('https://www.tiktok.com/search/user?lang=en&q=' + str(q))
                time.sleep(3)
                name = driver.find_element_by_xpath("//div[@data-e2e='search-user-container'][" + str(i) + "]//a[2]//p").text
            except:
                driver.get('https://www.tiktok.com/search/user?lang=en&q=' + str(q))
                time.sleep(3)
                '''
                for i in range(3):
                    driver.find_element_by_xpath("//button[@data-e2e='search-load-more']").click()  # load next page
                    time.sleep(5)
                '''
                name = driver.find_element_by_xpath("//div[@data-e2e='search-user-container'][" + str(i) + "]//a[2]//p").text
            homepage = "https://www.tiktok.com/@" + str(name) + "?lang=en"
            driver.get(homepage)
            time.sleep(5)
            profile = driver.find_element_by_xpath("//h2[@class='share-desc mt10']").text
            following = driver.find_element_by_xpath("//strong[@title='Following']").text
            followers = driver.find_element_by_xpath("//strong[@title='Followers']").text
            likes = driver.find_element_by_xpath("//strong[@title='Likes']").text
            videos = []
            for i in range(1, 31):  # the first 50 videos
                try:
                    video = driver.find_element_by_xpath("//main[@class='share-layout-main']//div[" + str(i) +"]//a").get_attribute('href')
                    videos.append(video)
                except:
                    break
            print([name, homepage, profile, following, followers, likes, str(videos)])
            ws.append([name, homepage, profile, following, followers, likes, str(videos)])
            wb.save(path)
            wb.close()
            print('finished writing')
            print('----------------------------------------')
    driver.quit()


nameVideoCrawl(options)
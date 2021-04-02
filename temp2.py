import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import as EC
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup


def getWorkshop():

    # keywords = ['금속공방', '도자공방', '목공방', '가죽공방', '유리공방', '섬유공방', '라탄공방']
    keywords = ['금속공방']

    # 크롬드라이버 옵션 (headless로 할 수 있게)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    # 크롬 드라이버 경로
    chrome_driver_dir = '/Users/jeongjong-yun/Development/chromedriver'
    driver = webdriver.Chrome(chrome_driver_dir)

    driver.get('https://map.naver.com/v5/search/금속공방?c=13956789.8686469,4503058.2103363,5,0,0,0,dh')

    # iframe으로 변경
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="searchIframe"]'))

    time.sleep(1)

    placeContainer = driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul')
    stores = placeContainer.find_elements_by_tag_name('li')

    endElement = stores[-1]

    # 내부 스크롤 아래로 내림
    while True:
        curCount = len(placeContainer.find_elements_by_tag_name('li'))

        print('스크롤 내린다')
        
        driver.execute_script("arguments[0].scrollIntoView(true);", endElement)
        time.sleep(2)
        stores = placeContainer.find_elements_by_tag_name('li')
        endElement = stores[-1]

        if curCount == len(placeContainer.find_elements_by_tag_name('li')):
            break

    
    # 결과 재정의
    stores = placeContainer.find_elements_by_tag_name('li')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    names = soup.find_all('span', class_='_1AjbI')
    numbers = soup.find_all('span', class_='_3ZA0S')

    print(names, numbers)


    time.sleep(100)


if __name__ == '__main__':
    getWorkshop()
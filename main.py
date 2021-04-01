import csv
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from keywords import keywords

def getWorkshop():

    # 크롬드라이버 옵션 (headless로 할 수 있게)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    # 크롬 드라이버 경로
    chrome_driver_dir = '/Users/jeongjong-yun/Development/chromedriver'
    driver = webdriver.Chrome(chrome_driver_dir)

    driver.get('https://map.kakao.com')

    for keyword in keywords:
        searchKeywordInput = driver.find_element_by_id('search.keyword.query')
        searchKeywordInput.clear()
        searchKeywordInput.send_keys(keyword)

        searchSubmit = driver.find_element_by_id('search.keyword.submit')
        searchSubmit.send_keys('\n')

        time.sleep(1)

        try:
            driver.find_element_by_id('info.search.place.more').send_keys('\n')
        except:
            print('더보기 안눌림')

        time.sleep(1)

        pageContainer = driver.find_element_by_id('info.search.page')
        pages = pageContainer.find_elements_by_tag_name('a')

        time.sleep(1)

        resultElements = []

        print('페이지 수 : ', len(pages))
        # csv 생성
        f = open(keyword+'.csv', 'w', encoding='utf-8')
        wr = csv.writer(f)

        storeDict = {
                    '공방이름': '',
                    '평균별점': '',
                    '별점건수': '',
                    '리뷰건수': ',',
                    '주소': '',
                    '지번주소': '',
                    '연락처': '',
                    '홈페이지': '',
                }

        wr.writerow(storeDict.keys())

        for pageIndex in range(len(pages)):
            
            pages[pageIndex].send_keys('\n')
            time.sleep(2)

            storeContainer = driver.find_element_by_id('info.search.place.list')
            stores = storeContainer.find_elements_by_tag_name('li')

            print(pageIndex+1, '페이지 상점 크롤링 완료')

            for store in stores:

                storeInfo = store.text.split('\n')
                
                try:
                    storeInfo.remove('즐겨찾기')
                    storeInfo.remove('로드뷰')
                    storeInfo.remove('상세보기')
                    storeInfo.remove('홈페이지')
                    storeInfo.remove('영업중')
                except:
                    pass
                print(storeInfo)
                try:
                    storeDict['공방이름'] = storeInfo[0][2:len(storeInfo[0])-6]
                    storeDict['평균별점'] = storeInfo[1]
                    storeDict['별점건수'] = storeInfo[2]
                    storeDict['리뷰건수'] = storeInfo[3]
                    storeDict['주소'] = storeInfo[4]
                except:
                    continue

                try:
                    if storeInfo[5][0:4] == '(지번)':
                        storeDict['지번주소'] = storeInfo[5]
                except:
                    storeDict['지번주소'] = ''
                try:
                    if str(storeInfo[5]).find('-') != -1 and str(storeInfo[5][0]) == '0':
                        storeDict['연락처'] = storeInfo[5]
                except:
                    pass

                try:
                    if str(storeInfo[6]).find('-') != -1 and str(storeInfo[6][0]) == '0':
                        storeDict['연락처'] = storeInfo[6]
                except:
                    storeDict['연락처'] = '연락처 없음'

                homepage = ''
                try:
                    homepage = store.find_element_by_class_name('homepage').get_attribute('href')
                    if homepage == 'https://map.kakao.com/#none':
                        storeDict['홈페이지'] = ''
                    else:
                        storeDict['홈페이지'] = homepage
                except:
                    pass
                
                wr.writerow(storeDict.values())

            if pageIndex == len(pages):
                try:
                    nextBtn = driver.find_element_by_id('info.search.page.next')
                    nextBtn.click()
                    pageIndex = 0
                    pages = pageContainer.find_elements_by_tag_name('a')
                except:
                    print('오류')


            f.close()
    driver.quit()


if __name__ == '__main__':
    getWorkshop()
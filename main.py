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

    # url이동
    driver.get('https://map.kakao.com')

    # 키워드 개수만큼 반복
    for keyword in keywords:
        # 검색 창에 키워드 넣고 검색 버튼 누르기
        searchKeywordInput = driver.find_element_by_id('search.keyword.query')
        searchKeywordInput.clear()
        searchKeywordInput.send_keys(keyword)

        searchSubmit = driver.find_element_by_id('search.keyword.submit')
        searchSubmit.send_keys('\n')
        # 간단한 프로젝트라서 time.sleep()으로 대기함
        time.sleep(1)

        # 이상한 팝업창 있어서 제거, 없다면 넘어감
        try:
            fuckPopup = driver.find_element_by_class_name('layer_body')
            fuckPopup.click()
        except:
            pass

        time.sleep(1)
        
        # 인기도 순으로 정렬하기 위해 element찾아서 누르기

        try:
            sortList = driver.find_element_by_id('info.search.place.sort')
            popLi = sortList.find_elements_by_tag_name('li')[1]
            popBtn = popLi.find_elements_by_tag_name('a')[0]
            popBtn.send_keys('\n')
        except:
            continue

        time.sleep(1)

        # 인기도 순으로 정렬하면 장소 더 보기 버튼이 없을 수도 있기 때문에 없다면 pass
        try:
            driver.find_element_by_id('info.search.place.more').send_keys('\n')
        except:
            print('더보기 안눌림')

        time.sleep(1)

        # csv 생성
        f = open(keyword+'.csv', 'w', encoding='utf-8')
        wr = csv.writer(f)

        # store에 들어갈 정보들 딕셔너리 정의
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

        # dictionary 정보들 csv header로 생성
        wr.writerow(storeDict.keys())

        pageContainer = driver.find_element_by_id('info.search.page')
        pages = pageContainer.find_elements_by_tag_name('a')
        
        # 페이지 하나인 키워드 체크
        if pageContainer.get_attribute('class') != 'pages':
            # 장소가 없는 키워드 체크
            try:
                storeContainer = driver.find_element_by_id('info.search.place.list')
                stores = storeContainer.find_elements_by_tag_name('li')
            except:
                continue

            storeContainer = driver.find_element_by_id('info.search.place.list')
            stores = storeContainer.find_elements_by_tag_name('li')

            len(stores)

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
                
                try:
                    storeDict['공방이름'] = storeInfo[0][2:len(storeInfo[0])-6]
                    storeDict['평균별점'] = storeInfo[1]
                    storeDict['별점건수'] = storeInfo[2]
                    storeDict['리뷰건수'] = storeInfo[3]
                    storeDict['주소'] = storeInfo[4]
                except:
                    continue

                print(storeInfo)

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
            f.close()
            continue
        else:
            # 스토어 개수 정의
            storeCount = 0
            pageIndex = 0
            while True:
                
                if storeCount == 1000:
                    break
                try:
                    pages[pageIndex].send_keys('\n')
                except:
                    break
                time.sleep(1)

                storeContainer = driver.find_element_by_id('info.search.place.list')
                stores = storeContainer.find_elements_by_tag_name('li')

                print('---------------------',pageIndex+1, '페이지 상점 크롤링 완료-----------------------')

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
                    
                    try:
                        storeDict['공방이름'] = storeInfo[0][2:len(storeInfo[0])-6]
                        storeDict['평균별점'] = storeInfo[1]
                        storeDict['별점건수'] = storeInfo[2]
                        storeDict['리뷰건수'] = storeInfo[3]
                        storeDict['주소'] = storeInfo[4]
                    except:
                        continue

                    print(storeInfo)

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
                    
                    storeCount+=1
                    wr.writerow(storeDict.values())

                    if storeCount == 1000:
                        break
                pageIndex+=1
                if pageIndex == len(pages):
                    try:
                        nextBtn = driver.find_element_by_id('info.search.page.next')
                        print(nextBtn.get_attribute('class'))
                        if nextBtn.get_attribute('class') != 'next disabled':
                            nextBtn.click()
                            time.sleep(1)
                            pageIndex = 0
                            pages = pageContainer.find_elements_by_tag_name('a')
                        else:
                            break
                    except:
                        print('오류')


        f.close()
    driver.quit()


if __name__ == '__main__':
    getWorkshop()
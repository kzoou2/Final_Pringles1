import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import re
import json
import pandas as pd


# --크롬창을 숨기고 실행-- driver에 options를 추가해주면된다
options = webdriver.ChromeOptions()
# options.add_argument('headless')

url = 'https://map.naver.com/v5/search'
driver = webdriver.Chrome()  # 드라이버 경로
driver.maximize_window()
# driver = webdriver.Chrome('./chromedriver',chrome_options=options) # 크롬창 숨기기
driver.get(url)
key_word = '제주도 식당'  # 검색어


# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait


# css를 찾을때 까지 10초 대기
time_wait(10, 'div.input_box > input.input_search')

# 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search.send_keys(key_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

res = driver.page_source  # 페이지 소스 가져오기
soup = BeautifulSoup(res, 'html.parser')  # html 파싱하여  가져온다

sleep(1)

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경
    res
    soup

# 페이지 다운
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)

# frame 변경
switch_frame('searchIframe')
page_down(40)
sleep(3)

# 매장 리스트
store_list = driver.find_elements(By.CSS_SELECTOR, 'li.UEzoS')
# 페이지 리스트
next_btn = driver.find_elements(By.CSS_SELECTOR, '.zRM9F > a')

# dictionary 생성
store_dict = []
# 시작시간
start = time.time()
print('[크롤링 시작...]')


# 크롤링 (페이지 리스트 만큼)
for btn in range(len(next_btn))[1:]:  # next_btn[0] = 이전 페이지 버튼 무시 -> [1]부터 시작
    store_list = driver.find_elements(By.CSS_SELECTOR, 'li.UEzoS')
    names = driver.find_elements(By.CSS_SELECTOR, '.TYaxT')  # 장소명
    types = driver.find_elements(By.CSS_SELECTOR, '.KCMnt')  # 장소 유형

    # print(names, types)

    for data in range(len(store_list)):  # 매장 리스트 만큼
        # print(data)
        page = driver.find_elements(By.CSS_SELECTOR, '.TYaxT')
        # print(page)
        # print(page[data])
        print(data)
        page[data].click()
        sleep(3)

        try:
            switch_frame('entryIframe')
            sleep(7)

            store_name = driver.find_element(By.CSS_SELECTOR, '.Fc1rA').text
            store_type = driver.find_element(By.CSS_SELECTOR, '.DJJvD').text
            print(store_name)
            print(store_type)
            
            # 주소 값 초기화
            jibun_addr = ''
            road_addr = ''
            
            # 별점, 리뷰 값 초기화
            out = []
            
            rank_report = 0.0
            review_report = 0
        

            # -----평점-----
#             try:
#                 store_rating_list = driver.find_element(By.CSS_SELECTOR,'.PXMot').text
#                 store_rating = re.sub('별점', '', store_rating_list).replace('\n', '')
#             except:
#                 pass
#             print(store_rating)


            review = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb')
            review_text = review.find_elements(By.TAG_NAME, 'span') # span태그 안에서 별 규칙성을 찾지 못해서 span태그안에 별점, 리뷰 텍스트 정보가 들어가 있기 때문에 span에 있는거 모두 들고오기로 했음.
            
            try:
                for i in review_text:
                    out.append(i.text) # parsing하기 쉽게 배열에 넣어놓음

                print(out)

                if len(out) == 0:
                    pass
                else:
                    if '별점' in out[0]: # 별점이 존재하는 경우
                        rank_report = float(out[0].split('\n')[1].split('/')[0]) # 별점을 실수형으로 바꿔서 담아둔다
                        if len(out) > 3 and '리뷰' in out[3]: # 리뷰가 방문자리뷰, 사용자리뷰 2개가 있는데 방문자, 블로그리뷰가 둘다 있는 경우
                            out[2] = out[2].split(' ')[1].replace(',','') # [방문자리뷰,200] 이런 형태로 있는 데이터를 200만 가져오도록 parsing
                            out[3] = out[3].split(' ')[1].replace(',','') # [블로그리뷰,50] 형태의 데이터를 50만 가져오도록 parsing
                            review_report = int(out[2]) + int(out[3]) # 두 리뷰를 더해준다.
                        else:
                            out[2] = out[2].split(' ')[1].replace(',','') # 방문자리뷰만 있는 경우
                            review_report = int(out[2])
                    else: # 별점이 존재하지 않는 경우
                        if len(out) < 2: # 방문자리뷰만 있는 경우 또는 블로그리뷰만 있는 경우
                            out[0] = out[0].split(' ')[1].replace(',','')
                            review_report = int(out[0])
                        else: # 방문자리뷰, 블로그리뷰 둘다 있는 경우
                            out[0] = out[0].split(' ')[1].replace(',','')
                            out[1] = out[1].split(' ')[1].replace(',','')
                            review_report = int(out[0]) + int(out[1]) # 리뷰 더해준다
                store_rate = rank_report   # 별점이랑 리뷰개수 담아서 return 해준다
            except:
                pass
            
            print(store_rate)
            

            # ------주소(위치)------
#             try:
#                 store_addr = driver.find_element(By.CSS_SELECTOR, '.LDgIH').text
#             except:
#                 pass
            
#             print(store_addr)


            # 주소 클릭
            store_addr_btn = driver.find_element(By.CSS_SELECTOR, '.PkgBl')
#             store_addr_btn.__getitem__(data).click()
            store_addr_btn.click()
            
            # 로딩
            sleep(1)
            
            # 주소 눌렀을 때 도로명, 지번 나오는 div
            addr = driver.find_elements(By.CSS_SELECTOR, '.Y31Sf > div')
#             print(addr)
            
            try:
                # 지번만 있는 경우
                if len(addr) == 1 and addr.__getitem__(0).text[0:2] == '지번':
                    jibun = addr.__getitem__(0).text
                    last_index = jibun.find('복사우\n')  # 복사버튼, 우편번호 제외
                    jibun_addr = jibun[2:last_index]
                    print('지번 주소 :', jibun_addr)

                # 도로명만 있는 경우
                elif len(addr) == 1 and addr.__getitem__(0).text[0:2] == '도로':
                    road = addr.__getitem__(0).text
                    last_index = road.find('복사우\n')  # 복사버튼, 우편번호 제외
                    road_addr = road[3:last_index]
                    print('도로명 주소 :', road_addr)

                # 도로명, 지번 둘 다 있는 경우
                else:
                    # 도로명
                    road = addr.__getitem__(0).text
                    road_addr = road[3:(len(road) -2)]
                    print('도로명 주소 :', road_addr)

                    # 지번
                    jibun = addr.__getitem__(1).text
                    last_index = jibun.find('복사우\n')
                    jibun_addr = jibun[2:last_index]
                    print('지번 주소 :', jibun_addr)
                
            except:
                pass
            

            # -----전화번호 가져오기-----
            try:
                store_tel = driver.find_element(By.CSS_SELECTOR, '.xlx7Q').text
            except:
                pass
            
            print(store_tel)
         

            # ---- list에 데이터 넣기 ----
            list_temp = [store_name, store_type, store_rate, road_addr, jibun_addr, store_tel]
            store_dict.append(list_temp)

            print(f'{store_name}... 완료')

            switch_frame('searchIframe')
            sleep(6)
        except:
            print("error")

    # 다음 페이지 버튼
    if page[-1]:
        next_btn[-1].click()
        sleep(3)
    else:
        print('페이지 인식 못함')
        break

print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을닫는다.

store_dict  # 확인

# 데이터 프레임으로 변환
df = pd.DataFrame(store_dict, columns = ['name','category','rate','road_addr','jibun_addr','tel'])

# csv로 저장
df.to_csv('jeju_restaurant.csv', encoding = 'utf-8', index = False)

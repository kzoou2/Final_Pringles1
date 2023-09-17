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
key_word = '제주도 소품샵'  # 검색어


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
store_list = driver.find_elements(By.CSS_SELECTOR, 'li.VLTHu')  # 키워드 검색 리스트
# 페이지 리스트
next_btn = driver.find_elements(By.CSS_SELECTOR, '.zRM9F > a')  # 페이지 다음 버튼

# dictionary 생성
store_dict = []
# 시작시간
start = time.time()
print('[크롤링 시작...]')

# 크롤링 (페이지 리스트 만큼)
for btn in range(len(next_btn))[1:]:  # next_btn[0] = 이전 페이지 버튼 무시 -> [1]부터 시작
    store_list = driver.find_elements(By.CSS_SELECTOR, 'li.VLTHu')
    names = driver.find_elements(By.CSS_SELECTOR, '.YwYLL')  # 장소명
    types = driver.find_elements(By.CSS_SELECTOR, '.YzBgS')  # 장소 유형

    for data in range(len(store_list)):  # 매장 리스트 만큼
        page = driver.find_elements(By.CSS_SELECTOR, '.YwYLL')  # 위names랑 동일
        print("page: ", btn, "store: ", data)
        page[data].click()
        sleep(4)

        try:
            switch_frame('entryIframe')
            sleep(10)

            store_name = driver.find_element(By.CSS_SELECTOR, '.Fc1rA').text
            store_type = driver.find_element(By.CSS_SELECTOR, '.DJJvD').text
            print(store_name)
            print(store_type)

            # 별점, 리뷰 값 초기화
            out = []

            rank_report = 0.0
            review_report = 0

            # --- 리뷰---

            review = driver.find_element(By.CSS_SELECTOR,
                                         '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb')
            review_text = review.find_elements(By.TAG_NAME,
                                               'span')  # span태그 안에서 별 규칙성을 찾지 못해서 span태그안에 별점, 리뷰 텍스트 정보가 들어가 있기 때문에 span에 있는거 모두 들고오기로 했음.

            try:
                for i in review_text:
                    out.append(i.text)  # parsing하기 쉽게 배열에 넣어놓음

                # print(out)

                if len(out) == 0:
                    pass
                else:
                    if '별점' in out[0]:  # 별점이 존재하는 경우
                        rank_report = float(out[0].split('\n')[1].split('/')[0])  # 별점을 실수형으로 바꿔서 담아둔다
                        if len(out) > 3 and '리뷰' in out[3]:  # 리뷰가 방문자리뷰, 사용자리뷰 2개가 있는데 방문자, 블로그리뷰가 둘다 있는 경우
                            out[2] = out[2].split(' ')[1].replace(',',
                                                                  '')  # [방문자리뷰,200] 이런 형태로 있는 데이터를 200만 가져오도록 parsing
                            out[3] = out[3].split(' ')[1].replace(',', '')  # [블로그리뷰,50] 형태의 데이터를 50만 가져오도록 parsing
                            review_report = int(out[2]) + int(out[3])  # 두 리뷰를 더해준다.
                        else:
                            out[2] = out[2].split(' ')[1].replace(',', '')  # 방문자리뷰만 있는 경우
                            review_report = int(out[2])
                    else:  # 별점이 존재하지 않는 경우
                        if len(out) < 2:  # 방문자리뷰만 있는 경우 또는 블로그리뷰만 있는 경우
                            out[0] = out[0].split(' ')[1].replace(',', '')
                            review_report = int(out[0])
                        else:  # 방문자리뷰, 블로그리뷰 둘다 있는 경우
                            out[0] = out[0].split(' ')[1].replace(',', '')
                            out[1] = out[1].split(' ')[1].replace(',', '')
                            review_report = int(out[0]) + int(out[1])  # 리뷰 더해준다
                store_rate = rank_report  # 별점이랑 리뷰개수 담아서 return 해준다
                store_review = review_report
            except:
                store_rate = []
                store_review = []
                pass

            print("store_rate: ", store_rate)
            print("store_review: ", store_review)

            # ------주소(위치)------

            # 주소 클릭
            store_addr_btn = driver.find_element(By.CSS_SELECTOR, '.PkgBl')
            #             store_addr_btn.__getitem__(data).click()
            store_addr_btn.click()

            # 로딩
            sleep(1)

            # 주소 눌렀을 때 도로명, 지번 나오는 div
            addr = driver.find_elements(By.CSS_SELECTOR, '.Y31Sf > div')
            #             print(addr)

            jibun_addr = []
            road_addr = []
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
                    road_addr = road[3:(len(road) - 2)]
                    print('road_addr :', road_addr)

                    # 지번
                    jibun = addr.__getitem__(1).text
                    last_index = jibun.find('복사우\n')
                    jibun_addr = jibun[2:last_index]
                    print('jibun_addr :', jibun_addr)

            except:
                jibun_addr = []
                road_addr = []
                pass

            # -----전화번호 가져오기-----
            store_tel = ""
            try:
                store_tel = driver.find_element(By.CSS_SELECTOR, '.xlx7Q').text
            except:
                store_tel = ""
                pass

            print('store_tel: ', store_tel)

            # # ----- 이용권 가격 -----
            # prices = []
            #
            # try:
            #     price_list = driver.find_element(By.CSS_SELECTOR,
            #                                      '#app-root > div > div > div > div > div > div.place_section.vKA6F > div.place_section_content > div.PIbes > div.O8qbU.tXI2c > div.vV_z_ >ul.Jp8E6.a0hWz')
            #     price = price_list.find_elements(By.CSS_SELECTOR, 'li > div > div.CLSES')
            #
            #     for i in price:
            #         prices.append(i.text)
            #     print('prices: ', prices)
            #
            # except:
            #     prices = []
            #     pass

            # # -----메뉴-----
            # menu_name = []
            # menu_price = []
            # try:
            #     # menu_plus = driver.find_element(By.CSS_SELECTOR,'.fvwqf')
            #     # menu_plus.click()
            #     driver.find_element(By.LINK_TEXT, "메뉴").click()
            #     menu_list = driver.find_elements(By.CSS_SELECTOR, 'li.E2jtL')
            #     menu_name = []  # 메뉴이름
            #     menu_price = []  # 메뉴가격
            #
            #     for i in menu_list:
            #         name = i.find_element(By.CSS_SELECTOR, '.lPzHi').text
            #         menu_name.append(name)
            #
            #         price = i.find_element(By.CSS_SELECTOR, '.GXS1X').text  # 텍스트를 넣을 변수 생성
            #         # price = re.sub('원\d{2},\d{3}', '', price)  # 할인 전 가격 제거  # 재정의
            #         menu_price.append(price)  # 추가
            #
            # except:
            #     menu_name = []
            #     menu_price = []
            #     pass
            #
            # print(menu_name)
            # print(menu_price)

            # # ---- 이용시간 -----
            # time_list = []
            #
            # try:
            #     # "a" 태그 선택
            #     a_tag = driver.find_element(By.CSS_SELECTOR,
            #                                 '#app-root > div > div > div > div > div > div.place_section.vKA6F > div.place_section_content > div.PIbes > div.O8qbU.pSavy > div.vV_z_ > a.gKP9i.RMgN0')
            #
            #     # "aria-expanded" 속성이 "false"일 때 클릭하여 변경
            #     if a_tag.get_attribute('aria-expanded') == 'false':
            #         a_tag.click()
            #
            #     # 클릭 후 시간 대기 (예: 2초)
            #     time.sleep(2)
            #
            #     times = a_tag.find_elements(By.CSS_SELECTOR, 'div.w9QyJ')
            #     # print(times)
            #
            #     # time_list = []
            #     for i in times:
            #         time_list.append(i.text)
            #     print('time_list: ', time_list)
            #
            # except:
            #     time_list = []
            #     pass

            # ---- list에 데이터 넣기 ----, prices
            list_temp = [store_name, store_type, road_addr, jibun_addr, store_tel, store_rate, store_review]
            store_dict.append(list_temp)

            print(f'... 완료')

            switch_frame('searchIframe')
            sleep(8)

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

# 데이터 프레임으로 변환 , '가격'
df = pd.DataFrame(store_dict, columns=['이름', '유형', '도로명주소', '지번주소', '전화번호', '별점', '리뷰 개수'])

# csv로 저장
df.to_csv('./jeju_shopculture/jeju_shop_sy.csv', encoding='utf-8', index=False)
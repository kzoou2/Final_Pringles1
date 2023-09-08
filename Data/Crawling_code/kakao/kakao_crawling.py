import json
import pandas as pd
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --크롬창을 숨기고 실행-- driver에 options를 추가해주면된다
# options = webdriver.ChromeOptions()
# options.add_argument('headless')

url = 'https://map.kakao.com/'
driver = webdriver.Chrome()  # 드라이버 경로
# driver = webdriver.Chrome('./chromedriver',chrome_options=options) # 크롬창 숨기기
driver.get(url)
key_word = '제주 카페'  # 검색어

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait


# 검색 정보 출력
def jeju_list_print():
    time.sleep(0.2)

    # (3) 장소 목록
    jeju_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

    for index in range(len(jeju_list)):
        print(index)

        # (4) 장소명
        names = driver.find_elements(By.CSS_SELECTOR, '.head_item > .tit_name > .link_name')

        # (5) 장소 유형
        types = driver.find_elements(By.CSS_SELECTOR, '.head_item > .subcategory')

        # (6) 주소
        address_list = driver.find_elements(By.CSS_SELECTOR, '.info_item > .addr')

        # (7) 영업시간
        times = driver.find_elements(By.CSS_SELECTOR, '.openhour > p > a')

        # (8) 전화번호
        phone_num = driver.find_elements(By.CSS_SELECTOR, '.info_item > .contact > .phone')

        # (9) 홈페이지
        home_page = driver.find_elements(By.CLASS_NAME,'homepage')
        href = []
        for i in home_page:
            home_page_href_ = i.get_attribute("href")
            href.append(home_page_href_)

        address = address_list.__getitem__(index).find_elements(By.CSS_SELECTOR, 'p')

        jeju_name = names[index].text
        print(jeju_name)

        jeju_type = types[index].text
        print(jeju_type)

        addr1 = address.__getitem__(0).text
        print(addr1)

        addr2 = address.__getitem__(1).text[5:]
        print(addr2)

        jeju_phone_num = phone_num[index].text
        print(jeju_phone_num)

        jeju_link = href[index]
        print(jeju_link)

        # dict에 데이터 집어넣기
        dict_temp = {
            '이름': jeju_name,
            '유형': jeju_type,
            '도로명주소': addr1,
            '지번주소': addr2,
            '영업시간': jeju_time,
            '전화번호': jeju_phone_num,
            '홈페이지': jeju_link
        }
        jeju_dict.append(dict_temp)
        print(f'{jeju_name} ...완료')


# css를 찾을때 까지 10초 대기
time_wait(10, 'div.box_searchbar > input.query')

# (1) 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, 'div.box_searchbar > input.query')
search.send_keys(key_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

sleep(1)

# (2) 장소 탭 클릭
place_tab = driver.find_element(By.CSS_SELECTOR, '#info\.main\.options > li.option1 > a')
place_tab.send_keys(Keys.ENTER)

sleep(1)

# 검색 리스트
jeju_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

# dictionary 생성
jeju_dict = []
# 시작시간
start = time.time()
print('[크롤링 시작...]')

# 페이지 리스트만큼 크롤링하기
page = 1  # 현재 크롤링하는 페이지가 전체에서 몇번째 페이지인지
page2 = 0  # 1 ~ 5번째 중 몇번째인지
error_cnt = 0

while 1:

    # 페이지 넘어가며 출력
    try:
        page2 += 1
        print("**", page, "**")

        # (7) 페이지 번호 클릭
        driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{page2}"]').send_keys(Keys.ENTER)

        # 검색 리스트 크롤링
        jeju_list_print()

        # 해당 페이지 검색 리스트
        jeju_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')
        # 한 페이지에 장소 개수가 15개 미만이라면 해당 페이지는 마지막 페이지
        if len(jeju_list) < 15:
            break
        # 다음 버튼을 누를 수 없다면 마지막 페이지
        if not driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').is_enabled():
            break

        # (8) 다섯번째 페이지까지 왔다면 다음 버튼을 누르고 page2 = 0으로 초기화
        if page2 % 5 == 0:
            driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
            page2 = 0

        page += 1

    except Exception as e:
        error_cnt += 1
        print(e)
        print('ERROR!' * 3)

        if error_cnt > 5:
            break

print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을 닫는다.

# 데이터프레임
df = pd.DataFrame(jeju_dict)

# csv 파일로 저장
df.to_csv('sy_cafe.csv', encoding='utf-8', index=False)

# json 파일로 저장 -> 검색어별 파일이름 변경
# with open('jeju_hostelall_data.json', 'w', encoding='utf-8') as f:
#     json.dump(jeju_dict, f, indent=4, ensure_ascii=False)
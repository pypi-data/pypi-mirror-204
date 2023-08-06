import time
from typing import Iterator, List, Tuple
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from util_hj3415 import utils, noti
from selenium.webdriver.common.by import By

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

# 4주 전 월요일 09시부터 일주일 단위(월~일) 일괄 오픈
# 7일전까지 위약없음.

COURSE_ADDR = {
    'SONO' : "https://www.sonofelicecc.com/rsv.cal.dp/dmparse.dm?fJiyukCd=60",
    'VIVALDI' : "https://www.sonofelicecc.com/rsvcc.cal.dp/dmparse.dm?fJiyukCd=30",
    'DELPINO' : "https://www.sonofelicecc.com/rsv.cal.dp/dmparse.dm?fJiyukCd=01&pop=Y",
    'MOUNTAIN' : "https://www.sonofelicecc.com/rsv.cal.dp/dmparse.dm?fJiyukCd=02"
}

MAIN_ADDR = 'https://www.sonofelicecc.com/'
LOGIN_ADDR = "https://www.sonofelicecc.com/login.dp/dmparse.dm"


def login(driver: WebDriver, id: str, password: str):
    # 로그인 링크 연결
    print('Login...')
    driver.implicitly_wait(5)
    driver.get(LOGIN_ADDR)

    print('Input id and password')
    driver.find_element(By.ID, 'cyberId').send_keys(id)
    driver.find_element(By.ID, 'cyberPass').send_keys(password)

    print('Click the login button')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="loginBtn"]/a').click()
    # 1초 정도 쉬어야 로그인이 반영된다.
    time.sleep(1)


def logout(driver: WebDriver):
    print('Logout...')
    driver.implicitly_wait(5)
    driver.get(MAIN_ADDR)

    login_link = driver.find_element(By.XPATH, '//*[@id="header"]/div/div[1]/ul[2]/li[1]/a')
    login_status = login_link.text  # '로그인' 또는 '로그아웃'
    logger.info(f"login status : {login_status}")
    if login_status == '로그아웃':
        login_link.click()


def extract_calendar(driver: WebDriver) -> Iterator[List[Tuple[str, str, str, WebElement]]]:
    print("Extract Calander..")
    DAYS_OF_WEEK = {0: "SUN", 1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI", 6: "SAT"}

    tbody_l_xpath = '//*[@id="container"]/div[3]/div[5]/div[1]/fieldset/table/tbody'
    tbody_r_xpath = '//*[@id="container"]/div[3]/div[5]/div[2]/fieldset/table/tbody'

    # 예약 날짜 관련한 테이블을 추출한다.
    tbody_l = driver.find_element(By.XPATH, tbody_l_xpath)
    tbody_r = driver.find_element(By.XPATH, tbody_r_xpath)

    logger.debug(tbody_l.get_attribute("innerHTML"))
    logger.debug(tbody_r.get_attribute("innerHTML"))

    # 좌측 테이블 추출
    for j, tr in enumerate(tbody_l.find_elements(By.TAG_NAME, "tr")):
        # tr은 가로 한줄을 나타냄
        logger.info(f"{j + 1} week.")
        # print(tr.get_attribute("innerHTML"))
        week_data = list()

        for i, td in enumerate(tr.find_elements(By.TAG_NAME, "td")):
            # td는 각 셀을 나타냄
            date = td.get_attribute("day")  # 형식 - 2023.04.01
            inner_html = td.get_attribute("innerHTML").strip().replace("&nbsp;", "")
            soup = BeautifulSoup(inner_html, 'html.parser')
            if date is not None:
                try:
                    status = str(soup.a['title']).strip()
                except KeyError:
                    status = ""
                date_data = (DAYS_OF_WEEK[i], str(date).strip(), status, td)
                week_data.append(date_data)
        logger.debug(week_data)
        yield week_data

    # 우측 테이블 추출
    for j, tr in enumerate(tbody_l.find_elements(By.TAG_NAME, "tr")):
        # tr은 가로 한줄을 나타냄
        logger.info(f"{j + 1} week.")
        # print(tr.get_attribute("innerHTML"))
        week_data = list()

        for i, td in enumerate(tr.find_elements(By.TAG_NAME, "td")):
            # td는 각 셀을 나타냄
            date = td.get_attribute("day")  # 형식 - 2023.04.01
            inner_html = td.get_attribute("innerHTML").strip().replace("&nbsp;", "")
            soup = BeautifulSoup(inner_html, 'html.parser')
            if date is not None:
                try:
                    status = str(soup.a['title']).strip()
                except KeyError:
                    status = ""
                date_data = (DAYS_OF_WEEK[i], str(date).strip(), status, td)
                week_data.append(date_data)
        logger.debug(week_data)
        yield week_data


def extract_timetable(driver: WebDriver):
    pass


def reserve_date(driver: WebDriver, date_wanted: str) -> bool:
    is_reserved = False
    # 예약 날짜 페이지로 이동하여 날짜와 예약가능여부를 추출한다.
    for i, week_data in enumerate(extract_calendar(driver)):
        print(f"{i + 1} week.")
        for day_of_week, date, status, td_web_element in week_data:
            logger.info(f'{day_of_week} / {date} / {status} / {td_web_element}')
            # 원하는 날짜가 예약가능 상태라면...
            if date == date_wanted and "예약하기" in status:
                # 예약을 위해서 '예약하기' 버튼을 누른다.
                td_web_element.find_element(By.TAG_NAME, "a").click()
                time.sleep(0.5)
                is_reserved = True
                break
        if is_reserved:
            break
    return is_reserved

def reserve_time(driver: WebDriver, wanted_time: str, is_testing: bool):
    is_reserved = False
    extract_timetable(driver)

    
def processing(id: str, password: str, course: str, date_wanted: str, time_wanted: str, is_testing: bool):
    driver = utils.get_driver(headless=False)
    wait = WebDriverWait(driver, timeout=10)
    print("Processing...")
    driver.implicitly_wait(5)
    driver.get(MAIN_ADDR)

    # 로그인이 안되어 있으면 로그인 한다.
    login_link = driver.find_element(By.XPATH, '//*[@id="header"]/div/div[1]/ul[2]/li[1]/a')
    login_status = login_link.text   # '로그인' 또는 '로그아웃'
    logger.info(f"login status : {login_status}")
    if login_status == '로그인':
        login(driver, id, password)

    try:
        # 코스 선택
        if course in COURSE_ADDR.keys():
            driver.implicitly_wait(5)
            driver.get(COURSE_ADDR[course])
        else:
            raise

        # 날짜 선택
        is_reserved_date = reserve_date(driver, date_wanted)

        # 날짜 예약이 되어서 시간예약 페이지로 넘어갔는지 is_reserved로 확인한다.
        if is_reserved_date:
            # 시간 예약을 처리하는 함수
            reserve_time(driver, time_wanted, is_testing)
        else:
            print(f"원하는 날짜({date_wanted}일)에 예약이 불가능한 상태입니다.")

    except Exception as e:
            print(f"Exception occurred : {e}")
    finally:
        time.sleep(2)

        # 중복 로그인을 허용하지 않아 깔끔하게 로그아웃을 하고 종료하는게 좋다.
        logout(driver)

        time.sleep(2)
        driver.close()


if __name__ == "__main__":
    ID = 'hj3415'
    PASS = 'ljgda6421~'

    DATE = "2023.04.04"     # 형식 - 2023.04.04
    TIME = "08:3"

    processing(ID, PASS, "VIVALDI", DATE, TIME, True)

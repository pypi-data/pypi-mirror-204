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


MAIN_ADDR = 'https://www.ecolian.or.kr/common/main.do?coDiv='



# 에콜리안 정선 자동예약 프로그램
# 예약 오픈 매월 5일, 20일 저녁 8시 - 15일 단위 예약접수
# 예 - 9월 5일 예약오픈 : 10월 1일 - 15일
# 9월 20일 예약오픈 : 10월 16일 - 말일

# 월 예약 가능 횟수 월 4회/인
# 취소가능일자 - 5일전까지





def extract_timetable(driver: WebDriver) -> Iterator[List[Tuple[str, WebElement]]]:
    """
    예약 시간 페이지에서 예약시간에 대한 정보를 추출하여 각 시간마다 가능한 분단위를 yield한다.
    :param driver:
    :return: 한 시간 단위의 예약 정보를 리스트에 담아 yield한다.
    """
    print("Extract Timetable..")
    driver.implicitly_wait(5)
    driver.refresh()

    # 예약 시간 관련한 테이블을 추출한다.
    tbody = driver.find_element(By.XPATH, '//*[@id="contents"]/table/tbody')
    logger.debug(tbody.get_attribute("innerHTML"))

    # 테이블의 첫줄은 시간과 분을 나타내는 타이틀이라 넘어간다.
    for j, tr in enumerate(tbody.find_elements(By.TAG_NAME, "tr")[1:]):
        # tr은 가로 한줄을 나타냄
        logger.info(f"... hour.")
        # print(tr.get_attribute("innerHTML"))
        hour_data = list()

        for i, td in enumerate(tr.find_elements(By.TAG_NAME, "td")):
            # td는 각 셀을 나타냄
            inner_html = td.get_attribute("innerHTML").strip().replace("&nbsp;", "")
            soup = BeautifulSoup(inner_html, 'html.parser')
            if soup.span is not None:
                # soup.span['time']의 형식 예시 - 06:20
                min_data = (str(soup.span['time']).strip(), td)
                hour_data.append(min_data)

        logger.info(hour_data)
        yield hour_data


def reserve_date(driver: WebDriver, date_wanted: str) -> bool:
    """
    원하는 날짜가 예약가능한지 확인하고 예약가능하면 시간 선택 창으로 넘어가도록 작업한다.
    :param driver:
    :param date_wanted: 원하는 날짜
    :return: 원하는 날짜가 예약이 가능해서 시간선택창으로 이동했는지 여부
    """
    is_reserved = False
    # 예약 날짜 페이지로 이동하여 날짜와 예약가능여부를 추출한다.
    for i, week_data in enumerate(extract_calendar(driver)):
        print(f"{i + 1} week.")
        for day_of_week, date, status, td_web_element in week_data:
            # 원하는 날짜가 예약가능 상태라면...
            if date == date_wanted and "예약가능" in status:
                # 예약을 위해서 '예약가능' 버튼을 누른다.
                td_web_element.find_element(By.TAG_NAME, "p").click()
                time.sleep(0.5)
                # 예약 확인 팝업창의 확인 버튼 누른다...
                driver.find_element(By.XPATH, '//*[@id="rspop_01"]/div[1]/div[3]/div/a[1]').click()
                is_reserved = True
                break
        if is_reserved:
            break
    return is_reserved


def reserve_time(driver: WebDriver, wanted_time: str, is_testing: bool):

    is_reserved = False
    # 예약 시간 페이지로 이동하여 예약가능시간을 추출한다.
    for i, hour_data in enumerate(extract_timetable(driver)):
        print("...hour")
        for hour_min, td_web_element in hour_data:
            # 오픈된 시간_분이 원하는 시간_분대라면...
            hour, min = hour_min.split(":")
            logger.info(f'hour : {hour} / min : {min}')




    if wanted_time in opened_time:
        # 예약가능 버튼을 누른다.
        td.find_element(By.TAG_NAME, "span").click()
        # https://www.selenium.dev/documentation/webdriver/interactions/alerts/ - alert 창 처리
        alert = wait.until(EC.alert_is_present())
        logger.info(alert.text)
        time.sleep(1)
        alert.accept()

        # 예약 최종확인 창으로 넘어간다.
        confirm_reservation()


def confirm_reservation():
    # captcha체크박스
    # //*[@id="recaptcha-anchor"]

    # 신청완료 버튼
    # //*[@id="btnSubmit"]/img

    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, timeout=5)
    # 캡챠 해결하기 - https://www.youtube.com/watch?v=CCcGPLaaU10&t=6s
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
    captcha_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='recaptcha-checkbox-border']")))
    captcha_box.click()

    # 신청완료 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()

    #time.sleep(20)


def processing(id: str, password: str, date_wanted: str, time_wanted: str, is_testing: bool):
    driver = utils.get_driver(headless=False)
    wait = WebDriverWait(driver, timeout=10)
    print("Processing...")
    driver.implicitly_wait(5)
    driver.get(MAIN_ADDR)

    # 로그인이 안되어 있으면 로그인 한다.
    login_img = driver.find_element(By.XPATH, '//*[@id="indexArea"]/div[2]/ul[2]/li[2]/a/img')
    login_status = login_img.get_attribute('alt')   # '로그인' 또는 '로그아웃'
    logger.info(f"login status : {login_status}")
    if login_status == '로그인':
        login(driver, id, password)

    # 예약 달력 페이지로 가서 원하는 날짜 예약 처리한다.
    is_reserved_date = reserve_date(driver, date_wanted)

    # 날짜 예약이 되어서 시간예약 페이지로 넘어갔는지 is_reserved로 확인한다.
    if is_reserved_date:
        # 시간 예약을 처리하는 함수
        reserve_time(time_wanted)
    else:
        print(f"원하는 날짜({date_wanted}일)에 예약이 불가능한 상태입니다.")

    time.sleep(2)
    driver.close()


if __name__ == "__main__":
    ID = 'hj3415'
    PASS = 'piyrw421'

    driver = utils.get_driver(headless=False)
    login(driver, ID, PASS)



    time.sleep(2)
    driver.close()

    DATE = "11"
    TIME = "08:3"

    #processing(ID, PASS, DATE, TIME, True)



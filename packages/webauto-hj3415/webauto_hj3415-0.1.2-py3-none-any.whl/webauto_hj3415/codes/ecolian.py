import time
from typing import Dict
import os

from twocaptcha import TwoCaptcha

import selenium.common.exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from util_hj3415 import utils
from selenium.webdriver.common.by import By

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


# 개인별 예약가능 횟수는 매 월 4회까지이고(9홀, 18홀 구분없음), 취소가능 횟수는 연 12회까지입니다.
# 예약취소는 홈페이지에서 언제든지 가능하며, 골프장 이용일 4일전부터 페널티가 적용됩니다.

def logout(driver:WebDriver):
    MAIN_PAGE = "https://www.ecolian.or.kr"

    # 로그인 링크 연결
    print(f'Logging out...')
    driver.implicitly_wait(5)
    driver.get(MAIN_PAGE)

    print('Click the logout button')
    time.sleep(1)
    login_out_link = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div[1]/div/div/ul[2]/li[1]/a')
    log_status = login_out_link.get_attribute('title')  # '로그인' 또는 '로그아웃'
    logger.debug(f"log status : {log_status}")
    if log_status == '로그아웃':
        login_out_link.click()


def login(driver: WebDriver, my_id: str, password: str):
    """
    에콜리안 정선의 홈페이지에 로그인한다.
    :param driver:
    :param my_id:
    :param password:
    :return:
    """
    LOGIN_ADDR = "https://www.ecolian.or.kr/join/login.do"

    # 로그인 링크 연결
    print(f'Logging in...{my_id} / {password}')
    driver.implicitly_wait(5)
    driver.get(LOGIN_ADDR)

    print('Input id and password')
    driver.find_element(By.ID, 'userId').send_keys(my_id)
    driver.find_element(By.ID, 'userPw').send_keys(password)

    print('Click the login button')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div/div[2]/a').click()

    mainwindow_handle = driver.current_window_handle
    logger.debug(f"mainwindow_handle: {mainwindow_handle}")
    wait = WebDriverWait(driver, timeout=2)

    try:
        # 이미 로그인한 상태라면 로그아웃하고 로그인하겠냐는 확인창뜸.
        if wait.until(EC.alert_is_present()) is not None:
            alert = driver.switch_to.alert
            logger.debug(f'{alert.text} - message window opened')
            alert.accept()
    except selenium.common.exceptions.TimeoutException:
        pass

    time.sleep(1)

    # 로그인하면 이상한 팝업창들이 뜨는데 이것들을 정리하는 코드
    logger.debug(f"window_handles: {driver.window_handles}")
    for window_handle in driver.window_handles:
        if window_handle != mainwindow_handle:
            driver.switch_to.window(window_handle)
            driver.close()

    driver.switch_to.window(mainwindow_handle)


def select_course(driver: WebDriver, course: str):
    course_id = {
        "광산": "104",
        "정선": "102",
        "제천": "101",
        "영광": "105",
        "거창": "103",
    }

    if course not in course_id.keys():
        raise

    RESERV_ADDR = f'https://www.ecolian.or.kr/reser/reser.do?coDiv={course_id[course]}'
    logger.info(f"{course} : {RESERV_ADDR}")
    print(f'Select course {course} & move to reservation page...')
    driver.implicitly_wait(5)
    driver.get(RESERV_ADDR)


def extract_calendar(driver: WebDriver) -> Dict[str, WebElement]:
    print("Extract possible dates from Calander ..")
    possible_date_dict = dict()
    for i in range(1, 3):
        cal_tbody = f'//*[@id="calendarBox{i}"]/table/tbody'
        cal_header = f'//*[@id="calendarBox{i}"]/div/ul/li[2]'

        # 예약 날짜 관련한 테이블을 2번 추출한다.(좌측달력, 우측달력)
        tbody = driver.find_element(By.XPATH, cal_tbody)
        logger.debug(tbody.get_attribute("innerHTML"))
        year, month = driver.find_element(By.XPATH, cal_header).text.split('.')
        logger.debug(f"{year} / {month}")

        for i, td in enumerate(tbody.find_elements(By.TAG_NAME, "td")):
            # td는 각 셀을 나타냄
            status_list = td.get_attribute("class").split()  # status_list = [done, impossible, possible] 을 가질 수 있음.
            logger.debug(status_list)
            if 'possible' in status_list:
                logger.debug(td.get_attribute("innerHTML"))
                date_link_element = td.find_elements(By.TAG_NAME, "a")
                date = date_link_element[0].text[:2]    # ex - 12<span>잔여 3</span> 문자열에서 앞의 두자리숫자가 날짜임.
                possible_date_dict[month+date] = date_link_element[0]

    # import pprint
    # pprint.pprint(possible_date_dict)
    return possible_date_dict


def select_date(driver: WebDriver, possible_dates: Dict[str, WebElement], desired_date: str) -> bool:
    for date, webelement in possible_dates.items():
        if desired_date == date:
            # 날짜를 선택한다.
            print(f'Select {date} & move to timetable page...')
            webelement.click()
            # 검색버튼을 누른다.
            time.sleep(1)
            # 일반적인 click()함수로는 실행되지 않아서 execute_script를 사용하여 버튼을 누른다.
            btn = driver.find_element(By.XPATH, '//*[@id="mainForm"]/div/div[2]/div[3]/div[3]/button')
            driver.execute_script("arguments[0].click();", btn)
            return True
    else:
        return False


def extract_time(driver: WebDriver) -> Dict[str, WebElement]:
    print("Extract possible times from Timetable ..")
    possible_time_dict = dict()
    time.sleep(1)

    # 예약 시간 관련한 테이블을 추출한다.
    wait = WebDriverWait(driver, timeout=10)
    tbody = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="time-grid-tablet"]')))
    logger.debug(tbody.get_attribute("innerHTML"))

    for a_href_time_element in tbody.find_elements(By.TAG_NAME, "a"):
        logger.debug(a_href_time_element.get_attribute("innerHTML"))
        possible_time = a_href_time_element.get_attribute("text")
        possible_time_dict[possible_time] = a_href_time_element

    # import pprint
    # pprint.pprint(possible_time_dict)
    return possible_time_dict


def select_time(driver: WebDriver, possible_times: Dict[str, WebElement], desired_time: str) -> bool:
    for time, webelement in possible_times.items():
        if time >= desired_time:
            # 시간을 선택한다.
            print(f'Select {time} & move to confirm page...')
            # 일반적인 click()함수로는 실행되지 않아서 execute_script를 사용하여 버튼을 누른다.
            driver.execute_script("arguments[0].click();", webelement)
            return True
    else:
        return False


def get_code_from_twocaptcha(path: str) -> str:
    api_key = os.getenv('APIKEY_2CAPTCHA', 'f4bfc7cbda6aaa0b0dab82e5c5e48325')
    solver = TwoCaptcha(api_key)
    try:
        result = solver.normal(path)
    except Exception as e:
        logger.error(e)
        return ''
    else:
        logger.info(f"captcha : {result}")
        return result['code']


def get_a_image(driver: WebDriver) -> str:
    captcha_img_xpath = '//*[@id="catpcha"]/img'
    temp_img_path = '../ecolian_captcha.png'
    captcha_img = driver.find_element(By.XPATH, captcha_img_xpath)
    captcha_img.screenshot(temp_img_path)
    return temp_img_path


def input_the_code(driver: WebDriver, code: str):
    captcha_input_xpath = '//*[@id="answer"]'

    driver.find_element(By.XPATH, captcha_input_xpath).send_keys(code)
    time.sleep(1)

    confirm_btn_xpath = '//*[@id="mainForm"]/div/div/div/div[2]/a[2]'
    confirm_btn = driver.find_element(By.XPATH, confirm_btn_xpath)
    driver.execute_script("arguments[0].click();", confirm_btn)


def process_alert_window(driver: WebDriver, is_testing) -> bool:
    wait = WebDriverWait(driver, timeout=2)

    try:
        # 이미 로그인한 상태라면 로그아웃하고 로그인하겠냐는 확인창뜸.
        if wait.until(EC.alert_is_present()) is not None:
            alert = driver.switch_to.alert
            logger.debug(f'{alert.text} - message window opened')
            if "확정하시겠습니까" in alert.text:

                # alert.accept() - 추후에 이것으로 바꾼다.
                if is_testing:
                    print(f"Reservation confirmed - {str(alert.text).strip()} - dismiss")
                    alert.dismiss()
                else:
                    print(f"Reservation confirmed - {str(alert.text).strip()} - accept")
                    alert.accept()
                    time.sleep(1)
                    alert = driver.switch_to.alert
                    logger.info(f'{alert.text} - message window opened')
                    time.sleep(5)
                return True
            elif "일치하지" in alert.text:
                print(f"Recaptcha input error...retrying...")
                alert.accept()
                return False
            else:
                print(f"Reservation dismissed...")
                alert.dismiss()
                return False
    except selenium.common.exceptions.TimeoutException:
        return False


def resolve_captcha(driver: WebDriver, is_testing: bool):
    img_path = get_a_image(driver)

    trying = 0
    while True:
        trying += 1
        captcha_code = get_code_from_twocaptcha(img_path)
        input_the_code(driver, captcha_code)
        is_confirmed = process_alert_window(driver, is_testing)
        if is_confirmed or trying > 2:
            break


def processing(courses: list, date: str, mytime: str, myid: str, mypass: str, is_testing: bool = False, headless: bool = True):
    if is_testing:
        print("This is a testing mode..")
    my_driver = utils.get_driver(headless=headless)
    login(my_driver, myid, mypass)
    for course in courses:
        select_course(my_driver, course)

        possible_date_dict = extract_calendar(my_driver)
        logger.info(f'possible_date : {possible_date_dict.keys()}')
        is_select_date = select_date(my_driver, possible_date_dict, date)

        if is_select_date:
            possible_time_dict = extract_time(my_driver)
            logger.info(f'possible_time : {possible_time_dict.keys()}')
            is_select_time = select_time(my_driver, possible_time_dict, mytime)

            if is_select_time:
                resolve_captcha(my_driver, is_testing)
            else:
                print(f"There are no available time after {mytime} on {date}..")
        else:
            print(f"There are no available date on {date}..")

    logout(my_driver)

    print("Done")
    my_driver.quit()


if __name__ == "__main__":
    DATE = '0419'
    TIME = '05:00'
    ID = 'hj3415'
    PASS = 'piyrw421'

    processing("정선", DATE, TIME, ID, PASS, is_testing=False, headless=False)




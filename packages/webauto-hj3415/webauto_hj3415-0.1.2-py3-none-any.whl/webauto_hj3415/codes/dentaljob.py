from util_hj3415 import utils, noti
from selenium.webdriver.common.by import By

ADDR = 'https://www.dentaljob.co.kr/00_Member/00_Login.aspx'

# 덴탈잡 점프업 자동화 프로그램

driver = utils.get_driver()
driver.get(ADDR)
driver.implicitly_wait(10)
print('Trying login and refresh...')

try:
    print('Input id and password')
    driver.find_element(By.NAME, 'login_id').send_keys('${ID}')
    driver.find_element(By.NAME, 'login_pw').send_keys('${PASS}')

    print('Click the login button')
    driver.find_element(By.ID, 'ctl00_ctl00_cbody_cbody_btnLogin').click()
    print('Click the 개재중인 채용광고 link')
    driver.find_element(By.XPATH, '//*[@id="login_on"]/div[2]/p[1]/a').click()
    print('Click the JumpUp button')
    driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_cbody_cbody_pnViewMenuAuth"]/table/tbody/tr[1]/td[2]/p[2]/img[1]').click()
    print('Done.')
except:
    #print('Wrong.')
    noti.telegram_to(botname="manager", text="Something wrong during dentaljob refreshing.")
finally:
    driver.close()
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import requests
import csv
import keyword_extract

#use as headless mode
options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome("../chromedriver",options=options)
class_list = []

USERID = 'id'
PASSWORD = 'pass'

# driver = webdriver.Chrome('/Users/hyugataki/Univ/B3/dbd/scraping/chromedriver')
error_flg = False
target_url = 'https://muscat.musashino-u.ac.jp/portal/top.do'
driver.get(target_url)
sleep(3)

#ログイン処理
username_input = driver.find_element(by=By.ID,value='userId')
username_input.send_keys(USERID)

password_input = driver.find_element(by=By.ID,value='password')
password_input.send_keys(PASSWORD)
sleep(1)
loginBtn = driver.find_element(by=By.XPATH, value="//*[@id='loginButton']")
loginBtn.click()
sleep(1)

#シラバス検索
syllabusSearch = driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/div[6]/ul/li[4]/ul/li[1]/a").get_attribute("href")
driver.get(syllabusSearch)
sleep(1)

dropdown = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/table/tbody/tr/td[1]/form/div[3]/div[2]/table/tbody/tr[5]/td[2]/select')
select = Select(dropdown)
select.select_by_index(1)
driver.find_element(by=By.XPATH, value="//*[@id='srch_search']").click()
sleep(1)

    #講義を抽出
LecList = []
OverviewList = []
j = 1
while j < 41:
    j += 1
    for i in range(3, 23): #20件取得する23
        lec_list = "//*[@id='form']/div[4]/table/tbody/tr[" + str(i) + "]/td[3]/a"
        driver.find_element(by=By.XPATH, value=lec_list).click()
        sleep(2)
        lec = driver.find_element(by=By.XPATH, value="//*[@id='form']/div[2]/table/tbody/tr[3]/td[3]")
        # print(lec.text)
        ll = []
        ll.append(lec.text)
        print(ll)
        LecList.append(ll)
        # print(LecList)
        sleep(1)
        overview = driver.find_element(by=By.XPATH, value="//*[@id='form']/div[3]/table/tbody/tr[1]/td[3]/table/tbody/tr/td")
        lll = []
        lll.append(overview.text)
        OverviewList.append(lll)
        # print(overview.text)
        # OverviewList.append(OV)
        # OverviewList.append(overview.text)

        driver.find_element(by=By.XPATH, value="//*[@id='back']").click()
        sleep(1)
        if i == 22: #次のページに
            p = j + 1
            nxtP = "//*[@id='form']/div[4]/table/tbody/tr[1]/td/div[2]/span[2]/a[" + str(p) + "]"
            driver.find_element(by=By.XPATH, value=nxtP).click()
        else:
            continue
else:
    print("DONE")

f = open("test.csv", 'w', newline='')
writer = csv.writer(f)
writer.writerows(LecList)
f.close()
print("出力完了")


f = open("muscat.csv", 'w', encoding='utf-8')
writer = csv.writer(f,lineterminator='\n')
writer.writerows(OverviewList)
f.close()
print("出力完了")

f2 = open("muscat_title.csv", 'w', encoding='utf-8')
writer = csv.writer(f2,lineterminator='\n')
writer.writerows(LecList)
f2.close()
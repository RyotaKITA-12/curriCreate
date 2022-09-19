from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import csv
import keyword_extract
import re
import pandas as pd


#use as headless mode
options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome("../chromedriver",options=options)
class_list = []

USERID = 's2022022'
PASSWORD = '_7j_ZwM8'

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
lec_all = []
    #講義を抽出
LecList = []
OverviewList = []

dropdown = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/table/tbody/tr/td[1]/form/div[3]/div[2]/table/tbody/tr[5]/td[2]/select')
select = Select(dropdown)
select.select_by_index(1)
driver.find_element(by=By.XPATH, value="//*[@id='srch_search']").click()
sleep(1)
english_lec = ["英語基礎A","英語基礎B","英語基礎C","英語基礎D","フィールド・スポーツ"]
j = 1
TF = True
try:
    while TF == True:
        j += 1
        for i in range(3, 23): #20件取得する23
            kari = []
            try:
                lec_list = "//*[@id='form']/div[4]/table/tbody/tr[" + str(i) + "]/td[3]/a"
                lec_data = driver.find_element(by=By.XPATH, value=lec_list)
            except NoSuchElementException:
                TF = False
                break
            
            # sleep(2)
            # lec = driver.find_element(by=By.XPATH, value="//*[@id='form']/div[2]/table/tbody/tr[3]/td[3]")
            lec = lec_data.text
            lec_sprit = re.sub('\[.*?\]','',lec)
            print(j)
            
            if lec_sprit in english_lec:
                class_list.append(lec_sprit)
                lec = lec
            elif lec_sprit in class_list:
                if i == 22: #次のページに
                    driver.execute_script("doPaging('form','navigateKougiList','pageCount','"+str(j)+"','maxCount','20');return false;")
                    # driver.execute_script("doPaging('form','navigateKougiList','pageCount','80','maxCount','20');return false;")⇦これ以上ない場合のテスト
                else:
                    continue
                continue
            else:
                class_list.append(lec_sprit)
                lec = lec_sprit
            # print(lec.text)
            lec_data.click()
            ll = []
            kari.append(lec)

            sleep(1)
            overview = driver.find_element(by=By.XPATH, value="//*[@id='form']/div[3]/table/tbody/tr[1]/td[3]/table/tbody/tr/td")
            kari.append(overview.text)

            keyword = '・'.join(keyword_extract.run(lec,overview.text))
            kari.append(keyword)
            

            driver.find_element(by=By.XPATH, value="//*[@id='back']").click()
            sleep(1)
            lec_all.append(kari)
            if i == 22: #次のページに
                driver.execute_script("doPaging('form','navigateKougiList','pageCount','"+str(j)+"','maxCount','20');return false;")
            else:
                continue
    else:
        print("DONE")


    df = pd.DataFrame(lec_all,columns=["lec","overvier","keyword"])
    df.to_csv("output.csv",index=False)
except:
    df = pd.DataFrame(lec_all,columns=["lec","overvier","keyword"])
    df.to_csv("output.csv",index=False)
    

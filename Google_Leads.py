from selenium import webdriver  
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd




now = datetime.now()
print('Start time:', now)
Filetime = now.strftime("%Y%m%d_%H%M%S")
file_name = 'Your Excel Name' + ' - ' + str(Filetime)+ '.xlsx'

data_set = []

print('sleep 3 sec')
time.sleep(3)

driver = webdriver.Chrome("excutive Path")
driver.maximize_window()

url = "https://www.google.com/"
driver.get(url)
time.sleep(3)

driver.find_element_by_name("q").send_keys("architects in bangalore")
# driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys("architects in chennai")
time.sleep(5)
# click on the Google search button 
# driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[2]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)
time.sleep(3)
driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mtqGb", " " ))]').click()
time.sleep(5)


page = 1
data_set = []

while True:
    
    time.sleep(5)
    links = driver.find_elements_by_class_name("dbg0pd")
    print(len(links))
    
    for i in links:
        
        time.sleep(5)
        i.click()
        time.sleep(3)
        page_content = driver.page_source
        # with open('Sourcepage.html','w',encoding='utf-8') as dp:
            # dp.write(page_content)

        Outlet_Name = re.findall("<span>([^>]*?)</span></h2>", page_content)
        if Outlet_Name:
            Outlet_Name = Outlet_Name[0]
            Outlet_Name = re.sub('&amp;', '&',Outlet_Name)
        else:
            Outlet_Name = ''
        
        # print("outlets:", Outlet_Name)
        # input('stop')

        Address = re.findall("class\=\"LrzXr\">([^>]*?)</span>", page_content)
        
        if Address:
            Address = Address[0]
            Address = re.sub('&amp;', '&',Address)
        else:
            Address = ''
        # print("address", Address)

        Phone_Number = re.findall("<span\s*aria-label[^>]*?>([^>]*?)</span></a>", page_content)
        if Phone_Number:
            Phone_Number = Phone_Number[0]
        else:
            Phone_Number = ''
        # print(":phone number",Phone_Number)

        ratings = re.findall('class\="fzTgPe\s*Aq14fc"[^>]*?>([^>]*?)</span>', page_content)
        if ratings:
            ratings = ratings[0]
        else:
            ratings = ''
        # print("ratings", ratings)
        
        

        data_set.append((Outlet_Name, Address, Phone_Number, ratings))
        
        # print('data_set:', data_set)
        df = pd.DataFrame(data_set,columns=['Outlet Name', 'Address', 'Phone Number', 'Rating'])
        df.to_excel(file_name, index= False)
    try:
        driver.find_element_by_xpath('//*[@id="pnnext"]').click()
        page+=1
        print('page:', page)
    except:
        break
        
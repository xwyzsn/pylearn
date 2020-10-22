from selenium import webdriver
from PIL import Image

#img = Image.open('capt.png')
#img = img.convert('L')  # P模式转换为L模式(灰度模式默认阈值127)
#count = 128  # 设定阈值
#table = []
#for i in range(256):
#    if i < count:
#        table.append(0)
#    else:
#        table.append(1)
#
#
#
#
#
#img = img.point(table, '1')
#table2=[]
#import numpy as np
#img_arr=np.array(img)
#print(img_arr)
#hei,wid=img_arr.shape
#
#for i in range(1,hei-1):
#    cnt=0
#    for j in range(1,wid-1):
#        if img_arr[i,j]==True:
#            continue
#        if img_arr[i+1,j]==False:
#            cnt+=1
#        if img_arr[i-1,j]==False:
#            cnt+=1
#        if img_arr[i-1,j-1]==False:
#            cnt+=1
#        if img_arr[i+1,j-1]==False:
#            cnt+=1
#        if img_arr[i-1,j+1]==False:
#            cnt+=1
#        if img_arr[i+1,j+1]==False:
#            cnt+=1
#        if img_arr[i,j-1]==False:
#            cnt+=1
#        if img_arr[i,j+1]==False:
#            cnt+=1
#        if cnt<8:
#            img_arr[i,j]=True
#print(img_arr)        
#
#img=Image.fromarray(np.uint8(img_arr*255))
#
#
#img.save('captcha1.png')  # 保存处理后的验证码
#
#yzm=pytesseract.image_to_string(Image.open('2.png'))
#print(yzm)

from selenium.webdriver.chrome.options import Options
chrome_options=Options()

chrome_options.add_argument('--headless')


browser = webdriver.Chrome(chrome_options=chrome_options)
url ='http://www.gdjw.zjut.edu.cn/jwglxt/xtgl/login_slogin.html'
browser.get(url)
png = browser.find_element_by_id('yzmPic')
png.screenshot('capt.png')
print('输入学号')
stu_name=input()
print('输入密码')
stu_pwd=input()
print('输入验证码')
yzm=input()
browser.find_element_by_id('yhm').clear()
browser.find_element_by_id('mm').clear()
browser.find_element_by_id('yzm').clear()
browser.find_element_by_id('yhm').send_keys(stu_name)
browser.find_element_by_id('mm').send_keys(stu_pwd)
browser.find_element_by_id('yzm').send_keys(yzm)
browser.find_element_by_id('dl').click()
#browser.find_element(By.xpath("//a[contains(text(),'等级考报名')]")).click()
import time
time.sleep(3)
browser.find_element_by_xpath("//a[contains(text(),'信息查询')]").click()
time.sleep(2)
browser.find_element_by_xpath("//a[contains(text(),'学生成绩查询')]").click()
time.sleep(4)
wnd= browser.window_handles
browser.switch_to.window(wnd[-1])
#tmp=browser.find_element_by_id('kbgrid_table_0').get_attribute('textContent')
#print(tmp)
#cur_url=browser.current_url
#import pandas as pd
#print(cur_url)
#table=pd.read_html(cur_url)
#print(table)
'''
#获取table
table_tr_list = browser.find_element_by_id('kbgrid_table_0').find_elements_by_tag_name('tr')
table_list=[]
for tr in table_tr_list:
    
    table_td_list = tr.find_elements_by_tag_name("td")
    row_list=[]
    for td in table_td_list:
        row_list.append(td.text)
        
    table_list.append(row_list)

print(table_list)
'''
browser.find_element_by_id('xnm_chosen').click()
browser.find_element_by_xpath('//li[1]').click()
browser.find_element_by_id('xqm_chosen').click()

(browser.find_element_by_id('xqm_chosen').find_element_by_xpath('.//li[1]')).click()
time.sleep(1)
browser.find_element_by_id('search_go').click()
time.sleep(2)

#table_tr_list = browser.find_element_by_id('tabGrid').find_elements_by_tag_name('tr')

#for tr in table_tr_list:
#    
#    table_td_list = tr.find_elements_by_tag_name("td")
#    row_list=[]
#    for td in table_td_list:
#        row_list.append(td.text)
#        
#    table_list.append(row_list)


table_list=[]
t = browser.find_element_by_id('sp_1_pager').text
t = int(t)
for i in range(t):
    table_tr_list = browser.find_element_by_id('tabGrid').find_elements_by_tag_name('tr')
    for tr in table_tr_list:
        table_td_list = tr.find_elements_by_tag_name("td")
        row_list=[]
        for td in table_td_list:
            row_list.append(td.text)    
        table_list.append(row_list)
    browser.find_element_by_id('next_pager').click()
    time.sleep(2)
#
print(table_list)


import pandas as pd
l=table_list
df=pd.DataFrame(l)
df=df[[1,2,4,5,6,9]]
df.columns=['学年','学期','课程名字','课程性质','学分','成绩']
for i in range(1,len(df)):
    i=i*16
    print(i)
    if(i>len(df)):
        break
    df=df.drop(i)
    
df=df.reset_index(drop=True)
bxk=df[df["课程性质"]=="必修课"]
rxk=df[df["课程性质"]=="任选课"]
tyk=df[df["课程性质"]=="体育课"]
xxk=df[df["课程性质"]=="限选课"]
print("不展示选修课\n")
three_cour=df[df["课程性质"]!="任选课"]
print(three_cour)
print("\n 计算总绩点:\n")
three_cour=three_cour.reset_index(drop=True)
three_cour=pd.DataFrame(three_cour)
three_cour['成绩']=pd.to_numeric(three_cour['成绩'])
three_cour['学分']=pd.to_numeric(three_cour['学分'])
s1=(three_cour["学分"].iloc[:]*three_cour["成绩"].iloc[:]).sum()
total_cre=three_cour["学分"].iloc[:].sum()
print(s1/(total_cre))




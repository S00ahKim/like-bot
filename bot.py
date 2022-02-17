# -*- coding: utf-8 -*-

from nis import cat
from selenium import webdriver
import inspect, os, platform, time
from config import exec_options

def bot(): 
  #필요한 변수 정의 
  insta_id = exec_options['id']
  insta_pw = exec_options['password']
  insta_tag = exec_options['tags'][0]
  insta_cnt = 2

  #크롬드라이버 로딩 
  options = webdriver.ChromeOptions() 
  options.add_argument('--disable-gpu') 

  current_folder = os.path.realpath( os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) 
  if platform.system() == 'Windows': 
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    driver_path = os.path.join(current_folder, 'chromedriver.exe') 
  else: 
    options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36')
    driver_path = os.path.join(current_folder, 'chromedriver') 
  
  driver = webdriver.Chrome(driver_path, options=options) 
  driver.implicitly_wait(10)

  ### 인스타그램 자동 좋아요 작업 ### 
  # 1. 인스타그램 로그인 페이지로 이동 
  driver.get('https://www.instagram.com/?hl=ko') 
  print('로그인중....') 
  time.sleep(5)

  # 2. 아이디 입력창을 찾아서 위에서 입력받은 아이디(insta_id)값 입력
  try:
    id_input = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input') 
    id_input.click() #입력창 클릭 
    id_input.send_keys(insta_id) #아이디 입력 
  except:
    id_input = driver.find_element_by_xpath('/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input') 
    id_input.click() #입력창 클릭       
    id_input.send_keys(insta_id) #아이디 입력 
  
  # 2-1. 패스워드 입력창을 찾아서 위에서 입력받은 패스워드(insta_pw)값 입력 
  try:
    pw_input = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input') 
    pw_input.click() 
    pw_input.send_keys(insta_pw) 
  except:
    pw_input = driver.find_element_by_xpath('/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input') 
    pw_input.click() 
    pw_input.send_keys(insta_pw) 
  
  # 3. 로그인 버튼 클릭 
  login_btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button') 
  login_btn.click() 
  
  # 잠시 대기 
  time.sleep(3)

  # 로그인 정보 남기지 않도록 하기
  not_save = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button[1]')
  not_save.click()
  time.sleep(1)

  # 알림 설정 나중에 하기
  alert_later = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
  alert_later.click()
  time.sleep(1)

  # 검색어 입력
  driver.get('https://www.instagram.com/explore/tags/' + insta_tag)
  time.sleep(5)

  # 5. 인기게시물 첫번째 피드 선택
  first_feed = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a') 
  first_feed.click() 
  time.sleep(10)
  
  # 6. 좋아요 작업
  driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button').click()

  idx = 1
  if idx < insta_cnt: 
    next_feed = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/button') 
    next_feed.click()
    driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button').click()
    time.sleep(5)
    idx += 1
  
  print('모든 작업 완료') 
  driver.quit()

bot()
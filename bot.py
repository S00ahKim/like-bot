# -*- coding: utf-8 -*-

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
  options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')

  current_folder = os.path.realpath( os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) 
  if platform.system() == 'Windows': 
    driver_path = os.path.join(current_folder, 'chromedriver.exe') 
  else: 
    driver_path = os.path.join(current_folder, 'chromedriver') 
  
  driver = webdriver.Chrome(driver_path, options=options) 
  driver.implicitly_wait(10)

  ### 인스타그램 자동 좋아요 작업 ### 
  # 1. 인스타그램 로그인 페이지로 이동 
  driver.get('https://www.instagram.com/?hl=ko') 
  print('로그인중....') 
  time.sleep(5)

  # 2. 아이디 입력창을 찾아서 위에서 입력받은 아이디(insta_id)값 입력 
  id_input = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label') 
  id_input.click() #입력창 클릭 
  id_input.send_keys(insta_id) #아이디 입력 
  
  # 2-1. 패스워드 입력창을 찾아서 위에서 입력받은 패스워드(insta_pw)값 입력 
  pw_input = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label') 
  pw_input.click() 
  pw_input.send_keys(insta_pw) 
  
  # 3. 로그인 버튼 클릭 
  login_btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button') 
  login_btn.click() 
  
  # 잠시 대기 
  time.sleep(3)

  # 5. 인기게시물 첫번째 피드 선택
  first_feed = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]') 
  first_feed.click() 
  time.sleep(1) 
  
  # 6. 좋아요 작업 - 입력한 횟수만큼 반복 작업 
  for idx in range(insta_cnt): 
    div = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div') 
    div = div.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]') 
    like_btn = div.find_element_by_tag_name('button') #좋아요 버튼 
    
    like_btn.click() #좋아요 클릭 
    print('{}번째 피드 좋아요 작업 완료'.format(idx + 1))
    
    # 너무 빠르게 작업을 할 경우 많은 양의 작업을 하게 되어 인스타그램측에서 계정 정지나 경고를 할 수 있으니
    # 작업과 다음 작업 사이의 속도를 조절하기 위해 20초 이상을 설정해주세요. 
    time.sleep(5)

    # 7. 좋아요 작업 - 다음 피드로 이동 
    if idx < insta_cnt: 
      next_feed = driver.find_element_by_link_text('다음') 
      next_feed.click()
  
  print('모든 작업 완료') 
  driver.quit()

bot()
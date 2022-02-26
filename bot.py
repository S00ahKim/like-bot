# -*- coding: utf-8 -*-

from selenium import webdriver
import inspect, os, platform, time
from config import exec_options

def bot(num_of_likes):
  insta_tags = exec_options['tags']
  driver = get_chrome_driver()
  login(driver)
  for tag in insta_tags:
    auto_like(driver, tag, num_of_likes)
  driver.quit()

def get_chrome_driver():
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
  return driver

def login(driver):
  insta_id = exec_options['id']
  insta_pw = exec_options['password']

  # 인스타그램 로그인 페이지로 이동 
  driver.get('https://www.instagram.com/?hl=ko') 
  print('로그인중....') 
  time.sleep(5)

  # 아이디 입력창을 찾아서 위에서 입력받은 아이디(insta_id)값 입력
  try:
    id_input = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input') 
    id_input.click() #입력창 클릭 
    id_input.send_keys(insta_id) #아이디 입력 
  except:
    id_input = driver.find_element_by_xpath('/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input') 
    id_input.click() #입력창 클릭       
    id_input.send_keys(insta_id) #아이디 입력 
  
  # 패스워드 입력창을 찾아서 위에서 입력받은 패스워드(insta_pw)값 입력 
  try:
    pw_input = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input') 
    pw_input.click() 
    pw_input.send_keys(insta_pw) 
  except:
    pw_input = driver.find_element_by_xpath('/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input') 
    pw_input.click() 
    pw_input.send_keys(insta_pw) 
  
  # 로그인 버튼 클릭 
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
  print('로그인 완료')

def auto_like(driver, tag, cnt):
  # 검색어 입력
  driver.get('https://www.instagram.com/explore/tags/' + tag)
  time.sleep(5)

  # 인기게시물 첫번째 피드 선택
  idx = 1
  first_feed = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a') 
  first_feed.click() 
  time.sleep(5)
  # 좋아요 작업
  try:
    check_if_liked(driver)
    driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button').click()
  except Exception as e:
    print(e)
    idx -= 1
  # 다음 피드 클릭
  driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/button').click()
  time.sleep(3)
  print('tag: %s, cnt: %s' % (tag, idx))

  while idx < cnt: 
    try:
      check_if_liked(driver)
      driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button').click()
      idx += 1
      print('tag: %s, cnt: %s' % (tag, idx))
    except Exception as e:
      print(e)
    finally:
      driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/button').click()
      time.sleep(3)

def check_if_liked(driver):
  _likes = driver.find_elements_by_css_selector("svg[aria-label=좋아요]")
  _like = [x for x in _likes if int(x.get_attribute('width')) > 20]
  if len(_like) == 0:
    raise Exception('Already Done!')
  if _like[0].get_attribute('color') != str('#8e8e8e'):
    raise Exception('Already Done!')

def main():
  num_of_likes = int(input('각 태그에 대해 몇 개의 좋아요를 작업할까요? :'))
  bot(num_of_likes)

if __name__ == '__main__':
  main()
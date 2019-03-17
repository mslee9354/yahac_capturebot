import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium import webdriver
import traceback


class Capture_Bot(object):
	def __init__(self, email, password):
		options = Options()
		# options.headless = True  # 만약 브라우저 창을 닫고싶다면 주석 해제
		# options.add_argument('--disable-gpu')
		self.driver = webdriver.Firefox(
			options=options, executable_path='geckodriver')
		self.driver.set_window_size(1500, 1000)
		self.driver.get(
			'https://discordapp.com/channels/336499288001478656/336499288001478656')  # 코야 대화방 접속
		self.driver.find_element_by_xpath(
			'//*[@id="app-mount"]/div[1]/div/div[2]/div/form/div/div[3]/div[1]/div/input').send_keys(email)  # 로그인 폼에 이메일 입력
		self.driver.find_element_by_xpath(
			'//*[@id="app-mount"]/div[1]/div/div[2]/div/form/div/div[3]/div[2]/div/input').send_keys(password)  # 로그인 폼에 비밀번호 입력
		self.driver.find_element_by_xpath(
			'//*[@id="app-mount"]/div[1]/div/div[2]/div/form/div/div[3]/button[2]').click()  # 로그인 버튼 클릭
	def captuere_image(self):
		cnt = 0  # 파일명
		while True:
			self.driver.implicitly_wait(1.5)
			self.driver.find_element_by_tag_name(
				'html').send_keys(Keys.ESCAPE)  # 새 메세지 제거
			parent_elem = self.driver.find_element_by_xpath(
				'/html/body/div/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div[1]')
			child_elems = parent_elem.find_elements_by_css_selector(
				'.messages-3amgkR > *')  # parent_elem의 하위 자식들 즉, 대화 내용
			if cnt == 0:
				lowest_elem = {'elem': child_elems[0], 'height': child_elems[0].size['height']} # 초기화
			for elem in child_elems:
				self.driver.find_element_by_tag_name(
					'html').send_keys(Keys.PAGE_DOWN)  # 아래로 스크롤
				if elem != child_elems[0]:
					if elem.location['y'] >= parent_elem.location['y']: # 만약 elem이 화면 밖에 있다면
						if lowest_elem['height'] < elem.size['height'] and lowest_elem['elem'] == elem: # 만약 elem이 수정되었다면
							lowest_elem = {'elem': elem, 'height': elem.size['height']}
						elif lowest_elem['elem'].location['y'] >= elem.location['y']:
							continue
						location = 'Location/{0}.gif'.format(cnt) # 스크린샷을 저장할 위치
						elem.screenshot(location) # 스크린샷 저장
						print(cnt)  # cnt 출력
						cnt += 1
					if lowest_elem['elem'].location['y'] < elem.location['y']: # 만약 elem이 lowest_elem보다 더 아래에 있다면
						lowest_elem = {'elem':elem,'height':elem.size['height']}

if __name__ == '__main__':  # main
	email = input('디스코드에 가입된 이메일을 입력해주세요 : ')
	password = input('비밀번호를 입력해주세요 : ')
	bot = Capture_Bot(email, password)  # 박제봇 객체 생성
	sleep(15)  # 10초 지연
	try:
		bot.captuere_image()
	except Exception:
		traceback.print_exc() # 에러 출력

from selenium import webdriver
import time
import random
from PIL import Image
from io import BytesIO
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains




class HuaDong():
	def __init__(self, url, ip=0):
		# 1.url 待测域名   value=srrys.pw
		# 2.代理IP，默认为0，则使用本地IP    格式http://49.4.67.31:3128
		self.url = url
		self.ip = ip
		if self.ip:
			print(self.ip)
			self.chrome_options = webdriver.ChromeOptions()
			self.chrome_options.add_argument('--proxy-server={}'.format(self.ip))
			self.driver = webdriver.Chrome(r'D:\chrome\chromedriver.exe',chrome_options=self.chrome_options)
		else:
			self.driver = webdriver.Chrome(r'D:\chrome\chromedriver.exe')
		self.wait = WebDriverWait(self.driver,5)
		self.action = ActionChains(self.driver)
		self.driver.get('https://ti.qianxin.com/v2/search?type=domain&{}'.format(self.url))

	def get_cut_img(self):
		# 返回有缺口的图片
		time.sleep(3)
		img_b_cut = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]').screenshot_as_png
		with open('cut_img.png','wb') as f:
			f.write(img_b_cut)
		cut_img = Image.open(BytesIO(img_b_cut))
		return cut_img

	def get_full_img(self):
    	# 返回完整的图片
		time.sleep(1)
		js='document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0].style="display:block;"'
		self.driver.execute_script(js)#执行js语句
		time.sleep(3)
		img_b_full = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/canvas').screenshot_as_png
		with open('full_img.png','wb') as f:
			f.write(img_b_full)
		full_img = Image.open(BytesIO(img_b_full))
		return full_img

	def get_distence(self, cut_imt, full_img):
    	# cut_img 有缺口的图片
    	# 完整的图片
    	# 返回距离
		for x in range(65,260):
		    for y in range(116):
		        cut_data = cut_imt.getpixel((x,y))
		        full_data = full_img.getpixel((x,y))
		        for i in range(3):
		            if abs(cut_data[i] - full_data[i]) > 50:
		                print('x={},y={}'.format(x,y))
		                return (x,y)

	def get_track(self, distence):
		# distence 传入需要滑动的距离
		# 返回滑动轨迹
		track=[]
		current = 0
		mid = distance*3/4
		t = random.randint(2,3)/10
		v = 0
		while current < distance:
	          if current < mid:
	             a=2
	          else:
	             a=-3
	          v0=v
	          v=v0+a*t
	          move=v0*t+1/2*a*t*t
	          current+=move
	          track.append(round(move))
		return track

	def move_botton(self, tracks):
		# 滑动轨迹
		button = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="geetest_slider_button"]')))
		time.sleep(2)
		ActionChains(self.driver).click_and_hold(button).perform()
		time.sleep(0.2)
		# 根据轨迹拖拽圆球
		for tra in tracks:
		    ActionChains(self.driver).move_by_offset(xoffset=tra,yoffset=0).perform()
		# 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
		imitate=ActionChains(self.driver).move_by_offset(xoffset=-1, yoffset=0)
		time.sleep(0.015)
		imitate.perform()
		time.sleep(random.randint(6,10)/10)
		imitate.perform()
		time.sleep(0.04)
		imitate.perform()
		time.sleep(0.012)
		imitate.perform()
		time.sleep(0.019)
		imitate.perform()
		time.sleep(0.033)
		ActionChains(self.driver).move_by_offset(xoffset=1, yoffset=0).perform()
		# 放开圆球
		ActionChains(self.driver).pause(random.randint(6,14)/10).release(button).perform()
		time.sleep(2)

if __name__ == '__main__':
	url = 'value=srrys.pw'
	ip = 'http://218.60.8.99:3219'
	hua = HuaDong(url,ip) 
	# hua = HuaDong(url)
	cut_img = hua.get_cut_img()
	full_img = hua.get_full_img()
	x,y = hua.get_distence(cut_img,full_img)
	distance = x - 6
	tracks = hua.get_track(distance)
	hua.move_botton(tracks)
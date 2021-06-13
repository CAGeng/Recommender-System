from logging import exception
import selenium
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        prefs = {"":""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        try:
            cls.driver.get('http://localhost:8080/')
            cls.driver.implicitly_wait(5)
        except selenium.common.exceptions.WebDriverException:
            print("无法访问此网站")
            cls.driver.quit()
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
    # 登录
    def login(self):
        wait = WebDriverWait(self.driver,10)

        self.driver.implicitly_wait(5)
        try:
            dropdownmenu2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(7) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu2).perform()
            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//li[contains(.,\'登录\')]'))).click()
            self.driver.find_element(By.XPATH,"(//input[@type='text'])[2]").send_keys("sft")
            self.driver.find_element(By.XPATH,"//input[@type='password']").send_keys("080090")
            self.driver.find_element(By.XPATH,"//button[contains(.,'登录')]").click()
        except selenium.common.exceptions.TimeoutException:
            print('登录超时')
            
    # 用户注册、登录、修改密码、查看个人信息、登出
    def test_0(self):
        wait = WebDriverWait(self.driver,10)

        self.driver.implicitly_wait(5)
        # 注册
        try:
            dropdownmenu2 = self.driver.find_element_by_css_selector("#app > section > header > div > div:nth-child(7) > i")
            ActionChains(self.driver).move_to_element(dropdownmenu2).perform()
            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'注册')]"))).click()

            wait.until(EC.presence_of_element_located((By.XPATH,'//div[1]/div/div/div/input'))).send_keys("seleniumTest0")
            self.driver.find_element(By.XPATH, "//div[2]/div/div/div/input").send_keys("yinxuanH@163.com")
            self.driver.find_element(By.XPATH, "//div[3]/div/div/div/input").send_keys("123456")
            self.driver.find_element(By.XPATH, "//div[4]/div/div/div/input").send_keys("111111")
            self.driver.find_element(By.XPATH, "//div[5]/div/div/div/input").send_keys("111111")
            self.driver.find_element(By.XPATH, "//span[contains(.,'获取邮箱验证码')]").click()

            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[3]/button'))).click()
            self.driver.find_element(By.XPATH, "//span[contains(.,'返回')]").click()
        except selenium.common.exceptions.TimeoutException:
            print('注册超时')
            self.driver.get('http://localhost:8080/')
            self.driver.implicitly_wait(5)
        
        # 登录
        self.login()

        #查看个人信息
        try:
            sleep(0.5)
            dropdownmenu2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(7) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu2).perform()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'查看个人信息')]"))).click()
            sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//div[3]/span/button/span'))).click()
        except selenium.common.exceptions.TimeoutException:
            print('查看个人信息超时')

        # 修改密码（失败的情况）
        try:
            sleep(0.5)
            dropdownmenu2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(7) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu2).perform()
            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'修改密码')]"))).click()
            self.driver.find_element(By.XPATH,"//input[@type='password']").send_keys("080090a")
            self.driver.find_element(By.XPATH,"(//input[@type='password'])[2]").send_keys("080090b")
            self.driver.find_element(By.XPATH,"(//input[@type='password'])[3]").send_keys("080090b")
            self.driver.find_element(By.XPATH,"//button[contains(.,'确定')]").click()
            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,'//div[2]/div/div[3]/button/span'))).click()
            self.driver.find_element(By.XPATH,"//div[3]/div/div/button/i").click()
        except selenium.common.exceptions.TimeoutException:
            print('修改密码超时')
        
        # 登出
        try:
            sleep(0.5)
            dropdownmenu2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(7) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu2).perform()
            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'登出')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('登出超时')

    # 搜索电影、电影详情、评论、打分、查看浏览记录
    def test_1(self):
        self.login()

        wait = WebDriverWait(self.driver,10)

        # 搜索电影
        try:
            sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/section/header/div/div[2]/div/input'))).send_keys("dark")
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'搜索')]"))).click()
            sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/section/main/div[1]/div/div[1]/header/div[2]/button[2]/span'))).click()
        except selenium.common.exceptions.TimeoutException:
            print('搜索超时')

        # 输入反馈、打分
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH,'//textarea'))).send_keys("great!")
            self.driver.find_element(By.XPATH,"//div[2]/span[4]/i").click()
            self.driver.find_element(By.XPATH,"//button[contains(.,'提交反馈')]").click()

            sleep(1)
            self.driver.find_element(By.XPATH,"//button[contains(.,'返回')]").click()
        except selenium.common.exceptions.TimeoutException:
            print('评分超时')
        
        # 查看浏览记录
        try:
            sleep(0.5)
            dropdownmenu2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(7) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu2).perform()
            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'查看浏览记录')]"))).click()
            self.driver.implicitly_wait(5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'返回')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('查看浏览记录超时')

    # 管理员账号、上传电影
    def test_2(self):
        # self.login()

        wait = WebDriverWait(self.driver,10)

        try:
            sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".el-icon-plus"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'确认上传')]")))
            self.driver.find_element(By.XPATH,"//input[@type='text']").send_keys("Impasse")
            self.driver.find_element(By.XPATH,"(//input[@type='text'])[2]").send_keys("ZhangYi")
            self.driver.find_element(By.XPATH,"//button[contains(.,'新增演员')]").click()
            sleep(0.5)
            self.driver.find_element(By.XPATH,"(//input[@type='text'])[3]").send_keys("QinHailu")
            self.driver.find_element(By.XPATH,"(//input[@type='text'])[4]").send_keys("ZhangYimou")
            self.driver.find_element(By.XPATH,"//span[contains(.,'Action')]").click()
            self.driver.find_element(By.XPATH,"(//input[@type='text'])[5]").send_keys("Wutela")
            wait.until(EC.element_to_be_clickable((By.XPATH,"//span[contains(.,'返回')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('上传电影超时')

    # 推荐电影、收藏影单
    def test_3(self):
        # self.login()

        wait = WebDriverWait(self.driver,10)

        try:
            sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'我的推荐')]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'上传')]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@type='text']"))).send_keys("test")
            sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'取消')]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'返回')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('推荐电影超时')
        
        try:
            sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'收藏影单')]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'影单详情')]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'返回')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('收藏影单超时')
        
        try:
            sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'删除影单')]"))).click()
            sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(.,'返回')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('删除影单超时')

    # 自定义排序
    def test_4(self):
        # self.login()

        wait = WebDriverWait(self.driver,10)

        try:
            sleep(1)
            dropdownmenu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(6) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu).perform()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'综合')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('综合排序超时')
        
        try:
            sleep(1)
            dropdownmenu2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(6) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu2).perform()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'最热门')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('最热门排序超时')
        
        try:
            sleep(1)
            dropdownmenu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#app > section > header > div > div:nth-child(6) > i')))
            ActionChains(self.driver).move_to_element(dropdownmenu).perform()
            wait.until(EC.element_to_be_clickable((By.XPATH,"//li[contains(.,'最相关')]"))).click()
        except selenium.common.exceptions.TimeoutException:
            print('最相关排序超时')

if __name__ == "__main__":
    unittest.main()
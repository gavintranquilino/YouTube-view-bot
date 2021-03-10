from random import randint, choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

class Bot(object):
    """Handle connections"""

    def __init__(self, website):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.website = website  
        self.wait = WebDriverWait(self.driver, 3)
        self.presence = EC.presence_of_element_located
        self.visible = EC.visibility_of_element_located

    def get_vid(self):
        self.driver.get(self.website)
    
    def play_video(self):
        self.wait.until(self.visible((By.ID, "video-title")))
        self.driver.find_element_by_xpath("//button[@class='ytp-large-play-button ytp-button']").click()

    def clear_cache(self):
        self.driver.delete_all_cookies()
    
    def refresh(self):
        self.driver.implicitly_wait(5)
        self.driver.refresh()
    
    def switch_tab(self, tab):
        self.driver.switch_to.window(self.driver.window_handles[tab])
    
    def new_tab(self):
        self.driver.execute_script("window.open('about:blank');")

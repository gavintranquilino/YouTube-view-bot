from os import getcwd
from json import load
from time import sleep
from random import randint, choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Bot(object):
    """Handle connections"""

    def __init__(self, website):
        self.driver = webdriver.Firefox(executable_path=getcwd()+'\\geckodriver.exe')
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

def get_config():
    with open('settings.json', 'r') as file:
        data = load(file)
    
    return data["website"], data["tab_amount"], data["watch_time"], data["view_cycles"]

def init_tabs(website, tab_amount):
    for _ in range(tab_amount):
        website.new_tab()

def open_links(website, tab_amount):
    for tab in range(tab_amount):
        # Open links
        website.switch_tab(tab)
        website.get_vid()

def play_video(website, tab_amount):
    for tab in range(tab_amount):
        # Play the video on each tab
        website.switch_tab(tab)
        website.play_video()

def refresh_all(website, tab_amount):
    for tab in range(tab_amount):
        # Refresh all tabs
        website.switch_tab(tab)
        website.refresh()

def main():
    print('Initilization')
    website, tab_amount, watch_time, view_cycles = get_config()
    website = Bot(website)

    print('Opening new tabs')
    init_tabs(website, tab_amount)

    print('Open links')
    open_links(website, tab_amount)
    
    print('Cycle start')
    print('Playing videos')
    play_video(website, tab_amount)
    for i in range(view_cycles):
        # Cycle the amount of refreshes
        sleep(watch_time) # Watch the video for n amount of times

        print('Refreshing all tabs')
        refresh_all(website, tab_amount)

        print('Clearing cache')
        website.clear_cache() # Clear cache and site cookies
        print(f"Run {i+1}/{view_cycles} complete")
    
    print('Cycles complete')

if __name__ == '__main__':
    main()

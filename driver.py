from random import randint, choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager 
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager

def get_driver(browser):
    """Get the webdriver specified in configuration"""

    # Browser name aliases
    chrome = ('chrome', 'google', 'google chrome', 'googlechrome', 'google-chrome', 'google_chrome')
    firefox = ('firefox', 'ff', 'mozilla', 'gecko', 'geckodriver', 'fire fox', 'fire_fox', 'fire-fox')
    opera = ('opera', 'opera gx', 'operagx', 'opera_gx', 'opera-gx')
    explorer = ('explorer', 'ie', 'internet explorer', 'internet-explorer', 'internet_explorer')
    edge = ('edge', 'microsoft edge', 'microsoft_edge', 'microsoft-edge')

    # Download browser binaries according to settings.json
    if browser.lower() in chrome:
        return webdriver.Chrome(ChromeDriverManager().install())

    elif browser.lower() in firefox:
        return webdriver.Firefox(executable_path=GeckoDriverManager().install())

    elif browser.lower() in opera:
        return webdriver.Opera(OperaDriverManager().install())

    elif browser.lower() in explorer:
        return webdriver.Ie(IEDriverManager().install())

    elif browser.lower() in edge:
        return webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())

    else:
        raise RuntimeError('Browser not found {}'.format(browser.lower()))


class Bot(object):
    """Handle connections"""

    def __init__(self, website, browser):
        """Initial function"""

        self.driver = get_driver(browser)
        self.website = website  
        self.wait = WebDriverWait(self.driver, 3)
        self.presence = EC.presence_of_element_located
        self.visible = EC.visibility_of_element_located

    def get_vid(self):
        """Open the YouTube link"""

        self.driver.get(self.website)
    
    def play_video(self):
        """Click on the play button"""

        self.wait.until(self.visible((By.ID, "video-title")))
        self.driver.find_element_by_xpath("//button[@class='ytp-large-play-button ytp-button']").click()

    def clear_cache(self):
        """Clear the cache"""

        self.driver.delete_all_cookies()
    
    def refresh(self):
        """Refresh the current tab"""

        self.driver.implicitly_wait(5)
        self.driver.refresh()
    
    def switch_tab(self, tab):
        """Switch to the specified tab"""

        self.driver.switch_to.window(self.driver.window_handles[tab])
    
    def new_tab(self):
        """Open a blank new tab"""
        
        self.driver.execute_script("window.open('about:blank');")

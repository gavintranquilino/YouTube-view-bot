from random import randint, choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    InvalidSessionIdException,
    NoSuchWindowException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager 
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.edge.service import Service as EdgeService

def get_driver(browser):
    """Get the webdriver specified in configuration"""

    # Browser name aliases
    chrome = ('chrome', 'google', 'google chrome', 'googlechrome', 'google-chrome', 'google_chrome')
    firefox = ('firefox', 'ff', 'mozilla', 'gecko', 'geckodriver', 'fire fox', 'fire_fox', 'fire-fox')
    explorer = ('explorer', 'ie', 'internet explorer', 'internet-explorer', 'internet_explorer')
    edge = ('edge', 'microsoft edge', 'microsoft_edge', 'microsoft-edge')

    # Download browser binaries according to settings.json
    if browser.lower() in chrome:
        # Prefer built-in Selenium Manager; fallback to webdriver_manager only if needed
        try:
            return webdriver.Chrome()
        except Exception:
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service)

    elif browser.lower() in firefox:
        try:
            return webdriver.Firefox()
        except Exception:
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service)

    elif browser.lower() in explorer:
        try:
            return webdriver.Ie()
        except Exception:
            service = IEService(IEDriverManager().install())
            return webdriver.Ie(service=service)

    elif browser.lower() in edge:
        try:
            return webdriver.Edge()
        except Exception:
            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service)

    else:
        raise RuntimeError('Browser not found {}. Supported: Chrome, Firefox, Edge, IE'.format(browser.lower()))


class Bot(object):
    """Handle connections"""

    def __init__(self, website, browser, tab_amount=1):
        """Initial function"""

        self.browser = browser
        self.tab_amount = tab_amount
        self.driver = get_driver(browser)
        self.website = website
        # Allow slower page loads/overlays before timing out
        self.wait = WebDriverWait(self.driver, 20)
        self.presence = EC.presence_of_element_located
        self.visible = EC.visibility_of_element_located

    def get_vid(self):
        """Open the YouTube link"""

        self.driver.get(self.website)
        self._accept_cookies()

    def play_video(self):
        """Click on the play button"""

        # Ensure we are on the desired video (avoid autoplay chaining to another video)
        if self.website not in self.driver.current_url:
            self.driver.get(self.website)

        # Wait for player to be ready and ensure play button is clickable
        self._accept_cookies()
        self.wait.until(self.presence((By.TAG_NAME, "video")))
        self._dismiss_overlays()
        if not self._click_play_button():
            # Fallback: try to start video via JS if button not found/clickable
            self.driver.execute_script("""
                const v = document.querySelector('video');
                if (v) { v.muted = false; v.play().catch(()=>{}); }
            """)

    def _dismiss_overlays(self):
        """Attempt to close common YouTube overlays such as cookie consent backdrops."""

        # Remove overlay backdrops that block clicks
        self.driver.execute_script(
            "document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove());"
        )

        # Try to click consent buttons if present
        consent_selectors = [
            "//button[normalize-space()='I agree']",
            "//button[normalize-space()='Accept all']",
            "//button[normalize-space()='Alle akzeptieren']",
            "//button[normalize-space()='Ich stimme zu']",
        ]

        for selector in consent_selectors:
            try:
                btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                btn.click()
                break
            except TimeoutException:
                continue

    def _accept_cookies(self):
        """Accept YouTube/Google cookie banners if present."""

        consent_selectors = [
            "//button[normalize-space()='I agree']",
            "//button[normalize-space()='Accept all']",
            "//button[normalize-space()='Alle akzeptieren']",
            "//button[normalize-space()='Ich stimme zu']",
            "//button[normalize-space()='Zustimmen und fortfahren']",
            "//button[@aria-label='Accept all']",
            "//button[@aria-label='Alle akzeptieren']",
        ]

        try:
            WebDriverWait(self.driver, 5).until(lambda d: True)
            for selector in consent_selectors:
                buttons = self.driver.find_elements(By.XPATH, selector)
                for btn in buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        btn.click()
                        return
        except Exception:
            # If anything goes wrong, just proceed; the overlay handler will try again.
            pass

    def _get_play_button(self):
        """Return a clickable play button element if available."""

        try:
            return self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-play-button")))
        except TimeoutException:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, ".ytp-play-button")
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    return btn
        return None

    def _click_play_button(self):
        """Try clicking the play button with retries to avoid stale references."""

        for _ in range(3):
            btn = self._get_play_button()
            if not btn:
                continue
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", btn
                )
                self.driver.execute_script("arguments[0].click();", btn)
                return True
            except (StaleElementReferenceException, ElementClickInterceptedException):
                self._dismiss_overlays()
                continue
        return False

    def clear_cache(self):
        """Clear the cache"""

        self.driver.delete_all_cookies()
    
    def refresh(self):
        """Refresh the current tab"""

        # Reload the intended video instead of refreshing whatever autoplay selected
        self.driver.implicitly_wait(5)
        self.driver.get(self.website)
        self._accept_cookies()
    
    def switch_tab(self, tab):
        """Switch to the specified tab"""

        try:
            self.driver.switch_to.window(self.driver.window_handles[tab])
        except (InvalidSessionIdException, NoSuchWindowException, IndexError):
            # Browser/tab closed or session lost; try to rebuild session so script does not exit
            self._restart_session()
            try:
                self.driver.switch_to.window(self.driver.window_handles[tab])
            except Exception:
                pass
    
    def new_tab(self):
        """Open a blank new tab"""
        
        self.driver.execute_script("window.open('about:blank');")

    def _restart_session(self):
        """Rebuild the browser session if it was lost."""

        try:
            self.driver.quit()
        except Exception:
            pass

        self.driver = get_driver(self.browser)
        self.wait = WebDriverWait(self.driver, 20)

        # Reopen tabs and load the target website in each
        handles_needed = max(self.tab_amount, 1)
        # Open first tab and load
        self.driver.get(self.website)
        self._accept_cookies()

        # Create remaining tabs
        for _ in range(handles_needed - 1):
            self.new_tab()

        # Load website in every tab
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            self.driver.get(self.website)
            self._accept_cookies()

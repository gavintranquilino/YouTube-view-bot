from json import load
from time import sleep
import driver

def get_config():
    """Read configuration file"""

    try:
        with open('default.json', 'r') as file:
            data = load(file)

    except FileNotFoundError:
        with open('config.json', 'r') as file:
            data = load(file)
    
    return data

def init_tabs(website, tab_amount):
    """Opens tabs according to tab amount set in config.json"""

    for _ in range(tab_amount):
        website.new_tab()

def open_links(website, tab_amount):
    """Open the YouTube link in each tab"""

    for tab in range(tab_amount):
        # Open links
        website.switch_tab(tab)
        website.get_vid()

def play_video(website, tab_amount):
    """Click on the play button"""

    for tab in range(tab_amount):
        # Play the video on each tab
        website.switch_tab(tab)
        website.play_video()

def refresh_all(website, tab_amount):
    """Refresh all tabs"""

    for tab in range(tab_amount):
        # Refresh all tabs
        website.switch_tab(tab)
        website.refresh()

def main():
    """Main Function"""

    print('Initilization')
    config = get_config()

    website = driver.Bot(config['website'], config['browser'])

    print('Opening new tabs')
    init_tabs(website, config['tab_amount'])

    print('Open links')
    open_links(website, config['tab_amount'])
    
    print('Cycle start')
    print('Playing videos')
    play_video(website, config['tab_amount'])

    for i in range(config['view_cycles']):

        # Cycle the amount of refreshes
        sleep(config['watch_time']) # Watch the video for n amount of times

        print('Refreshing all tabs')
        refresh_all(website, config['tab_amount'])

        print('Clearing cache')
        website.clear_cache() # Clear cache and site cookies
        print(f"Run {i+1}/{config['view_cycles']} complete")
    
    print('Complete')

if __name__ == '__main__':
    main()

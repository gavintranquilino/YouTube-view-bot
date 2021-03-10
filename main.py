from json import load
import driver

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
    website = driver.Bot(website)

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

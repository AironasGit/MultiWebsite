import winreg
import subprocess
import time


def get_list_of_links(path):
    list_of_links = []
    with open(path, "r") as f:
        file = f.readlines()
        for line in file:
            list_of_links.append(line.strip()) # Remove '/n'
    return list_of_links


def windows_get_default_browser():
    key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice")
    prog_id, _ = winreg.QueryValueEx(key, "ProgId")
    key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE), r"SOFTWARE\Classes\{}\shell\open\command".format(prog_id))
    launch_string, _ = winreg.QueryValueEx(key, "")  # read the default value
    return launch_string.split('"')[1]


def open_first_tab(window_mode, default_browser, list_of_links):
    if window_mode == "-new-window":
        subprocess.call([default_browser, window_mode , list_of_links[0]])
        list_of_links.pop(0)
        window_mode = "-new-tab"
    return window_mode

def main():
    # Settings
    window_mode = "-new-window" # -new-tab, -new-window
    location_of_links = "list_of_websites.txt"
    # Settings
    
    list_of_links = get_list_of_links(location_of_links)
    default_browser = windows_get_default_browser()
    
    match default_browser.split("\\")[-1]:
        case "firefox.exe":
            window_mode = open_first_tab(window_mode, default_browser, list_of_links)
            for link in list_of_links:
                time.sleep(0.5) # Firefox browser opens an empty tab if there is no delay
                subprocess.call([default_browser, window_mode , link])
        case "chrome.exe":
            window_mode = open_first_tab(window_mode, default_browser, list_of_links)
            for link in list_of_links:
                subprocess.call([default_browser, window_mode , link])
        case "msedge.exe":
            window_mode = open_first_tab(window_mode, default_browser, list_of_links)
            for link in list_of_links:
                subprocess.call([default_browser, window_mode , link])
        case "iexplore.exe":
            ...


if __name__ == "__main__":
    main()

'''
Chrome +
Edge +
Firefox +
Explorer -
Other ?
'''
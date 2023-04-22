import sys
import winreg
import subprocess


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


def build_arg(window, list_of_links):
    arg = window
    for link in list_of_links:
        arg = f'{arg} {link}'
    return arg


def main():
    # Settings
    window_mode = "--new-window" # --parent-window (opens links in the current browser window) --new-window (opens links in new browser window)
    location_of_links = "list_of_websites.txt"
    # Settings
    list_of_links = get_list_of_links(location_of_links)
    default_browser = windows_get_default_browser()
    arg = build_arg(window_mode, list_of_links)
    print(arg)
    subprocess.call([default_browser, arg])


if __name__ == "__main__":
    main()

'''
Chrome +
Edge +
Firefox -
Explorer -
other ?
'''
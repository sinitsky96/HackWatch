from time import sleep

import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scrollDown(browser):
    SCROLL_PAUSE_TIME = 0.5
    for i in range(2):

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    sleep(4)
    body = browser.find_element(by=By.ID, value='facebook')
    return body.text


def hackWatch(mail, passw):
    chrome_options = ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("--disable-notifications")

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    browser.get("http://www.facebook.com")
    sleep(2)

    email = browser.find_element(by=By.ID, value="email")
    password = browser.find_element(by=By.ID, value="pass")
    email.send_keys(mail)

    password.send_keys(passw)
    sleep(1)
    login = browser.find_element(by=By.NAME, value="login")
    login.click()
    sleep(1)
    browser.get("https://www.facebook.com/groups/118649778226975")
    data = scrollDown(browser)
    search = ["האקטון", "הקאתון", "hack", "hackathon"]
    for term in search:
        if term in data:
            success()
            browser.quit()
    fail()
    browser.quit()


def start():
    layout = [[sg.Text("HackWatch", size=(15, 3))],
              [sg.Text("Email"), sg.In(size=(25, 1), enable_events=True, key="-EMAIL-")],
              [sg.Text("Password"), sg.In(size=(20, 1), enable_events=True, key="-PASS-")], [sg.Button("OK")]]

    # Create the window
    window = sg.Window("Demo", layout)

    # Create an event loop

    while True:
        event, values = window.read()

        # End program if user closes window or
        # presses the OK button
        if event == "OK":
            window.close()
            hackWatch(values["-EMAIL-"], values["-PASS-"])
        if event == sg.WIN_CLOSED:
            break
    window.close()


def success():
    sg.Popup('Great Success!!', keep_on_top=True)


def fail():
    sg.Popup('WAWAWIWA :(', keep_on_top=True)


start()

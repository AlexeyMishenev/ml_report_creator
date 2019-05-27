#! /usr/bin/env python3

import json
import os
from os.path import dirname, exists, join
from time import sleep

from PIL import Image
from selenium import webdriver

from credentials import Credentials


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    dr = webdriver.Chrome('./chromedriver', options=options)
    dr.maximize_window()
    dr.fullscreen_window()

    return dr


def login():
    driver.get(datacamp["sign_in"])
    user_email = driver.find_element_by_id('user_email')
    user_email.send_keys(Credentials.user_email)

    driver.find_element_by_css_selector(".dc-account-modal__next-btn").click()
    sleep(1)

    password = driver.find_element_by_id('user_password')
    password.send_keys(Credentials.user_password)

    form = driver.find_element_by_id('new_user')
    form.submit()
    sleep(2)


def take_screenshots():
    base_url = datacamp["base_url"]

    for c_name, course in datacamp["courses"].items():
        for p_name, part in course.items():
            for ex in range(1, part["ex"] + 1):
                url = f"{base_url}/{c_name}/{p_name}?ex={ex}"
                file = join("images", c_name, p_name, f"{ex}.png")
                if not exists(dirname(file)):
                    os.makedirs(dirname(file))
                driver.get(url)
                sleep(2)
                driver.save_screenshot(file)


def save_pdf(output):
    images = []
    for c_name, course in datacamp["courses"].items():
        for p_name, part in course.items():
            for ex in range(1, part["ex"] + 1):
                file = join("images", c_name, p_name, f"{ex}.png")
                if exists(file):
                    images.append(file)

    pil_img = [Image.open(i).convert('RGB') for i in images]

    pil_img[0].save(output, "PDF", resolution=100.0, save_all=True, append_images=pil_img[1:])


if __name__ == '__main__':
    with open("datacamp.json") as fd:
        datacamp = json.load(fd)

    driver = get_driver()

    login()
    take_screenshots()

    driver.quit()

    save_pdf("datacamp.pdf")

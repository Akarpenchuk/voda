# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import time

success = True
wd = WebDriver()
wd.implicitly_wait(60)

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

try:
    wd.get("http://kv-mmc-ais01.mts.com.ua:4450/")
    wd.find_element_by_id("tbUserName").click()
    wd.find_element_by_id("tbUserName").clear()
    wd.find_element_by_id("tbUserName").send_keys("akarpenchuk")
    wd.find_element_by_id("tbPassword").click()
    wd.find_element_by_id("tbPassword").clear()
    wd.find_element_by_id("tbPassword").send_keys("")
    wd.find_element_by_id("btnLogin").click()
    wd.find_element_by_xpath("//div[@id='zz14_TopNavigationMenuV4']//span[.='ЦКУ']").click()
    wd.find_element_by_xpath("//div[@id='zz15_V4QuickLaunchMenu']/div/ul/li[2]/a/span/span").click()
    wd.find_element_by_xpath("//div[@id='zz15_V4QuickLaunchMenu']/div/ul/li[2]/ul/li[3]/a/span/span").click()
finally:
    wd.quit()
    if not success:
        raise Exception("Test failed.")

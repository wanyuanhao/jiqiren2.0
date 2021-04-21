# -*- coding:utf-8 -*-
from selenium import webdriver
import unittest
from time import sleep

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http:\\userssodev.91bihu.me")
driver.implicitly_wait(5)
driver.find_element_by_id("userName").send_keys("niepan45")
driver.find_element_by_id("Password").send_keys("91bihu.com")
sleep(8)
class TestCaseUI(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        driver.quit()

    def test01(self):
        "打印用户名"
        sleep(3)
        user_name = driver.find_element_by_css_selector("#app > section > section > header > div > div.el-col.el-col-22 > div > div.operate > a > span")
        print(user_name.text)
    def test02(self):
        "打印车牌"
        driver.find_elements_by_class_name("el-submenu__title")[0].click()
        sleep(0.5)
        driver.find_element_by_css_selector("#app > section > aside > ul > li.el-submenu.is-opened > ul > li:nth-child(1) > a").click()
        sleep(5)
        license =driver.find_element_by_css_selector("#app > section > section > main > div > div > div.loading-other-style.ant-spin-nested-loading > div > div > div:nth-child(1) > div > div.el-table__fixed > div.el-table__fixed-body-wrapper > table > tbody > tr:nth-child(2) > td.el-table_5_column_66.tabel-col > div > a").click()
        print(license.text)

if __name__ == '__main__':
    unittest.main()





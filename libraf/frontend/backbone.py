# -*- coding:utf-8 -*-

from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import unittest

URL = "http://192.168.5.161:9000/"

#login
R_UNAME = "admin" #正确登录用户名
R_PWD = "admin123" #正确登录密码
W_UNAME = "admin11111111111" #错误登录用户名
W_PWD = "admin111111111111111" #错误登录密码
#change user password
UNAME = "test1" #修改用户密码
OLDPWD = "admin123" #输入正确的旧密码
NEWPWD = "admin12345" #输入格式正确的新密码
W_OLDPWD = "a" #输入格式错误的旧密码
W_NEWPWD = "1" #输入格式错误的新密码
#create new user
NEW_USER = "test2" #创建新的用户
NEW_PWD = "admin1234" #新用户的密码
CONFIRMPWD_NOT_MATCH = "admin12" #确认密码与新密码不符

browser = webdriver.Chrome()

#browser = webdriver.Ie()

#browser = webdriver.Firefox()

class TestLoginAndLogout(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        browser.get(URL+"login")
        browser.implicitly_wait(30)
        browser.maximize_window()

    @classmethod
    def tearDownClass(self):
        pass

    def test01_username_password_null(self):
        print "#"*10 + u"case:用户名和密码为空" + "#"*10
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        err_msg = browser.find_element_by_class_name("err-msg").text
        print u"提示语:"+err_msg
        self.assertEqual(err_msg,u"用户名或密码不能为空. 请输入用户名 请输入密码")

    def test02_username_null(self):
        print "#"*10 + u"case:用户名为空" + "#"*10
        browser.find_element_by_id("password").send_keys(R_PWD)
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        err_msg = browser.find_element_by_class_name("err-msg").text
        print u"提示语:"+err_msg
        self.assertEqual(err_msg,u"用户名或密码不能为空. 请输入用户名")

    def test03_password_null(self):
        print "#"*10 + u"case:密码为空" + "#"*10
        browser.find_element_by_id("username").send_keys(R_UNAME)
        browser.find_element_by_id("password").clear()
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        err_msg = browser.find_element_by_class_name("err-msg").text
        print u"提示语:"+err_msg
        self.assertEqual(err_msg,u"用户名或密码不能为空. 请输入密码")
    
    def test04_username_password_wrong(self):
        print "#"*10 + u"case:用户名和密码错误" + "#"*10
        browser.find_element_by_id("username").clear()
        browser.find_element_by_id("username").send_keys(W_UNAME)
        browser.find_element_by_id("password").clear()
        browser.find_element_by_id("password").send_keys(W_PWD)
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        err_msg = browser.find_element_by_class_name("err-msg").text
        print u"提示语:"+err_msg
        self.assertEqual(err_msg,u"用户不存在")

    def test05_username_wrong(self):
        print "#"*10 + u"case:用户名错误" + "#"*10
        browser.find_element_by_id("username").clear()
        browser.find_element_by_id("username").send_keys(W_UNAME)
        browser.find_element_by_id("password").clear()
        browser.find_element_by_id("password").send_keys(R_PWD)
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        err_msg = browser.find_element_by_class_name("err-msg").text
        print u"提示语:"+err_msg
        self.assertEqual(err_msg,u"用户不存在")

    def test06_password_wrong(self):
        print "#"*10 + u"case:密码错误" + "#"*10
        browser.find_element_by_id("username").clear()
        browser.find_element_by_id("username").send_keys(R_UNAME)
        browser.find_element_by_id("password").clear()
        browser.find_element_by_id("password").send_keys(W_PWD)
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        err_msg = browser.find_element_by_class_name("err-msg").text
        print u"提示语:"+err_msg
        self.assertEqual(err_msg,u"账号或者密码错误")

    def test07_username_password_right(self):
        print "#"*10 + u"case:用户名和密码正确" + "#"*10
        browser.find_element_by_id("username").clear()
        browser.find_element_by_id("username").send_keys(R_UNAME)
        browser.find_element_by_id("password").clear()
        browser.find_element_by_id("password").send_keys(R_PWD)
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        #browser.add_cookie({'name':R_UNAME,'value':R_PWD, 'path':'/'})
        #browser.get(URL)

        #data = browser.find_element_by_xpath("//ul[@class='dropdown-menu']/a[@href='logout']").text
        #if data:
            #print u"登录成功"
        #self.assertEqual(data,u"退出")
        current_url = browser.current_url
        self.assertEqual(current_url,URL)

    def test08_logout(self):
        print "#"*10 + u"case:退出登录" + "#"*10
        browser.find_element_by_class_name("dropdown").click()
        time.sleep(2)
        menu = browser.find_element_by_class_name("dropdown-menu").find_element_by_link_text(u"退出")
        webdriver.ActionChains(browser).move_to_element(menu).perform()
        time.sleep(2)
        menu.click()
        time.sleep(2)
        current_url = browser.current_url
        if current_url == URL+"login":
            print u"退出登录成功"
        self.assertEqual(current_url,URL+"login")
        
class TestChangeAdminPassword(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        browser.get(URL+"login")
        browser.find_element_by_id("username").send_keys("admin")
        browser.find_element_by_id("password").send_keys("admin123")
        browser.find_element_by_class_name("login_btn").submit()    

    @classmethod
    def tearDonwClass(self):
        pass       

    def test01_change_password_admin(self):
        print "#"*10 + u"case:修改管理员密码" + "#"*10
        time.sleep(2)
        browser.find_element_by_class_name("dropdown-ico").click()
        browser.find_element_by_class_name("dropdown-menu").find_element_by_link_text(u"修改密码").click()
        data = browser.find_element_by_class_name("bkb-tip-content").text
        print u"闪现提示语："+data
        self.assertEqual(data,u"管理员不能修改密码")

class TestChangeUserPassword(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global menu_old,menu_new,menu_confirm
        browser.get(URL+"login")
        browser.find_element_by_id("username").send_keys(UNAME)
        browser.find_element_by_id("password").send_keys(OLDPWD)
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        browser.find_element_by_class_name("dropdown-ico").click()
        time.sleep(2)
        browser.find_element_by_class_name("dropdown-menu").find_element_by_link_text(u"修改密码").click()
        menu_old = browser.find_element_by_name("oldpwd")
        menu_new = browser.find_element_by_name("newpwd")
        menu_confirm = browser.find_element_by_name("confirmpwd")

    @classmethod
    def tearDonwClass(self):
        pass      

    def test01_default_display(self):
        print "#"*10 + u"case:用户修改密码页面默认检查" + "#"*10
        datas = browser.find_elements_by_tag_name("input")
        for data in datas:
            if data.get_attribute("name") == "oldpwd":
                olddata = data.get_attribute("placeholder")
                print u"旧密码输入框浅色提示语："+olddata
            if data.get_attribute("name") == "newpwd":
                newdata = data.get_attribute("placeholder")
                print u"新密码输入框浅色提示语："+newdata
            if data.get_attribute("name") == "confirmpwd":
                confirmdata = data.get_attribute("placeholder")
                print u"确认密码输入框浅色提示语："+confirmdata
        data = browser.find_element_by_tag_name("p").text
        print u"密码格式提示："+data
        data1 = browser.find_element_by_tag_name("button").get_attribute("disabled")
        print u"保存按钮是否可用："+data1
        self.assertEqual(olddata,u"请输入旧密码")
        self.assertEqual(newdata,u"请输入新密码")
        self.assertEqual(confirmdata,u"请再次输入新密码")
        self.assertEqual(data,u"密码可以为6-20位英文字母、数字或符号, 至少同时包含字母或数字, 字母区分大小写")
        self.assertEqual(data1,"true")

    def test02_oldpwd_null(self):
        print "#"*10 + u"case:旧密码为空" + "#"*10
        menu_old.clear()
        webdriver.ActionChains(browser).move_to_element(menu_new).click().perform()
        time.sleep(2)
        datas = browser.find_elements_by_class_name("col-sm-4")
        data = datas[0].text
        print u"提示语："+data
        buttondata = browser.find_element_by_tag_name("button").get_attribute("disabled")
        print u"保存按钮是否置灰："+buttondata
        self.assertEqual(data,u"× 旧密码不能为空")
        self.assertEqual(buttondata,"true")

    def test03_newpwd_null(self):
        print "#"*10 + u"case:新密码为空" + "#"*10
        menu_old.send_keys(OLDPWD)
        menu_new.clear()
        webdriver.ActionChains(browser).move_to_element(menu_confirm).click().perform()
        time.sleep(2)
        datas = browser.find_elements_by_class_name("col-sm-4")
        data = datas[1].text
        print u"提示语："+data
        buttondata = browser.find_element_by_tag_name("button").get_attribute("disabled")
        print u"保存按钮是否置灰："+buttondata
        self.assertEqual(data,u"× 新密码不能为空")
        self.assertEqual(buttondata,"true")

    def test04_confirmpwd_null(self):
        print "#"*10 + u"case:确认密码为空" + "#"*10
        menu_old.clear()
        menu_old.send_keys(OLDPWD)
        menu_new.clear()
        menu_new.send_keys(NEWPWD)
        menu_confirm.clear()
        webdriver.ActionChains(browser).move_to_element(menu_new).click().perform()
        time.sleep(2)
        datas = browser.find_elements_by_class_name("col-sm-4")
        data = datas[2].text
        print u"提示语："+data
        buttondata = browser.find_element_by_tag_name("button").get_attribute("disabled")
        print u"保存按钮是否置灰："+buttondata
        self.assertEqual(data,u"× 确认密码不能为空 × 密码输入不一致")
        self.assertEqual(buttondata,"true")
        

    def test05_oldpwd_wrong(self):
        print "#"*10 + u"case:旧密码错误" + "#"*10
        menu_old.send_keys(W_OLDPWD)
        menu_new.clear()
        menu_new.send_keys(NEWPWD)
        menu_confirm.clear()
        menu_confirm.send_keys(NEWPWD)
        buttondata = browser.find_element_by_tag_name("button").get_attribute("disabled")
        if buttondata == None:
            browser.find_element_by_tag_name("button").submit()
        else:
            print u"保存按钮不可点击"
        time.sleep(2)
        datas = browser.find_elements_by_class_name("col-sm-4")
        data = datas[0].text
        print u"提示语："+data
        self.assertEqual(data,u"× 密码输入错误")
        
            
        '''
        datas = browser.find_elements_by_tag_name("span")
        olddata = datas[-5].text
        print olddata
        data1 = datas[-1].get_attribute("class")
        print data1
        data2 = datas[-3].get_attribute("class")
        print data2
        self.assertEqual(buttondata,None)
        self.assertEqual(olddata,u"× 密码输入错误")
        self.assertEqual(data1,"glyphicon glyphicon-ok")
        self.assertEqual(data2,"glyphicon glyphicon-ok")'''

    def test06_newpwd_wrong(self):
        print "#"*10 + u"case:新密码格式错误" + "#"*10
        menu_old.clear()
        menu_old.send_keys(OLDPWD)
        menu_new.clear()
        menu_new.send_keys(W_NEWPWD)
        webdriver.ActionChains(browser).move_to_element(menu_confirm).click().perform()
        time.sleep(2)
        datas = browser.find_elements_by_class_name("col-sm-4")
        data = datas[1].text
        print u"提示语："+data
        buttondata = browser.find_element_by_tag_name("button").get_attribute("disabled")
        print u"保存按钮是否置灰："+buttondata
        self.assertEqual(data,u"× 密码格式错误")
        self.assertEqual(buttondata,"true")
        
    def test07_newpwd_confirmpwd_not_match(self):
        print "#"*10 + u"case:确认密码与新密码不一致" + "#"*10
        menu_old.clear()
        menu_old.send_keys(OLDPWD)
        menu_new.clear()
        menu_new.send_keys(NEWPWD)
        menu_confirm.clear()
        menu_confirm.send_keys(W_NEWPWD)
        #browser.find_element_by_tag_name("button").submit()
        webdriver.ActionChains(browser).move_to_element(menu_new).click().perform()
        time.sleep(2)
        datas = browser.find_elements_by_class_name("col-sm-4")
        data = datas[2].text
        print u"提示语："+data
        buttondata = browser.find_element_by_tag_name("button").get_attribute("disabled")
        print u"保存按钮是否置灰："+buttondata
        self.assertEqual(data,u"× 密码输入不一致")
        self.assertEqual(buttondata,"true")
                

    def test08_change_password_success(self):
        print "#"*10 + u"case:修改密码成功" + "#"*10
        menu_old.clear()
        menu_old.send_keys(OLDPWD)
        menu_new.clear()
        menu_new.send_keys(NEWPWD)
        menu_confirm.clear()
        menu_confirm.send_keys(NEWPWD)
        buttondata1 = browser.find_element_by_tag_name("button").get_attribute("disabled")
        if buttondata1 == None:
            browser.find_element_by_tag_name("button").submit()
        else:
            print u"错误：保存按钮不可用！"
        time.sleep(1)
        data = browser.find_element_by_class_name("err_form").text.split("\n")[0]
        print u"密码修改成功提示："+data
        browser.find_element_by_link_text(u"确认").click()
        time.sleep(2)
        print u"当前url："+browser.current_url
        buttondata = browser.find_element_by_tag_name("button").text
        self.assertEqual(buttondata1,None)
        self.assertEqual(data,u"密码修改成功，请返回登录界面登录")
        self.assertEqual(buttondata,u"登录")
        self.assertEqual(browser.current_url,URL+"login")

class TestUserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print "#"*10 + u"用户身份登录" + "#"*10
        browser.get(URL+"login")
        browser.find_element_by_id("username").send_keys(UNAME)
        browser.find_element_by_id("password").send_keys(NEWPWD)
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        
    @classmethod
    def tearDonwClass(self):
        pass

    def test01_create_new_user(self):
        print "#"*10 + u"case:检查创建用户按钮" + "#"*10
        buttondata = browser.find_element_by_tag_name("button").get_attribute("class").split()[-1]
        print u"\"创建用户\"按钮是否可用："+buttondata
        self.assertEqual(buttondata,"disabled")

    def test02_delete_user(self):
        print "#"*10 + u"case:检查删除用户按钮" + "#"*10
        datas = browser.find_elements_by_tag_name("a")
        for data in datas:
            text = data.text
            if text == u"删除":
                value = data.get_attribute("class")
                print u"删除是否可用："+value
        self.assertEqual(value,"disabled")
        browser.find_element_by_class_name("dropdown-ico").click()
        time.sleep(2)
        menu = browser.find_element_by_class_name("dropdown-menu").find_element_by_link_text(u"退出").click()

class TestUserManagementAdmin(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print "#"*10 + u"管理员身份登录" + "#"*10
        browser.get(URL+"login")
        browser.find_element_by_id("username").send_keys("admin")
        browser.find_element_by_id("password").send_keys("admin123")
        browser.find_element_by_class_name("login_btn").submit()
        time.sleep(2)
        
    @classmethod
    def tearDonwClass(self):
        pass

    def test01_create_new_user_button(self):
        print "#"*10 + u"case:创建新用户" + "#"*10
        menu = browser.find_element_by_tag_name("button")
        buttondata = menu.get_attribute("class").split()[-1]
        print u"\"创建用户\"按钮是否可用："+buttondata
        menu.click()
        time.sleep(2)
        modallabel = browser.find_element_by_class_name("modal-title").text
        print u"弹窗标题："+modallabel
        status = browser.find_element_by_id("createUser").get_attribute("style").split(":")[1][1:-1]
        print u"创建用户弹窗是否存在："+status
        self.assertEqual(buttondata,"enabled")
        self.assertEqual(modallabel,u"创建新用户")
        self.assertEqual(status,"block")

    def test02_close_button(self):
        print "#"*10 + u"case:创建新用户弹窗关闭按钮" + "#"*10
        #browser.find_element_by_tag_name("button").click()
        browser.find_element_by_class_name("modal-header").find_element_by_tag_name("button").click()
        time.sleep(2)
        status = browser.find_element_by_id("createUser").get_attribute("style").split(":")[1][1:-1]
        print u"创建用户弹窗是否存在："+status
        self.assertEqual(status,"none")

    def test03_cancel_button(self):
        print "#"*10 + u"case:创建新用户弹窗取消按钮" + "#"*10
        browser.find_element_by_tag_name("button").click()
        time.sleep(2)
        buttondatas = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")
        confirmbutton = buttondatas[0].click()
        time.sleep(2)
        status = browser.find_element_by_id("createUser").get_attribute("style").split(":")[1][1:-1]
        print u"创建用户弹窗是否存在："+status
        self.assertEqual(status,"none")

    def test04_username_null(self):
        print "#"*10 + u"case:创建新用户 用户名为空" + "#"*10
        browser.find_element_by_tag_name("button").click()
        time.sleep(2)
        browser.find_element_by_name("username").clear()
        menu = browser.find_element_by_name("newpwd")
        webdriver.ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
        data = browser.find_elements_by_class_name("form-group")[0].find_element_by_tag_name("span").text
        print u"提示语："+data
        buttondatas = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")
        confirmbutton = buttondatas[1].get_attribute("disabled")
        print u"保存按钮是否置灰："+confirmbutton
        self.assertEqual(data,u"用户名不能为空")
        self.assertEqual(confirmbutton,"true")

    def test05_password_null(self):
        print "#"*10 + u"case:创建新用户 密码为空" + "#"*10
        browser.find_element_by_name("username").clear()
        browser.find_element_by_name("username").send_keys(NEW_USER)
        browser.find_element_by_name("newpwd").clear()
        menu = browser.find_elements_by_name("newpwd")[1]
        webdriver.ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
        data = browser.find_elements_by_class_name("form-group")[1].find_element_by_tag_name("span").text
        print u"提示语："+data
        buttondatas = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")
        confirmbutton = buttondatas[1].get_attribute("disabled")
        print u"保存按钮是否置灰："+confirmbutton
        self.assertEqual(data,u"密码不能为空")
        self.assertEqual(confirmbutton,"true")

    def test06_confirmpwd_null(self):
        print "#"*10 + u"case:创建新用户 确认密码为空" + "#"*10
        browser.find_element_by_name("username").clear()
        browser.find_element_by_name("username").send_keys(NEW_USER)
        browser.find_element_by_name("newpwd").clear()
        browser.find_element_by_name("newpwd").send_keys(NEW_PWD)
        browser.find_elements_by_name("newpwd")[1].clear()
        menu = browser.find_element_by_name("newpwd")
        webdriver.ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
        data = browser.find_elements_by_class_name("form-group")[2].find_element_by_tag_name("span").text
        print u"提示语："+data
        buttondatas = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")
        confirmbutton = buttondatas[1].get_attribute("disabled")
        print u"保存按钮是否置灰："+confirmbutton
        self.assertEqual(data,u"密码输入不一致")
        self.assertEqual(confirmbutton,"true")

    def test07_password_wrong(self):
        print "#"*10 + u"case:创建新用户 密码错误" + "#"*10
        browser.find_element_by_name("username").clear()
        browser.find_element_by_name("username").send_keys(NEW_USER)
        browser.find_element_by_name("newpwd").clear()
        browser.find_element_by_name("newpwd").send_keys(W_NEWPWD)
        menu = browser.find_elements_by_name("newpwd")[1]
        webdriver.ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
        data = browser.find_elements_by_class_name("form-group")[1].find_element_by_tag_name("span").text
        print u"提示语："+data
        buttondatas = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")
        confirmbutton = buttondatas[1].get_attribute("disabled")
        print u"保存按钮是否置灰："+confirmbutton
        self.assertEqual(data,u"密码格式错误")
        self.assertEqual(confirmbutton,"true")

    def test08_newpwd_confirmpwd_not_match(self):
        print "#"*10 + u"case:创建新用户 确认密码与密码不一致" + "#"*10
        browser.find_element_by_name("username").clear()
        browser.find_element_by_name("username").send_keys(NEW_USER)
        browser.find_element_by_name("newpwd").clear()
        browser.find_element_by_name("newpwd").send_keys(NEW_PWD)
        browser.find_elements_by_name("newpwd")[1].clear()
        browser.find_elements_by_name("newpwd")[1].send_keys(CONFIRMPWD_NOT_MATCH)
        menu = browser.find_element_by_name("newpwd")
        webdriver.ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
        data = browser.find_elements_by_class_name("form-group")[2].find_element_by_tag_name("span").text
        print u"提示语："+data
        buttondatas = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")
        confirmbutton = buttondatas[1].get_attribute("disabled")
        print u"保存按钮是否置灰："+confirmbutton
        self.assertEqual(data,u"密码输入不一致")
        self.assertEqual(confirmbutton,"true")

    def test09_username_exist(self):
        print "#"*10 + u"case:创建新用户 用户名已存在" + "#"*10
        browser.find_element_by_name("username").clear()
        browser.find_element_by_name("username").send_keys("admin")
        browser.find_element_by_name("newpwd").clear()
        browser.find_element_by_name("newpwd").send_keys(NEW_PWD)
        browser.find_elements_by_name("newpwd")[1].clear()
        browser.find_elements_by_name("newpwd")[1].send_keys(NEW_PWD)
        buttondata = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")[1]
        confirmbutton = buttondata.get_attribute("disabled")
        if confirmbutton == None:
            buttondata.click()
            time.sleep(2)
            data = browser.find_element_by_class_name("text-danger").text
            print u"提示语："+data
        self.assertEqual(data,u"用户已存在")

    def test10_save_button(self):
        print "#"*10 + u"case:创建新用户 保存按钮" + "#"*10
        browser.find_element_by_name("username").clear()
        browser.find_element_by_name("username").send_keys(NEW_USER)
        browser.find_element_by_name("newpwd").clear()
        browser.find_element_by_name("newpwd").send_keys(NEW_PWD)
        browser.find_elements_by_name("newpwd")[1].clear()
        browser.find_elements_by_name("newpwd")[1].send_keys(NEW_PWD)
        buttondata = browser.find_element_by_class_name("modal-footer").find_elements_by_tag_name("button")[1]
        confirmbutton = buttondata.get_attribute("disabled")
        if confirmbutton == None:
            buttondata.click()
            time.sleep(2)
            status = browser.find_element_by_id("createUser").get_attribute("style").split(":")[1][1:-1]
            print u"创建用户弹窗是否存在："+status
            print u"新用户为："+NEW_USER
            menu = browser.find_element_by_tag_name("tbody")
            users = menu.find_elements_by_xpath("//tr")[2:]
            lst = []
            for user in users:
                username = user.find_elements_by_tag_name("td")[0].text
                lst.append(username)
            print u"用户列表："+str(lst)
        self.assertEqual(status,"none")
        self.assertTrue(NEW_USER in lst)

    def test11_delete_admin(self):
        print "#"*10 + u"case:删除admin" + "#"*10
        menu = browser.find_element_by_tag_name("tbody")
        user = menu.find_elements_by_xpath("//tr")[2]
        delete = user.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("class")
        print u"删除是否可用："+delete
        self.assertEqual(delete,"disabled")

    def test12_delete_user(self):
        print "#"*10 + u"case:删除用户" + "#"*10
        users = browser.find_element_by_tag_name("tbody").find_elements_by_xpath("//tr")[2:]
        for user in users:
            data = user.find_elements_by_tag_name("td")
            username = data[0].text
            if username == NEW_USER:
                delete = data[2].find_element_by_tag_name("a").get_attribute("class")
                print u"删除是否可用："+delete
                menu = data[2].find_element_by_link_text(u"删除")
                webdriver.ActionChains(browser).move_to_element(menu).click().perform()
                time.sleep(2)
                data = browser.find_element_by_class_name("bootbox-body").text
                print u"删除提示："+data
                browser.find_element_by_xpath("//button[@data-bb-handler='Cancel']").click()
                time.sleep(2)
                value = browser.find_element_by_tag_name("body").get_attribute("class")
                webdriver.ActionChains(browser).move_to_element(menu).click().perform()
                time.sleep(2)
                browser.find_element_by_xpath("//button[@data-bb-handler='OK']").click()
                time.sleep(2)
                hmenu = browser.find_element_by_tag_name("tbody")
                husers = hmenu.find_elements_by_xpath("//tr")[2:]
                lst = []
                for user in husers:
                    username = user.find_elements_by_tag_name("td")[0].text
                    lst.append(username)
                print u"用户列表："+str(lst)
        self.assertEqual(delete,"enabled")
        self.assertEqual(data,u"确认删除该用户？")
        self.assertEqual(value,"")
        self.assertFalse(NEW_USER in lst)

class TestPreview(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass
        #browser.get(URL+"login")
        #browser.find_element_by_id("username").send_keys("admin")
        #browser.find_element_by_id("password").send_keys("admin123")
        #browser.find_element_by_class_name("login_btn").submit()
        #time.sleep(2)
        
    @classmethod
    def tearDonwClass(self):
        pass
        
    def test01_switch_preview(self):
        menus = browser.find_elements_by_class_name("menu-name")
        for menu in menus:
            if menu.text == u"预览":
                webdriver.ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
        if browser.find_element_by_class_name("bkb-container").find_element_by_id("preview-settings"):
            print u"成功切换到预览页面"

class TestSystemSettings(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass
        #browser.get(URL+"login")
        #browser.find_element_by_id("username").send_keys("admin")
        #browser.find_element_by_id("password").send_keys("admin123")
        #browser.find_element_by_class_name("login_btn").submit()
        #time.sleep(2)
        
    @classmethod
    def tearDonwClass(self):
        browser.quit()

    def test01_switch_system_settings(self):
        menus = browser.find_elements_by_class_name("menu-name")
        for menu in menus:
            if menu.text == u"系统设置":
                webdriver.ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
        if browser.find_element_by_class_name("bkb-container").find_element_by_class_name("bkb-config"):
            print u"成功切换到系统设置页面"

    def test02_system_info(self):
        menus = browser.find_element_by_class_name("bkb-config").find_elements_by_tag_name("li")
        for menu in menus:
            if menu.text == u"系统信息":
                value = menu.get_attribute("class")
                print value
        datas = browser.find_elements_by_xpath("//tbody/tr")
        for data in datas:
            menu = data.find_elements_by_tag_name("td")[0].text
            #content = data.find_elements_by_tag_name("td")[1].text
            if menu == u"设备名称：":
                devicename = data.find_elements_by_tag_name("td")[1].text
                print u"设备名称："+devicename
            if menu == u"设备型号：":
                equipment_model = data.find_elements_by_tag_name("td")[1].text
                print u"设备型号："+equipment_model
            if menu == u"设备序列号：":
                serial_number = data.find_elements_by_tag_name("td")[1].text
                print u"设备序列号："+serial_number
            if menu == u"设备MAC地址：":
                mac = data.find_elements_by_tag_name("td")[1].text
                print u"设备MAC地址："+mac
            if menu == u"系统版本：":
                system_version = data.find_elements_by_tag_name("td")[1].text
                print u"系统版本："+system_version
            if menu == u"Web版本：":
                web_version = data.find_elements_by_tag_name("td")[1].text
                print u"Web版本："+web_version
            if menu == u"系统时间：":
                system_time = data.find_elements_by_tag_name("td")[1].text
                print u"系统时间："+system_time
        self.assertEqual(value,"active")
        self.assertEqual(devicename,u"深瞳人眼相机")
        self.assertEqual(equipment_model,u"RY10")
        self.assertEqual(serial_number,u"UN1607150036")
        self.assertEqual(mac,u"00:04:4b:07:78:24")
        self.assertEqual(system_version,u"")
        self.assertEqual(web_version,u"backbone_f-v1.6.3")
        #self.assertEqual(system_time,u"")

    def test03_switch_system_maintenance(self):
        browser.find_element_by_link_text(u"系统维护").click()
        time.sleep(2)
        menus = browser.find_element_by_class_name("bkb-config").find_elements_by_tag_name("li")
        for menu in menus:
            if menu.text == u"系统维护":
                value = menu.get_attribute("class")
                print value
        self.assertEqual(value,"active")

    def test04_system_recovery(self):
        menu = browser.find_elements_by_class_name("simple-module")[1]
        content = menu.find_element_by_class_name("text-important").text
        print content
        #menu.find_element_by_tag_name("button").click()
        self.assertEqual(content,u"提示：整个软件系统将完全恢复为出厂状态")
        
                                                            

if __name__ == "__main__":
    suite = unittest.TestSuite()
    '''suite.addTest(TestLoginAndLogout("test01_username_password_null"))
    suite.addTest(TestLoginAndLogout("test02_username_null"))
    suite.addTest(TestLoginAndLogout("test03_password_null"))
    suite.addTest(TestLoginAndLogout("test04_username_password_wrong"))
    suite.addTest(TestLoginAndLogout("test05_username_wrong"))
    suite.addTest(TestLoginAndLogout("test06_password_wrong"))
    suite.addTest(TestLoginAndLogout("test07_username_password_right"))
    suite.addTest(TestLoginAndLogout("test08_logout"))'''

    suite.addTest(TestChangeAdminPassword("test01_change_password_admin"))
    
    '''suite.addTest(TestChangeUserPassword("test01_default_display"))
    suite.addTest(TestChangeUserPassword("test02_oldpwd_null"))
    suite.addTest(TestChangeUserPassword("test03_newpwd_null"))
    suite.addTest(TestChangeUserPassword("test04_confirmpwd_null"))
    suite.addTest(TestChangeUserPassword("test05_oldpwd_wrong"))
    suite.addTest(TestChangeUserPassword("test06_newpwd_wrong"))
    suite.addTest(TestChangeUserPassword("test07_newpwd_confirmpwd_not_match"))
    suite.addTest(TestChangeUserPassword("test08_change_password_success"))
    
    suite.addTest(TestUserManagement("test01_create_new_user"))
    suite.addTest(TestUserManagement("test02_delete_user"))

    suite.addTest(TestUserManagementAdmin("test01_create_new_user_button"))
    suite.addTest(TestUserManagementAdmin("test02_close_button"))
    suite.addTest(TestUserManagementAdmin("test03_cancel_button"))
    suite.addTest(TestUserManagementAdmin("test04_username_null"))
    suite.addTest(TestUserManagementAdmin("test05_password_null"))
    suite.addTest(TestUserManagementAdmin("test06_confirmpwd_null"))
    suite.addTest(TestUserManagementAdmin("test07_password_wrong"))
    suite.addTest(TestUserManagementAdmin("test08_newpwd_confirmpwd_not_match"))
    suite.addTest(TestUserManagementAdmin("test09_username_exist"))
    suite.addTest(TestUserManagementAdmin("test10_save_button"))
    suite.addTest(TestUserManagementAdmin("test11_delete_admin"))
    suite.addTest(TestUserManagementAdmin("test12_delete_user"))
    
    suite.addTest(TestPreview("test01_switch_preview"))

    suite.addTest(TestSystemSettings("test01_switch_system_settings"))
    suite.addTest(TestSystemSettings("test02_system_info"))
    suite.addTest(TestSystemSettings("test03_switch_system_maintenance"))
    suite.addTest(TestSystemSettings("test04_system_recovery"))'''
    
    runner = unittest.TextTestRunner()
    runner.run(suite)




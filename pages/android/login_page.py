from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.logger import logger

class LoginPage(BasePage):
    # --- 元素定位 (Locators) ---

    # 登录方式选择
    LOGIN_VIA_PHONE_BTN = (AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="使用手机号码继续"]')
    LOGIN_VIA_WX_BTN = (AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="使用微信继续"]')
    LOGIN_VIA_GOOGLE_BTN = (AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="使用 Google 继续"]')
    LOGIN_VIA_APPLE_BTN = (AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="使用 Apple 继续"]')

    # 手机号登录流程
    GET_CODE_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="获取验证码"]')
    PRIVACY_AGREE_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="同意"]')
    AGREEMENT_CHECKBOX = (AppiumBy.XPATH, '//android.widget.CheckBox')
    CLOSE_BTN = (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView')
    PHONE_INPUT = (AppiumBy.XPATH, '//android.widget.EditText')
    VERIFY_CODE_INPUT = (AppiumBy.XPATH, '//android.widget.EditText')
    LOGIN_SUBMIT_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="登录"]')

    # 密码登录流程
    SWITCH_PASSWORD_LOGIN_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="密码登录"]')
    PS_PHONE_INPUT = (AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')
    PS_PASSWORD_INPUT = (AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[2]')

    # 个人信息填写
    GENDER_SELECT_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="选择您的性别"]')
    GENDER_MALE_OPT = (AppiumBy.XPATH, '//android.view.View[@content-desc="男"]')
    GENDER_FEMALE_OPT = (AppiumBy.XPATH, '//android.view.View[@content-desc="女"]')
    NAME_INPUT = (AppiumBy.XPATH, '//android.widget.EditText')
    BIRTHDAY_SELECT_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="生日"]')
    SETUP_COMPLETE_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="完成"]')

    # --- 业务动作 (Actions) ---

    def click_login_via_phone(self):
        """
        动作：点击手机号登录
        """
        logger.info("点击手机号登录")
        self.click_element(self.LOGIN_VIA_PHONE_BTN)

    def click_login_via_wx(self):
        """
        动作：点击微信登录
        """
        logger.info("点击微信登录")
        self.click_element(self.LOGIN_VIA_WX_BTN)

    def click_login_via_google(self):
        """
        动作：点击Google登录
        """
        logger.info("点击Google登录")
        self.click_element(self.LOGIN_VIA_GOOGLE_BTN)

    def click_login_via_apple(self):
        """
        动作：点击Apple登录
        """
        logger.info("点击Apple登录")
        self.click_element(self.LOGIN_VIA_APPLE_BTN)

    def click_get_code_btn(self):
        """
        动作：点击获取验证码
        """
        logger.info("点击获取验证码")
        self.click_element(self.GET_CODE_BTN)

    def click_privacy_agree(self):
        """
        动作：点击同意隐私协议
        """
        logger.info("点击同意隐私协议")
        self.click_element(self.PRIVACY_AGREE_BTN)

    def click_agreement_checkbox(self):
        """
        动作：点击用户协议勾选框
        """
        logger.info("点击用户协议勾选框")
        self.click_element(self.AGREEMENT_CHECKBOX)

    def click_close_btn(self):
        """
        动作：点击关闭按钮
        """
        logger.info("点击关闭按钮")
        self.click_element(self.CLOSE_BTN)

    def input_phone(self, phone: str):
        """
        动作：输入手机号
        """
        logger.info(f"输入手机号: {phone}")
        self.input_text(self.PHONE_INPUT, phone)

    def input_verify_code(self, code: str):
        """
        动作：输入验证码
        """
        logger.info(f"输入验证码: {code}")
        self.input_text(self.VERIFY_CODE_INPUT, code)

    def click_login_submit(self):
        """
        动作：点击登录按钮
        """
        logger.info("点击登录按钮")
        self.click_element(self.LOGIN_SUBMIT_BTN)

    def click_switch_password_login(self):
        """
        动作：点击切换到密码登录
        """
        logger.info("点击切换到密码登录")
        self.click_element(self.SWITCH_PASSWORD_LOGIN_BTN)

    def input_ps_phone(self, phone: str):
        """
        动作：输入密码登录的手机号
        """
        logger.info(f"输入密码登录的手机号: {phone}")
        self.input_text(self.PS_PHONE_INPUT, phone)

    def input_ps_password(self, password: str):
        """
        动作：输入密码登录的密码
        """
        logger.info("输入密码登录的密码")
        self.input_text(self.PS_PASSWORD_INPUT, password)

    def click_gender_select(self):
        """
        动作：点击选择性别
        """
        logger.info("点击选择性别")
        self.click_element(self.GENDER_SELECT_BTN)

    def click_gender_male(self):
        """
        动作：点击男性
        """
        logger.info("点击男性")
        self.click_element(self.GENDER_MALE_OPT)

    def click_gender_female(self):
        """
        动作：点击女性
        """
        logger.info("点击女性")
        self.click_element(self.GENDER_FEMALE_OPT)

    def input_name(self, name: str):
        """
        动作：输入名字
        """
        logger.info(f"输入名字: {name}")
        self.input_text(self.NAME_INPUT, name)

    def click_birthday_select(self):
        """
        动作：点击选择生日
        """
        logger.info("点击选择生日")
        self.click_element(self.BIRTHDAY_SELECT_BTN)

    def click_setup_complete(self):
        """
        动作：点击初始设定完成
        """
        logger.info("点击初始设定完成")
        self.click_element(self.SETUP_COMPLETE_BTN)
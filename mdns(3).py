# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json


class Mdns(object):
    def __init__(self, username, password):
        self.login_url = "https://www.mdnsonline.com/customer/login"
        self.session = self.login(username, password)
        self.add_url = "https://www.mdnsonline.com/shopping-cart/add"
        self.shopping_cart_url = "https://www.mdnsonline.com/shopping-cart"
        self.check_out_url = "https://www.mdnsonline.com/shopping-cart/checkout"
        self.checkout_address_url = "https://www.mdnsonline.com/shopping-cart/checkout-address"
        self.checkout_final_url = "https://www.mdnsonline.com/shopping-cart/checkout-final"
        self.payForm_url = "https://www.paydollar.com/b2c2/eng/payment/payForm.jsp"
        self.payALIPAY2_url = "https://www.paydollar.com/b2c2/eng/payment/payALIPAY2.jsp"
        self.headers = {
            'Host': 'www.mdnsonline.com',
            'Referer': 'https://www.mdnsonline.com/category/newarrival/madness',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }

    def login(self, username, password):
        session = requests.session()
        headers = {
            'Host': 'www.mdnsonline.com',
            'Origin': 'https://www.mdnsonline.com',
            'Referer': 'https://www.mdnsonline.com/customer/login',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        web_data = session.get(self.login_url, headers=headers).text
        soup = BeautifulSoup(web_data, 'lxml')
        csrf_content = soup.find_all('meta')[3]['content']
        print(csrf_content)  # 提取登录csrf

        form_data = {
            '_csrf-frontend': csrf_content,
            'CustomerLoginForm[email]': username,
            'CustomerLoginForm[password]': password,
        }
        # 发起登录请求
        session.post(self.login_url, data=form_data, headers=headers)
        web_data = session.get("https://www.mdnsonline.com/customer/edit-profile").text
        # print(web_data)  # 账户页面
        print("========== 登录成功 ==========")
        return session

    def add(self, id, size, quantity):
        product_url = "https://www.mdnsonline.com/product/1598"
        web_data = self.session.get(product_url, headers=self.headers).text
        soup = BeautifulSoup(web_data, 'lxml')
        csrf_content = soup.find_all('meta')[4]['content']
        print(csrf_content)  # 提取登录csrf

        headers = {
            'Host': 'www.mdnsonline.com',
            'Origin': 'https://www.mdnsonline.com',
            'Referer': product_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'X-CSRF-Token': csrf_content,
            'X-Requested-With': 'XMLHttpRequest',
        }
        form_data = {
            'product_id': id,
            'product_size_id': size,
            'quantity': quantity
        }
        web_data = self.session.post(self.add_url, data=form_data, headers=headers).text
        add_ret = json.loads(web_data)
        print("========== 加购物车 ==========")
        print(add_ret)

    def shopping_cart(self):
        web_data = self.session.get(self.shopping_cart_url, headers=self.headers).text
        # print(web_data)
        soup = BeautifulSoup(web_data, 'lxml')
        csrf_content = soup.find_all('meta')[3]['content']
        # print(csrf_content)
        return csrf_content

    def check_out(self):
        self.headers['Referer'] = 'https://www.mdnsonline.com/category/shopping-cart'
        web_data = self.session.get(self.check_out_url, headers=self.headers).text
        # print(web_data)
        soup = BeautifulSoup(web_data, 'lxml')
        csrf_content = soup.find_all('meta')[3]['content']
        print(csrf_content)
        print("========== 立即付款 ==========")
        return csrf_content

    def checkout_address(self, _csrf_frontend):
        self.headers['Referer'] = 'https://www.mdnsonline.com/shopping-cart/checkout'
        self.headers['Origin'] = 'https://www.mdnsonline.com'
        form_data = {
            '_csrf-frontend': _csrf_frontend,
            'OrderForm[customerid]': '*',
            'OrderForm[firstname]': '*',
            'OrderForm[lastname]': '**',
            'OrderForm[email]': '***',
            'OrderForm[telephone]': '*',
            'OrderForm[company]': '',
            'OrderForm[ship_address1]': '*',
            'OrderForm[ship_address2]': '*',
            'OrderForm[ship_city]': '*',
            'OrderForm[ship_postcode]': '*',
            'OrderForm[ship_country]': '*',
            'OrderForm[ship_zone]': '*',
            'OrderForm[ship_countryid]': '*',
            'OrderForm[ship_zoneid]': '*',
            'issameadd': '1',
            'OrderForm[payment_address1]': '*',
            'OrderForm[payment_address2]': '*',
            'OrderForm[payment_city]': '*',
            'OrderForm[payment_postcode]': '*',
            'OrderForm[payment_country]': '*',
            'OrderForm[payment_zone]': '*',
            'OrderForm[payment_countryid]': '96',
            'OrderForm[payment_zoneid]': '4132',
            'OrderForm[shippingmethod]': 'sfexpress',
        }
        web_data = self.session.post(self.checkout_address_url, data=form_data, headers=self.headers).text
        # print(web_data)
        soup = BeautifulSoup(web_data, 'lxml')
        csrf_content = soup.find_all('meta')[3]['content']
        print(csrf_content)
        print("========== 确认地址 ==========")
        return csrf_content

    def checkout_final(self, _csrf_frontend):
        self.headers['Referer'] = 'https://www.mdnsonline.com/shopping-cart/checkout-address'
        form_data = {
            '_csrf-frontend': _csrf_frontend,
            'OrderForm[customerid]': '**',
            'OrderForm[firstname]': '**',
            'OrderForm[lastname]': '**',
            'OrderForm[email]': '***',
            'OrderForm[telephone]': '***',
            'OrderForm[company]': '',
            'OrderForm[shippingmethod]': '*',
            'OrderForm[payment_address1]': '**',
            'OrderForm[payment_address2]': '**',
            'OrderForm[payment_city]': '*',
            'OrderForm[payment_postcode]': '*',
            'OrderForm[payment_country]': '*',
            'OrderForm[payment_zone]': '*',
            'OrderForm[payment_countryid]': '*',
            'OrderForm[payment_zoneid]': '4132',
            'OrderForm[confirmaddress]': '0',
            'OrderForm[confirmaddress]': '1',
            'OrderForm[confirmorder]': '0',
            'OrderForm[confirmorder]': '1',
            'OrderForm[paymentmethod]': 'alipay',
            'OrderForm[agreeterm]': '0',
            'OrderForm[agreeterm]': '1',
        }
        web_data = self.session.post(self.checkout_final_url, data=form_data, headers=self.headers).text
        # print(web_data)
        soup = BeautifulSoup(web_data, 'lxml')
        pay_form = {
            'merchantId': soup.select('input')[0]['value'],
            'amount': soup.select('input')[1]['value'],
            'orderRef': soup.select('input')[2]['value'],
            'currCode': soup.select('input')[3]['value'],
            'mpsMode': soup.select('input')[4]['value'],
            'successUrl': soup.select('input')[5]['value'],
            'failUrl': soup.select('input')[6]['value'],
            'cancelUrl': soup.select('input')[7]['value'],
            'payType': soup.select('input')[8]['value'],
            'lang': soup.select('input')[9]['value'],
            'payMethod': 'ALIPAY',
            'secureHash': soup.select('input')[11]['value']
        }
        print(pay_form)
        print("========== 提交订单 ==========")
        return pay_form

    def pay_Form(self, pay_form):
        headers = {
            # 'Cookie':'JSESSIONID=675188032EF3E4AE9E38FBE286E3CC6A',
            'Host': 'www.paydollar.com',
            'Origin': 'https://www.mdnsonline.com',
            'Referer': 'https://www.mdnsonline.com/shopping-cart/checkout-final',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        web_data = self.session.post(self.payForm_url, data=pay_form, headers=headers).text
        # print(web_data)
        print("========== 第一次提交支付 ==========")
        soup = BeautifulSoup(web_data, 'lxml')
        sessionId = soup.select('input')[31]['value']
        print(sessionId)
        return sessionId

    def pay_ALIPAY(self, pay_form, sessionId):
        headers = {
            # 'Cookie': 'JSESSIONID=675188032EF3E4AE9E38FBE286E3CC6A',
            'Host': 'www.paydollar.com',
            'Origin': 'https://www.paydollar.com',
            'Referer': 'https://www.paydollar.com/b2c2/eng/payment/payForm.jsp',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        pay_form2 = {
            'masterMerId': '1',
            'merchantId': '88589837',
            'successUrl': 'https://www.mdnsonline.com/shopping-cart/paydollar-callback?key=4e88b14e99aeb388e258fb8f598e36ea&result=success',
            'failUrl': 'https://www.mdnsonline.com/shopping-cart/paydollar-callback?key=4e88b14e99aeb388e258fb8f598e36ea&result=fail',
            'cancelUrl': 'https://www.mdnsonline.com/shopping-cart/paydollar-callback?key=4e88b14e99aeb388e258fb8f598e36ea&result=cancel',
            'amount': '513',
            'currCode': '344',
            'orderRef': pay_form['orderRef'],
            'print': 'null',
            'failRetry': 'null',
            'sessionId': '120650235',
            'payMethod': 'ALIPAY',
            'lang':'X',
            'redirect': '-1',
            'payType': 'N',
            'secureHash': pay_form['secureHash'],
            'oriCountry': 'null',
            'destCountry': 'null',
            'referer': 'www.mdnsonline.com',
            'paymentPageSkip': 'T',
            'merpMethod': 'ALIPAY',
            'templateId': '0',
            'mpsMode': 'NIL',
            'deviceMode': 'auto',
            'hiddenAmount': 'F',
            'expDateCheck': '0',
            'expDateUpdate':'F',
            'saveCardControl': '0',
            'selectedPayMethod': 'ALIPAY',
            'pcTimeZone': '8',
        }
        ALIPAY_form = {
            'refix': '',
            'Time':'',
            'calmode': '',
            'payTerm':'',
            'computeMethod':'',
            'SupplierNumber':'',
            'ProductType':'',
            'ProductCode':'',
            'SerialNumber':'',
            'PreInterestRate':'',
            'PreMonthlyAmount':'',
            'PreTotalAmount':'',
            'Productname':'',
            'Modelname':'',
            'Suppliername':'',
            'InterestFreeMonth':'',
            'WaiveMonthlyInstallmentFrom':'',
            'WaiveMonthlyInstallmentTo':'',
            'masterMerId': '1',
            'merchantId': pay_form['merchantId'],
            'successUrl': pay_form['successUrl'],
            'failUrl': pay_form['failUrl'],
            'cancelUrl': pay_form['cancelUrl'],
            'remark':'',
            'appId':'',
            'appRef':'',
            'amount': pay_form['amount'],
            'currCode': pay_form['currCode'],
            'orderRef': pay_form['orderRef'],
            'print': 'null',
            'failRetry': 'null',
            'sessionId': sessionId,
            'payMethod': 'ALIPAY',
            'lang': pay_form['lang'],
            'redirect': '-1',
            'payType': pay_form['payType'],
            'secureHash': pay_form['secureHash'],
            'oriCountry': 'null',
            'destCountry': 'null',
            'referer': 'www.mdnsonline.com',
            'paymentPageSkip': 'T',
            'channelType':'',
            'merpMethod': 'ALIPAY',
            'templateId': '0',
            'foreignCode':'',
            'mpsMode': 'NIL',
            'deviceMode': 'auto',
            'csothName':'',
            'csothEmail':'',
            'csothPhone':'',
            'hiddenAmount': 'F',
            'expDateCheck': '0',
            'expDateUpdate': 'F',
            'saveCardControl': '0',
            'dplId':'',
            'selectedPayMethod': 'ALIPAY',
            'pcTimeZone': '8',
        }
        web_data = self.session.post(self.payALIPAY2_url, data=ALIPAY_form, headers=headers).text
        # print(web_data)
        print("========== 第二次提交支付 ==========")
        soup = BeautifulSoup(web_data, 'lxml')
        alipay_url = soup.meta['content'].lstrip('0; url=')
        print("========== 支付宝付款链接 ==========")
        print(alipay_url)
        return alipay_url

    def run(self):
        try:
            a, b,c = raw_input("please int satrt num and end num ; 11 15 66 \n").split()
            self.add(1585,9381,1)
            self.add(1584, 9377, 1)
            _csrf_frontend = self.shopping_cart()
            _csrf_frontend_1 = self.check_out()  # 确认信息
            _csrf_frontend_2 = self.checkout_address(_csrf_frontend_1)  # 确认地址
            pay_form = self.checkout_final(_csrf_frontend_2)  #
            sessionId = self.pay_Form(pay_form)
            alipay_url = self.pay_ALIPAY(pay_form, sessionId)
            with open('alipay_url.txt', 'a+') as file:
                file.write(alipay_url+'\n')
        except Exception as e:
            print("========== 错误信息:  ==========", e)


if __name__ == '__main__':
    mdns = Mdns('***', '***')
    while 1:
        mdns.run()
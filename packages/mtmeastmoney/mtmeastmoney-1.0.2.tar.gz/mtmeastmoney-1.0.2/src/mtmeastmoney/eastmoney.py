import random
import requests
from datetime import datetime, date
from .ocr import ocr_code
import time
import re
import json


def post_order(session, url, data: dict):
    payloadHeader = {'Content-Type': 'application/json'}
    rsp = session.post(url, data=json.dumps(data), headers=payloadHeader)
    return rsp.json().get("Message", rsp.json())


class EastMoney:
    def __init__(self, userId=None, password=None, randomNumber=None, duration=15) -> None:
        self.host = "https://jywg.18.cn"
        self.session = requests.Session()
        self.userId = userId
        self.password = password
        self.login_duration = duration
        self.random_number = random.random() if randomNumber is None else randomNumber
        self.vertify_code_url = self.host + f"/Login/YZM?randNum={self.random_number}"
        self.validate_key = ""
        pass

    def get_validate_key(self):
        url = self.url_add_host("/Trade/XzsgBatPurchase")
        rsp = self.session.get(url)
        validatekey_list = re.findall("<input id=\"em_validatekey\"[^>]*value=\"([^\"]*)\"", rsp.text)
        if not len(validatekey_list):
            raise Exception("获取验证秘钥：登录失败")
        return validatekey_list[0]

    def login_once(self):
        data = {
            "userId": str(self.userId),
            "password": str(self.password),
            "randNumber": str(self.random_number),
            "identifyCode": ocr_code(self.vertify_code_url),
            "duration": str(self.login_duration),
            "authCode": "",
            "type": "Z"
        }
        url = self.host + "/Login/Authentication?validatekey="
        rsp = self.session.post(url, data)
        return "Uuid" in str(self.session.cookies)

    def login_retry(self, max_times=3, wait_second=5):
        for _ in range(max_times):
            if self.login_once():
                break
            else:
                time.sleep(wait_second)
        else:
            raise Exception("登录失败")
        self.validate_key = self.get_validate_key()

    def url_add_host(self, url):
        return (self.host + url) if "https" not in url else url

    def url_add_validate_key(self, url):
        url = self.url_add_host(url)
        url = (url + "?") if "?" not in url else url
        return url + f"validatekey={self.validate_key}"

    def query(self, url, data=None):
        if data is None:
            rsp = self.session.post(url)
        else:
            rsp = self.session.post(url, data=data)
        try:
            bonds_data = rsp.json()["Data"]
        except:
            raise Exception("获取信息：登录失败")
        return bonds_data

    def query_stock_trade_info(self, stock_code):
        url = self.url_add_validate_key("/Trade/GetAllNeedTradeInfo")
        return self.query(url, data={"stockCode": stock_code})["ZqInfo"]

    def query_trade_history(self, start_date, end_date, count=10000):
        url = self.url_add_validate_key("/Search/GetHisDealData")
        return self.query(url, data={"st": start_date, "et": end_date, "qqhs": count, "dws": ""})

    def query_market_convertible_bonds_list(self):
        url = self.url_add_validate_key("/Trade/GetConvertibleBondListV2")
        return self.query(url)

    def query_asset_stocks_list(self):
        url = self.url_add_validate_key("/Search/GetStockList")
        return self.query(url)

    def query_is_new_convertible_bond_available_today(self):
        today_str = date.today().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=10&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=PUBLIC_START_DATE"

        resp = self.session.get(url)
        result = re.search(today_str, resp.text)
        if result is not None:
            return True
        else:
            return False

    def scripts_buy_today_convertible_bonds(self):
        json_data = self.query_market_convertible_bonds_list()
        json_data = [bond for bond in json_data if bond["PURCHASEDATE"] == datetime.now().strftime("%Y%m%d")]
        if not len(json_data):
            return "今日无可买可转债"
        data = [{
            "StockCode": bond["SUBCODE"],
            "StockName": bond["SUBNAME"],
            "Price": bond['PARVALUE'],
            "Amount": int(bond['LIMITBUYVOL']),
            "TradeType": "B",
            "Market": bond['Market']
        } for bond in json_data]
        url = self.url_add_validate_key("/Trade/SubmitBatTradeV2")
        message = post_order(self.session, url, data)
        return message

    def scripts_sell_old_convertible_bonds(self):
        json_data = self.query_asset_stocks_list()
        json_data = [i for i in json_data if int(i["Kysl"]) > 0]
        if not len(json_data):
            return ""
        data = [{
            "stockCode": i["Zqdm"],
            "price": 80,
            "amount": int(i['Kysl']),
            "tradeType": "S",
            "zqmc": i["Zqmc"],
            "gddm": i["Gddm"],
            "market": i["Market"]
        } for i in json_data if "债" in i["Zqmc"] or "转2" in i["Zqmc"]]
        url = self.url_add_validate_key("/Trade/SubmitTradeV2")
        message_list = [
            f"卖单提交:" + str(i["zqmc"]) + str(i["amount"]) + str(post_order(self.session, url, i)) for i in data
            if i["amount"] > 0
        ]
        return "\n".join(message_list)

    def scripts_auto_trade_bonds(self, isSell=False):
        try:
            message = self.scripts_buy_today_convertible_bonds()
        except Exception as e:
            message = str(e)
        if isSell:
            message += "\n"
            try:
                message += self.scripts_sell_old_convertible_bonds()
            except Exception as e:
                message += str(e)
        if message.endswith("\n"):
            message = message[:-1]
        return message
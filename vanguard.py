import requests
import re
import json


class Vanguard():
    LOGIN_URL = "https://secure.vanguardinvestor.co.uk/Login"
    LOGIN_ENDPOINT = "https://secure.vanguardinvestor.co.uk/en-GB/Api/Session/Login/Post"
    HOLDINGS_URL = "https://secure.vanguardinvestor.co.uk/en-GB/Api/Holdings/SubAccountHoldings/Get?accountHierarchyId=%s"
    HIERARCHY_ID_URL = "https://secure.vanguardinvestor.co.uk/en-GB/Customer/Home/SelectRootForLogin"
    LOGGED_IN = False

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def get_antiforgery_token(self):
        return re.findall('data-javascript-antiforgery="(.*)?">', self.session.get(self.LOGIN_URL).text)[0]

    def login(self):
        self.LOGGED_IN = self.session.post(self.LOGIN_ENDPOINT, json={"request": {
            "Username": self.username, "Password": self.password}}, headers={"anti-forgery-token": self.get_antiforgery_token()}).status_code == 200
        self.get_heirarchy()

    def is_logged_in(self):
        return self.LOGGED_IN

    def get_heirarchy(self):
        self.hierarchy_id = re.findall(
            '&quot;HierarchyId&quot;:&quot;(.*?)&quot;', self.session.get(self.HIERARCHY_ID_URL).text)[0]

    def get_data(self):
        dataset = self.session.get(self.HOLDINGS_URL % (self.hierarchy_id), headers={
            "anti-forgery-token": self.get_antiforgery_token()}).text
        resultant = []
        for holding in json.loads(dataset)['Result']['Holdings']:
            resultant.append({
                "value": holding['MarketValue']['Amount'],
                "name": holding["ProductCode"]
            })

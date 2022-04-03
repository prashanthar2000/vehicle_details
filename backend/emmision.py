import requests
import re
class emmision_test:
    def __init__(self, vehicle_number):
        self.__VIEWSTATE = r'id="__VIEWSTATE" value="(.*)" />'
        self.__EVENTVALIDATION = r'id="__EVENTVALIDATION" value="(.*)" />'
        self.__VIEWSTATEGENERATOR = r'id="__VIEWSTATEGENERATOR" value="(.*)" />'
        self.__EVENTTARGET = r'id="__EVENTTARGET" value="(.*)" />'
        self.__EVENTARGUMENT = r'id="__EVENTARGUMENT" value="(.*)" />'
        self.__LASTFOCUS = r'id="__LASTFOCUS" value="(.*)" />'
        self.__VIEWSTATEENCRYPTED = r'id="__VIEWSTATEENCRYPTED" value="(.*)" />'
        self.__LASTFOCUS = r'id="__LASTFOCUS" value="(.*)" />'
        self.__VIEWSTATEENCRYPTED = r'id="__VIEWSTATEENCRYPTED" value="(.*)" />'
        self.__LASTFOCUS = r'id="__LASTFOCUS" value="(.*)" />'
        self.regex = {"__VIEWSTATE": self.__VIEWSTATE,
                      "__EVENTVALIDATION": self.__EVENTVALIDATION,
                      "__VIEWSTATEGENERATOR": self.__VIEWSTATEGENERATOR,
                      "__EVENTARGUMENT": self.__EVENTARGUMENT,
                      "__LASTFOCUS": self.__LASTFOCUS,
                      "__EVENTTARGET": self.__EVENTTARGET,
                      "__VIEWSTATEENCRYPTED": self.__VIEWSTATEENCRYPTED,
                      "__LASTFOCUS": self.__LASTFOCUS,
                      "__VIEWSTATEENCRYPTED": self.__VIEWSTATEENCRYPTED,
                      "__LASTFOCUS": self.__LASTFOCUS,
                      }
        self.cookies = {}
        self.session = requests.session()
        # self.session.proxies.update({'http': 'http://localhost:8080'})
        self.vehicle_number = vehicle_number

    def getCSRFIDs(self):
        req = self.session.get("http://etc.karnataka.gov.in/ReportingUser/Scgr1.aspx")
        for i in self.regex:
            self.cookies[i] = re.findall(self.regex[i], req.text)
        return self.cookies
    
    def get_emmision_data(self):    
        self.cookies = self.getCSRFIDs()

        burp0_url = "http://etc.karnataka.gov.in:80/ReportingUser/Scgr1.aspx"
        burp0_cookies = {"ASP.NET_SessionId": "3uoqg0tfr5lpqyhcgfwo2wbf"}
        burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "http://etc.karnataka.gov.in", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer": "http://etc.karnataka.gov.in/ReportingUser/Scgr1.aspx", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", "Connection": "close"}
        burp0_data = {"__EVENTTARGET": '', "__EVENTARGUMENT": '', "__VIEWSTATE": self.cookies["__VIEWSTATE"] ,
         "__VIEWSTATEGENERATOR": self.cookies["__VIEWSTATEGENERATOR"], 
         "__EVENTVALIDATION": self.cookies["__EVENTVALIDATION"], "Sreg": self.vehicle_number, "Veh_Type": "P", "Button1": "Search"}
        res = self.session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        return res.text  

    def extract_emmision_data(self):
        regex = '<td><a href=".*" target="_blank">.*</a></td><td>.*</td><td>.*</td><td>.*</td><td>(.*)</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>(.*)</td><td>.*'
        data = self.get_emmision_data()
        emmision_data = re.findall(regex, data)
        return emmision_data   
if __name__ == '__main__':
    obj = emmision_test("KA02JN5485")
    data = obj.extract_emmision_data()
    for i in data:
        print(i)
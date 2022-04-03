
import requests

from PIL import Image
import io

import pytesseract

import time
import psutil

#res type 1 
# t1 = {'PoliceFineDetailsList': None, 'TotalFineAmount': None, 'Response': {'ResponseVal': False, 'Reason': 'No Fine Details Found For This Search'}, 'OffencesDtls': {'respCode': 0, 'respText': None, 'base_url': None, 'Data': None}, 'Result': None}

# res type 2 
# t2 = {'PoliceFineDetailsList': None, 'TotalFineAmount': None, 'Response': {'ResponseVal': False, 'Reason': 'captcha is not valid.'}, 'OffencesDtls': None, 'Result': None}
from emmision import emmision_test

class traffic_fine:
    
    def __init__(self , reg_num ,debug=False ):
        self.reg_num = reg_num
        self.retry_count = 0
        self.debug = debug
    
    def solve_capche(self,debug):
        burp0_url = "https://www.karnatakaone.gov.in:443/CaptchaeGernerate.aspx?New=1"
        burp0_headers = {"Connection": "close", "sec-ch-ua": "\"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"", "sec-ch-ua-mobile": "?0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://www.bangaloretrafficpolice.gov.in/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
        res = requests.get(burp0_url, headers=burp0_headers)
        cookie = res.cookies.get_dict()
        gif = res.content
        image = Image.open(io.BytesIO(gif))
        custom_config = r'-l eng '#--oem 3 --psm 6'
        capche = pytesseract.image_to_string(image, config=custom_config)
        capche = capche.strip()
        if debug:
            image.show()   
            print(capche)
            time.sleep(5)
            for proc in psutil.process_iter():
                if proc.name() == "display":
                    proc.kill()
 
        return cookie , capche
    
    def getFineDetails(self,cookie , capche):
        burp0_url = "https://www.karnatakaone.gov.in:443/PoliceCollectionOfFine/PoliceFine_Details?CaptchaCode="
        burp0_url += capche + "&SearchBy=REGNO&SearchValue="
        burp0_url += self.reg_num + "&ServiceCode=BPS"
        burp0_cookies = {"__RequestVerificationToken": "luqv2cZ8gnLMsCLum679VP6MUZOLgx5rp5_dHyVRUuftRz4szX6ntXxX6aSJmpH-KkKuUS_PpUwGBFV5tMwKYorrFA81", "KarnatakaOneSession": "da4k3ta0bxx13fsajwxhw30j"}
        burp0_cookies["KarnatakaOneSession"] = cookie["KarnatakaOneSession"]

        burp0_headers = {"Connection": "close", "sec-ch-ua": "\"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"", "Accept": "application/json, text/plain, */*", "X-XSRF-Token": "8h05C2J3r63jPAlWQe4JdjJu5nlAphjX4sks_gF6hM1uLuJW8ziQTxJyW4yyepxEPkaX2tnTtNzH6YqpmwEsulc5fl01", "X-Requested-With": "XMLHttpRequest", "sec-ch-ua-mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Origin": "https://www.karnatakaone.gov.in", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.karnatakaone.gov.in/PoliceCollectionOfFine/TrafficViolationFineCollection/dUZnOGxNQzFCbEdIckVoQlNaZVV2UT09", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
        res = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

        return res
    
    def check_res(self, res):
        res = res.json()
        if res["Response"] :
            if res["Response"]["ResponseVal"] == False  and "captcha is not valid." in res["Response"]["Reason"]:
                print("\t\t" ,res)
                return False 
            return True
        #if response doesn't exists 
        return False
    
    def return_function(self):
        while(self.retry_count < 5):
            cookie , capche = self.solve_capche(self.debug)
            res = self.getFineDetails(cookie, capche)
            if self.check_res( res):
                return res.json()
            self.retry_count += 1
        

if __name__ == '__main__':
    # print(emmision_test("KA02JN5485").extract_emmision_data())
    # fine = traffic_fine("KA02JN5485", True)
    # print(fine.return_function())
    print(emmision_test("KA02JY1047").extract_emmision_data())
    fine = traffic_fine("KA02JY1047", True)
    print(fine.return_function())
    
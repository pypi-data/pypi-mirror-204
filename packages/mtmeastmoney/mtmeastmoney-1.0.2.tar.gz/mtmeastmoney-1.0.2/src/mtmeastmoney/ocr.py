import ddddocr
import requests
import time

def ocr_code(vertify_code_url):
    for _ in range(5):
        ocr = ddddocr.DdddOcr(show_ad=False)
        rsp = requests.get(vertify_code_url)
        res = ocr.classification(rsp.content)
        verify_code = res.replace("z", "2").replace("o", "0")
        if len(verify_code) == 4:
            return verify_code
        else:
            time.sleep(1)
    raise Exception("无法识别出正确的验证码")
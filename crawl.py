from selenium import webdriver
import time
import re

def crawl_frame(frame_xpath):
    driver.switch_to.default_content()
    # 팝니다 iframe 가져오기
    frame = driver.find_element_by_xpath(frame_xpath)
    # 팝니다 iframe으로 스위치
    driver.switch_to.frame(frame)
    for pg in [1, 3, 4, 5, -1]:
        for i in range(20):
            # 첫 번째 매물 가져오기
            row = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[%d]/td[1]/a' % (3 * (i + 1)))
            # '/html/body/table[2]/tbody/tr[6]/td[1]/a'
            # 첫 번째 매물 시각 가져오기
            row_date = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[%d]/td[5]/font' % (3 * (i + 1)))
            # 첫 번째 매물 클릭하기
            row.click()
            # 첫 번째 매물 ID 가져오기
            row_id = row.get_attribute('onclick')  # menu('M12345678') 형태
            row_code = row_id[6:-2]  # M12345678 형태
            # 첫 번째 매물 상세 정보 가져오기
            try:
                e = driver.find_element_by_xpath('//*[@id="submenu_%s"]/td/table/tbody/tr/td[1]/font' % row_code)
                # print(row_code) # M12345678
                # print(row.text) # 블루홀 계좌있음/급매/삼성
                # print(e.text) # 연락처, 수량, 가격, IP
                # print(row_date.text) # 시각
                e_tokens = re.split('\n| , |:', e.text)

                memo = row.text.strip()
                phone_number = e_tokens[1].strip()
                amount = e_tokens[3].strip()
                unit_price = e_tokens[5].strip()
                ip_addr = e_tokens[7].strip()
                mod_date = row_date.text.strip()

                print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row_code, memo, phone_number, amount, unit_price, ip_addr, mod_date))
            except:
                pass

        if pg >= 0:
            next_page = driver.find_element_by_xpath('/html/body/table[4]/tbody/tr/td[1]/a[%d]' % pg)
            # print('Next page...')
            next_page.click()
            time.sleep(1.5)
            # driver.implicitly_wait(3)

if __name__ == '__main__':
    driver = webdriver.Chrome('C:\\Users\\gb\\PycharmProjects\\forty\\chromedriver.exe')
    driver.implicitly_wait(3)
    # 블루홀 매매 페이지 오픈
    driver.get('http://stock.38.co.kr/html/trade/trade_sellbuy/index_red.html?act=search&sc_column=item_code&sc_string=259960&sc_term=30&imsi=2&tmpstr=%BA%ED%B7%E7%C8%A6')

    sel_frame_xpath = '/html/body/table[3]/tbody/tr/td/table[3]/tbody/tr/td[1]/iframe'
    buy_frame_xpath = '/html/body/table[3]/tbody/tr/td/table[3]/tbody/tr/td[2]/iframe'

    print('--- sel ---')
    crawl_frame(sel_frame_xpath)
    print('--- buy ---')
    crawl_frame(buy_frame_xpath)

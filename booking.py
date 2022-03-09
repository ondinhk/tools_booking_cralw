import time
import requests as rq
import json
import re
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

HEADERS = {
    'user-agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
    , 'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5'
}
ARRAY = []
BASE_URL = 'https://www.booking.com/searchresults.vi.html?label=888&sid=048a9fe95aafeade797e607e6d5e4b2b&aid=1541467&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D1541467%3Blabel%3D888%3Bsid%3D048a9fe95aafeade797e607e6d5e4b2b%3Btmpl%3Dsearchresults%3Bcheckin_monthday%3D08%3Bcheckin_year_month%3D2022-03%3Bcheckout_monthday%3D09%3Bcheckout_year_month%3D2022-03%3Bclass_interval%3D1%3Bdest_id%3D-3712045%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_history%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsh_position%3D1%3Bshw_aparth%3D1%3Bsi%3Dai%3Bsi%3Dci%3Bsi%3Dco%3Bsi%3Ddi%3Bsi%3Dla%3Bsi%3Dre%3Bslp_r_match%3D0%3Bsrpvid%3D4b5775c46f0200d5%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ss=%C4%90%C3%A0+L%E1%BA%A1t&is_ski_area=0&ssne=%C4%90%C3%A0+L%E1%BA%A1t&ssne_untouched=%C4%90%C3%A0+L%E1%BA%A1t&city=-3712045&checkin_year=2022&checkin_month=3&checkin_monthday=15&checkout_year=2022&checkout_month=3&checkout_monthday=16&group_adults=2&group_children=0&no_rooms=1&from_sf=1&sr_change_search=2&offset='
COUNT = 0
HOUSE = 0

def exportFile():
    with open('data_dalat_old.json', 'w', encoding='utf8') as file:
        json.dump(ARRAY, file, ensure_ascii=False)
    print("Complete")


def crawler(page):
    global HOUSE
    url = BASE_URL + str(page)
    response = rq.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    # khung chứa các item h
    divItemHotel = soup.find_all('div', {'class': '_5d6c618c8'})
    # lặp qua từng khung để lấy info
    for idx, item in enumerate(divItemHotel):
        # (tag a: chứa tên và hình)
        tag_a_img = item.find('div', {'class': 'a5c3ef8268'})
        # lấy tag a
        tag_a = tag_a_img.find('a')
        url_booking = tag_a.attrs['href']
        # Cat url
        rs = url_booking.index('?');
        new_url_booking = url_booking[0:rs]
        # Url img
        tag_img = tag_a_img.find('img', {'class': 'e75f1d9859'})
        url_img = tag_img.attrs['src']
        # Tên trọ
        name = tag_img.attrs['alt']
        # lấy mô tả, do css mô tả chỉ có duy nhất 1 class
        # và có nhiều class giống nên phải lặp qua để lấy div có duy nhât 1 class
        des = item.find_all('div', class_='_4abc4c3d5')
        for i in des:
            if len(i["class"]) != 1:
                continue
            des = i.get_text()
        # Lay khoang cach
        distance = item.find('span', {'data-testid': 'distance'}).get_text()
        # Lay gia
        cost = item.find('span', {'class': 'fde444d7ef _e885fdc12'}).get_text()
        # Rating
        rate = item.find('div', {'class': '_9c5f726ff bd528f9ea6'})
        if rate is not None:
            rate = rate.get_text()
        else:
            rate = 'Chưa có đánh giá'
        # Numer rating
        print(new_url_booking)
        reviews = item.find('div', {'class': '_4abc4c3d5 _1e6021d2f _6e869d6e0'})
        if reviews is not None:
            reviews = reviews.get_text()
        else:
            reviews = 'Chưa có đánh giá'
        # Create object
        array_comment = getReviews(new_url_booking)
        # array_comment = []
        temp = {'title': name, 'link_booking': new_url_booking,
                'image': url_img,
                'description': des,
                'distance': distance,
                'cost': cost,
                'quanlityComment': reviews,
                'rate': rate,
                'listComment': array_comment}
        HOUSE+=1
        ARRAY.append(temp)


def getMaximumPage():
    response = rq.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    tag_num = soup.find('div', {'class': '_111b4b398'})
    num_string = tag_num.getText()
    pattern = '\d+'
    str_list = re.findall(pattern, num_string)
    numPage = int(str_list[0])
    return numPage


def getReviews(url):
    global COUNT
    SLEEP_TIME = random.randint(2, 3)
    print("TimeSleep: " + str(SLEEP_TIME))
    driver.implicitly_wait(SLEEP_TIME)
    driver.get(url)

    # Click button show list reviews
    button = driver.find_element(by=By.XPATH, value="//span[contains(text(), 'Đọc tất cả đánh giá')]")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(SLEEP_TIME)

    # Parse HTML
    pageData = driver.page_source
    html_page = BeautifulSoup(pageData, 'html.parser')
    # Lấy số lượng comment
    number_html = html_page.find('span', {'class': 'review-score-widget__subtext'})
    number_text = number_html.get_text();
    space_idx = number_text.index(" ");
    # Số lượng comment
    number_int = int(number_text[0:space_idx])
    loop = round(number_int / 10)
    loop = round(loop / 3)
    print("Number comment " + str(round(number_int / 3)) + " Loop: " + str(loop))
    # Mảng lưu tạm
    array = []
    for i in range(loop):
        # Lấy block comment
        pageData = driver.page_source
        html_page = BeautifulSoup(pageData, 'html.parser')
        reviews = html_page.find_all('li', {'class': 'review_list_new_item_block'})
        # Lặp qua tất cả các review
        for item in reviews:
            COUNT += 1
            # Lấy tên
            name = item.find('span', {'class': 'bui-avatar-block__title'}).get_text()
            # print(name)
            contry = item.find('span', {'class': 'bui-avatar-block__subtitle'})
            if contry is not None:
                contry = contry.get_text()
            else:
                contry = 'None'
            #     Tittle
            title = item.find('h3', {'class': 'c-review-block__title c-review__title--ltr'})
            if title is not None:
                title = title.get_text()
            else:
                title = 'Ẩn danh'
            comment = item.find('span', {'class': 'c-review__body'}).get_text()
            # Validation
            contry = contry.replace('\n', '')
            title = title.replace('\n', '')
            # Array temp
            array_temp = {'username': name, 'contry': contry, 'title': title, 'comment': comment}
            # Thêm vào mảng tổng
            array.append(array_temp)
        # Dừng 0.5s rồi next qua trang khác
        # print("-------------------------")
        btn_next_page = driver.find_element(by=By.XPATH, value="//a[@class='pagenext']")
        driver.execute_script("arguments[0].click();", btn_next_page)
        time.sleep(SLEEP_TIME)
    # END LOOP

    # print(array)
    return array


if __name__ == '__main__':
    COUNT = 0
    print('Run main')
    numPage = getMaximumPage()
    numLoop = round(int(numPage / 25))
    # numLoop = round(numLoop/3)
    page = 0
    print("Loop: " + str(numLoop))
    print("#######################")
    for idx in range(numLoop):
        print(str(page) + " - " + " Loop: " + str(idx))
        time.sleep(1)
        crawler(page)
        page = page + 25

    print("Tổng số comment: " + str(COUNT))
    print("Tổng số House: " + str(HOUSE))
    exportFile()
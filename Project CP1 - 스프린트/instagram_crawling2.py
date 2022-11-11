from urllib.request import urlopen
# 아스키코드로 변환
from urllib.parse import quote_plus as qp
from bs4 import BeautifulSoup
from selenium import webdriver
import time
# 스크롤을 위해 추가
from selenium.webdriver.common.keys import Keys


# 스크롤기능을 넣어서 대량으로 가져오려고 했는데 실패해서
# 인스타개인페이지로 들어가서 직접 받아오기로 했다.


# 아래코드가 성공하면 시도할 url
##baseurl = "https://www.instagram.com/leeji_ee/"
baseurl = 'https://www.instagram.com/'
plusurl = input('검색할 태그를 입력하세요 : ')
url = baseurl + qp(plusurl)
print(url)


# 인스타그램은 다음 페이지를 클릭해서 추가로 보는 방식이 아니라
# 스크롤을 내림으로써 이미지가 추가되는 방식이다.
# 그래서 bs가 아닌 webdriver를 써야 한다.
# 인스타페이지에서 우클릭으로 페이지소스보기하면 전부 자바스크립트(스크롤형식)로 쓰여있다.
# 그래서 BeautifulSoup으로 불러올 수가 없다.
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)  # 딜레이 방지용

# 스크롤 횟수 지정 예시
# scroll_cnt = int(input("스크롤 횟수 : "))
# scroll_cnt = 33
# for i in range(scroll_cnt):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 클래스가 _aabd _aa8k _aanf 3개라서
# 클래스 불러올거니깐 .을 붙이고 공간을 없앤다
insta = soup.select('._aabd._aa8k._aanf')

# 출력해보는게 중요하다. 작동이 안되는지 확인하기 위해서
# print(insta)#클래스에 해당하는 인스타의 모든정보를 가져온다
# print(insta[0])  # 다 가져오지 않고 첫 번째 정보만 가져온다

# 1개만 가져오개 아니라 여러개를 가져올 거라서 반복문을 쓴다
n = input('이미지로 저장할 시작 숫자 : ')
for i in insta:
    # print(i.a['href'])
    # href는 #(헤시태그)로 검색된 결과 중 해당 사진의 원주소를 말하는데
    # 예시) /p/Ckcm89JPEiv/ 처럼 나오는데
    # 이것만으로는 해당 페이지로 들어가기 어렵다.
    # 그래서 인스타그램주소를 더한 형태로 만들어 준다.
    print('https://www.instagram.com' + i.a['href'])

    # 이미지가 속한 src태그가 해당하는 클래스(.aagv) 가져온다.
    img_url = i.select_one('._aagv').img['src']  # 한개만 가져올거라 select_one()을 씀

    # 이미지 저장하기
    with urlopen(img_url) as f:
        # 텍스트가 아니라서 w대신 wb씀
        with open('C:/Users/coding-jang/Desktop/프로젝트/colorful_project/Project CP1 - 스프린트/img/' + plusurl + str(n) + '.jpg', 'wb') as h:
            # 저장위치 : img폴더
            # 파일명 : 검색어 + 순서,
            #         확장자:.jpg
            #         이미지 파일쓰기 : wb

            img = f.read()  # url open한걸 읽고 img폴더에 저장
            # h 에 img를 쓴다.
            h.write(img)
    # 반복하기 위해서
    n += 1
    print(img_url)
    print()  # 출력된 결과를 읽기 편하기 위해 빈줄을 추가함


driver.close()

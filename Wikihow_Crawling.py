from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as rep
import os

base = "https://ko.wikihow.com/"

# ------------------수정------------------------


maintheme = '두통'

theme = '부비동-두통-낫는-법'
# theme = '편두통-없애는-법'
# theme = '아이의-두통-낫게-하는-법'

# ------------------------------------------

quote = rep.quote_plus(theme)
url = base + quote

res = req.urlopen(url)

soup = BeautifulSoup(res,"html.parser")

txt_savePath = 'C:\\Pythonsource\\Workspace\\Crawling\\Project\\'+ str(maintheme) + '\\' + str(theme) + '\\txt'
img_savePath = 'C:\\Pythonsource\\Workspace\\Crawling\\Project\\'+ str(maintheme) + '\\' + str(theme) + "\\Images"

try:
    if not(os.path.isdir(txt_savePath)):
        os.makedirs(os.path.join(txt_savePath))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

try:
    if not(os.path.isdir(img_savePath)):
        os.makedirs(os.path.join(img_savePath))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

print('텍스트 크롤링 시작')
print()

f = open(txt_savePath + '\\' + str(theme) + '.txt', 'a', encoding='utf-8')


num_stage = len(soup.find_all('div', {"class": "section steps sticky"})) + 1    # 단계의 갯수.
ol_li_list = []       # 각 ol 안에 들어있는 list 태그를 저장한 리스트.


for a in range(1, num_stage + 1):
    t = "div#단계_" + str(a) + " > ol > li"
    ol_li = soup.select(t)            # 각 ol 안에 들어있는 list 태그의 갯수.
    ol_li_list.append(len(ol_li))   # 리스트에 저장.

first_list = []    # 텍스트 크롤링을 위한 Selector의 첫번째 부분을 저장한 리스트.

for a in range(1, num_stage + 1):
    first = "div#단계_" + str(a) + " > ol > li#step-id-" + str(a-1)   # 텍스트 크롤링을 위한 Selector의 첫번째 부분.
    first_list.append(first)                                         # 리스트에 저장.

num_contents = 0    # 텍스트를 크롤링할 게시물의 갯수. (default = 0)

url_list = []       # 텍스트 크롤링을 위한 최종 Selector를 저장한 리스트.

for n in range(0,num_stage):
    num_li = ol_li_list[n]              # 리스트에 저장되어 있는 각 ol 안의 list 태그 갯수를 하나씩 불러오기.
    first_selector = first_list[n]      # 리스트에 저장되어 있는 Selector의 첫번째 부분을 하나씩 불러오기.

    for e in range(0,num_li):
        final_url = first_selector + str(num_contents)      # 텍스트 크롤링을 위한 최종 Selector.
        num_contents += 1
        url_list.append(final_url)                          # 리스트에 저장.

index = 0                               # 크롤링한 텍스트의 순서를 표시할 인덱스.

for f_url in url_list:
    text = soup.select(f_url + " > div.step > b.whb")[0].getText()      # 최종 크롤링 과정.
    f.write(str(index+1))
    f.write('.' + ' ')
    f.write(text)
    f.write('\n')
    index += 1
f.close()
print('텍스트 크롤링 완료')
print()
print('========================')
print()
print('이미지 크롤링 시작')
print()

images = soup.select("div.mwimg.largeimage.floatcenter > a > div.content-spacer > img")     # 이미지 크롤링을 위한 Selector 경로.
for i, div in enumerate(images,1):
    fullfilename = os.path.join(img_savePath, str(i)+'.jpg')                     # 크롤링한 이미지를 저장할 경로 설정.
    print('{} : {} 크롤링 완료'.format(i, fullfilename))
    req.urlretrieve(div['data-src'],fullfilename)                                           # 이미지 크롤링 진행

print()
print("이미지 크롤링 완료")
print()
print('========================')
print()
print(theme, '크롤링 완료')
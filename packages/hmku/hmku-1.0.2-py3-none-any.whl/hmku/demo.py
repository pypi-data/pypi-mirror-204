import os
import json
from lxml import etree
import requests
import threading
import time
from zhconv import convert
import imghdr
requests.packages.urllib3.disable_warnings()

session = requests.session()


# 单本书采用多线程，开启多线程采集每一话的所有page

def get_json(mid):  # 得到一本漫画的所有章节

    json_url = f'https://www.hmku.top/index.php/api/comic/chapter?callback=jQuery22409895390228187688_1682343459921&mid={mid}'
    # 'jQuery22409895390228187688_1682343459921'
    resp = session.get(json_url, headers=hh).text
    mark = False
    new_resp = []
    for line in resp:
        if '(' == line:
            mark = True
            continue
        if mark == True:
            if ')' == line:
                mark = False
                continue
            new_resp.append(line)

    respond = json.loads(''.join(new_resp))['data']

    alone_book_list = []
    for line in respond:
        chapter_url = line['link']
        chapter_name = convert(line['name'], 'zh-cn')
        alone_book_list.append(
            {'chapter_name': chapter_name, 'chapter_url': chapter_url})

    # print(respond)
    return alone_book_list

    # print(resp['data'])


def get_mid_name(home_url):

    # home_url='https://www.hmku.top/index.php/manga/shendujiaoliuhui'

    resp = session.get(home_url, headers=hh).text

    # with open('tt.html','w',encoding='utf-8')as g:
    #     g.write(resp)
    resp1 = resp.replace('<!--', '').replace('-->', '')
    book_id = ''.join(etree.HTML(resp1).xpath(
        "//*[@class='send-gift']/@data-mid"))
    bookname = convert(''.join(etree.HTML(resp).xpath(
        "/html/head/title/text()")).split('-')[0].strip(), 'zh-cn')

    print(book_id, bookname)

    all_chapter = get_json(book_id)  # 开启多线程，这里是章节名字和章节链接

    # 设置多线程
    thread = []
    if not os.path.exists(f'./manga/{bookname}'):
        os.makedirs(f'./manga/{bookname}')
    for line in all_chapter:
        chapter_name = line['chapter_name'].replace(
            '&hellip;', '').replace('&ldquo;', '').replace('&rdquo;', '').replace('?', '？').replace(':', '').replace('.', '_')
        chapter_url = line['chapter_url']
        thread.append(threading.Thread(target=download,
                      args=(bookname, chapter_name, chapter_url)))

    # 启动多线程
    for line in thread:
        line.start()

    for line in thread:
        line.join()

    return bookname


def get_alone_chapter_all_page(url):

    # url='https://www.hmku.top/index.php/chapter/10812'
    while True:
        try:
            resp = session.get(url, timeout=5, verify=False, headers=hh).text
            break
        except:
            time.sleep(3)
    all_page = etree.HTML(resp).xpath(
        "//*[@class='read-container']/div[@class='rd-article-wr clearfix']/div/img/@data-original")

    # print(all_page)

    return all_page


def download(bookname, name, url):

    page_list = get_alone_chapter_all_page(url)
    print(name)
    num = 0
    new_down = []
    for line in page_list:
        # print(line,name,num)
        num += 1
        # continue
        new_down.append(threading.Thread(target=new_download,
                        args=(line, bookname, name, num)))  # 不影响更新
        # threading.Thread(target=new_download, args=(line,bookname,name,num)).start()
        # num+=1
    for ii in new_down:
        ii.start()

    for ii in new_down:
        ii.join()

    os.system('cls')
    return


hh = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}


def new_download(line, bookname, name, num):

    while True:
        if os.path.exists(f'./manga/{bookname}/{name}/{num}.jpg'):
            if os.path.getsize(f'./manga/{bookname}/{name}/{num}.jpg') <= 5:
                pass
            else:
                print(f'./manga/{bookname}/{name}/{num}.jpg', '已存在，pass')
                return
        # print(line)
        try:
            content = session.get(
                line, headers=hh, verify=False, timeout=5).content
            break
        except Exception as e:
            # print(e)
            print(e, 'waiting 3s')
            time.sleep(3)
            # content = session.get(line).content
    try:
        if not os.path.exists(f'./manga/{bookname}/{name}'):
            os.makedirs(f'./manga/{bookname}/{name}')
    except:
        pass

    with open(f'./manga/{bookname}/{name}/{num}.jpg', 'wb')as g:
        g.write(content)
        g.close()

    print(f'{bookname}/{name}/{num}.jpg', 'done!')
    return

# get_alone_chapter_all_page()
# get_json(1726l)
# get_mid_name()


# if __name__ == '__main__':
    # home_url = [
    #     'https://www.hmku.top/index.php/comic/shendujiaoliuhui',
    #     'https://www.hmku.top/index.php/comic/mimijiaohua',
    #     'https://www.hmku.top/index.php/comic/qiangzicantingdemamamen',
    #     'https://www.hmku.top/index.php/comic/selunyan',
    #     'https://www.hmku.top/index.php/comic/yuwangchengzhenapp',
    #     'https://www.hmku.top/index.php/comic/diaojiaokaiguan',
    #     'https://www.hmku.top/index.php/comic/zhichangxianjing',
    #     'https://www.hmku.top/index.php/comic/zizimendediaojiao',
    #     'https://www.hmku.top/index.php/comic/jimudepengyoumen',
    #     'https://www.hmku.top/index.php/comic/diwangapp',
    #     'https://www.hmku.top/index.php/comic/shechanhuazi',
    # ]

    # # print(resp)
    # # exit()
    # for line in home_url:

    #     name=get_mid_name(line)
    #     print(name,'下载完成！')
def main(home_url):
    name = get_mid_name(home_url)
    all_comic = os.listdir('./manga')

    for ii in all_comic:
        # print(ii)
        ll = os.listdir(f'./manga/{ii}')
        for pp in ll:
            all_pic = os.listdir(f'./manga/{ii}/{pp}')
            for oo in all_pic:
                file_name = (f'./manga/{ii}/{pp}/{oo}').replace('/', r'\\')
                # print(file_name)
                if imghdr.what(file_name) == None:
                    # print(file_name,'kkkkkkkk')
                    os.remove(file_name)
                    pass

    print(name, '下载完成！')

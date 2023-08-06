# import requests
# import threading
# import re
# import queue
# import os
#
# def get_urls():
#     url = r'https://image.baidu.com/search/acjson?'
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'}
#     pattern = '(http.*?jpg)'         #加括号，则会按照返回括号所匹配的结果，一个字符串多个括号，则会返回多个括号分别匹配到的结果：参考https://blog.csdn.net/qq_30534935/article/details/94589036
#     r = requests.get(url, headers = headers)
#
#     r.encoding = r.apparent_encoding  #修改内容的编码格式，否则可能是乱码
#
#     html = r.text     #r.text是网页内容，编码后内容; r.content返回的是二进制数据
#     img_urls = re.findall(pattern,html)
#
#     return img_urls
#
# a = get_urls()
# print(a)


'''

代码来自：https://zhuanlan.zhihu.com/p/367325899
'''

import requests
import os
import re


def get_images_from_baidu(keyword, page_num, save_dir):
    # UA 伪装：当前爬取信息伪装成浏览器
    # 将 User-Agent 封装到一个字典中
    # 【（网页右键 → 审查元素）或者 F12】 → 【Network】 → 【Ctrl+R】 → 左边选一项，右边在 【Response Hearders】 里查找
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    # 请求的 url
    url = 'https://image.baidu.com/search/acjson?'
    # url = 'https://www.google.com.hk/search?q=Pelvic+X-ray&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjF_NDO8d_9AhUOZt4KHahBBboQ_AUoAXoECAEQAw&biw=1707&bih=924&dpr=1.5'
    n = 0
    for pn in range(0, 30 * page_num, 30):
        # 请求参数
        param = {'tn': 'resultjson_com',
                 # 'logid': '7603311155072595725',
                 'ipn': 'rj',
                 'ct': 201326592,
                 'is': '',
                 'fp': 'result',
                 'queryWord': keyword,
                 'cl': 2,
                 'lm': -1,
                 'ie': 'utf-8',
                 'oe': 'utf-8',
                 'adpicid': '',
                 'st': -1,
                 'z': '',
                 'ic': '',
                 'hd': '',
                 'latest': '',
                 'copyright': '',
                 'word': keyword,
                 's': '',
                 'se': '',
                 'tab': '',
                 'width': '',
                 'height': '',
                 'face': 0,
                 'istype': 2,
                 'qc': '',
                 'nc': '1',
                 'fr': '',
                 'expermode': '',
                 'force': '',
                 'cg': '',    # 这个参数没公开，但是不可少
                 'pn': pn,    # 显示：30-60-90
                 'rn': '30',  # 每页显示 30 条
                 'gsm': '1e',
                 '1618827096642': ''
                 }
        request = requests.get(url=url, headers=header, params=param)
        if request.status_code == 200:
            print('Request success.')
        request.encoding = 'utf-8'
        # 正则方式提取图片链接
        html = request.text
        image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)
        print(image_url_list)
        # # 换一种方式
        # request_dict = request.json()
        # info_list = request_dict['data']
        # # 看它的值最后多了一个，删除掉
        # info_list.pop()
        # image_url_list = []
        # for info in info_list:
        #     image_url_list.append(info['thumbURL'])

        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        for image_url in image_url_list:
            image_data = requests.get(url=image_url, headers=header).content
            with open(os.path.join(save_dir, f'{n:06d}.jpg'), 'wb') as fp:
                fp.write(image_data)
            n = n + 1


if __name__ == '__main__':
    keyword = 'Pelvic X-ray'
    save_dir = "/home/xjm/xjm/xjm_pycharm/gupen/gupen_google/"
    page_num = 100
    get_images_from_baidu(keyword, page_num, save_dir)
    print('Get images finished.')
import requests
import re
import os
import argparse
import urllib.parse

def get_image_urls(query, num_images):
    # 编码查询词为 URL 格式
    query = urllib.parse.quote(query)
    # 设置请求头信息
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    # 设置要请求的 URL
    url = "https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
    # 发送 GET 请求并获取结果
    response = requests.get(url, headers=headers).text
    # 从结果中提取图片链接
    image_urls = re.findall('"ou":"(.*?)"', response)[:num_images]
    return image_urls

def download_image(url, save_path):
    # 设置请求头信息
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    # 发送 GET 请求并保存图片
    response = requests.get(url, headers=headers)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def main():
    # 设置参数解析器
    parser = argparse.ArgumentParser(description='Google 图片爬取')
    parser.add_argument('--query', type=str, default='cat', help='查询词')
    parser.add_argument('--num_images', type=int, default=10, help='要下载的图片数量')
    parser.add_argument('--save_directory', type=str, default='./images', help='保存目录')
    args = parser.parse_args()

    # 获取要下载的图片链接
    image_urls = get_image_urls(args.query, args.num_images)

    # 创建保存目录
    if not os.path.exists(args.save_directory):
        os.makedirs(args.save_directory)

    # 下载并保存图片
    for i, url in enumerate(image_urls):
        save_path = os.path.join(args.save_directory, f"{i}.jpg")
        download_image(url, save_path)
        print(f"{i+1}/{args.num_images} images downloaded from {url} to {save_path}")

if __name__ == '__main__':
    main()

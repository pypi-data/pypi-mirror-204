# Created by Han Xu
# email:736946693@qq.com
# Created by Han Xu
# email:736946693@qq.com
import requests
import urllib.parse
import os
import re

class pixiv_keyword_spider():
    def __init__(self):
        """
        @:brief
        @:return
        """
        self.path=input("type in the path where you want to reserve the images:")

        self.url="https://www.pixiv.net/ajax/search/artworks/"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
            "referer": "https://www.pixiv.net/",

        }

        self.keyword = input("type in the keywords used to search in pixiv:")
        self.paginator = int(input("Type in the number of pages you want.Each page has almost 70 images:"))

    def get_urls(self):
        """
        @:brief Get the URLs that you need to visit.
        @:return return a list of the URLs
        """
        keyword = urllib.parse.quote(self.keyword)
        params = []
        for i in range(1, self.paginator + 1):
            params.append(
                "{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh&version=c4032a21df2a82afb72b3fd753afb10a037befb5".format(
                    keyword,
                    keyword,
                    i))
        urls = []
        for i in params:
            urls.append(self.url + i)
        return urls


    def get_path(self):
        """
        @:brief Get the path where you want to reserve the images.
        @:return
        """
        dirname="./"+self.path
        dirname_origin = dirname
        int_index = 0
        while(True):
            IsExist = os.path.exists(dirname)
            if (IsExist==False):
                os.mkdir(dirname)
                IsCreate=True
                break
            else:
                int_index+=1
                dirname=dirname_origin+"({})".format(int_index)

        return dirname+"/"

    def get_profile_url(self, urls):
        """
        @:brief Get the URLs of specific page including the image.
        @:return the URLs of specific page including the image
        """
        profile_urls = []
        for each_url in urls:
            response = requests.get(each_url, headers=self.headers)
            if (response.status_code != 403 and response.status_code != 404):
                url_txt = response.text
                pattern = re.compile('"id":"[0-9]+[^"]')
                id_list = pattern.findall(url_txt)
                for i in id_list:
                    if i:
                        i = i[i.rfind(":")+2:]
                        print(i)
                        profile_urls.append("https://www.pixiv.net/artworks/" + i)
            else:
                raise Exception("the invalid url:{}!".format(each_url))
        return profile_urls


    def get_image_urls(self, profile_urls):
        """
        @:brief Get the URLs of images.
        @:return a list of URLs of images
        """
        image_urls = []
        for url in profile_urls:
            url_txt = requests.get(url, headers=self.headers).text
            pattern = re.compile('"regular":"[\S][^"]+')
            url_list=pattern.findall(url_txt)
            for i in url_list:
                if i:
                    i=i[i.rfind("http"):]
                    image_urls.append(i)
        return image_urls


    def get_image(self,images_urls):
        """
        @:brief download the images into the path you set just
        @:return
        """
        m = 1
        for img_url in images_urls:
            # 定义一个flag用于判断下载图片是否异常
            flag = True
            try:
                print("第{}张图片的URL是{}".format(m, img_url))
                response = requests.get(img_url, headers=self.headers)
                if (flag):
                    # 下载完成提示
                    with open(self.path + str(m) + img_url[img_url.rfind("."):], "wb+") as f:
                        f.write(response.content)
                        print('**********第' + str(m) + '张图片下载完成********')
                        print("保存于{}".format(os.getcwd() + self.path[1:]))
                        # 每下载完后一张,m累加一次
                        m = m + 1
            except BaseException as error:
                flag = False
                print(error)
        print('下载完成!')
        return

    def __call__(self, *args, **kwargs):
        """
        @brief the constrcution of the class
        @:return
        """
        self.path=self.get_path()
        urls = self.get_urls()
        profile_url = self.get_profile_url(urls)
        image_urls=self.get_image_urls(profile_urls=profile_url)
        self.get_image(image_urls)
        return

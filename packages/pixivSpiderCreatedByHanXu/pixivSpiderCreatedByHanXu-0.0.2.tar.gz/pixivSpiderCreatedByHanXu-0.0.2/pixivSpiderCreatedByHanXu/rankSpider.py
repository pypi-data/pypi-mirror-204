# Created by Han Xu
# email:736946693@qq.com
import requests
import os
import re

class pixiv_rank_spider():
    def __init__(self):
        """
        @:brief
        @:return
        """
        self.searchMode_dict={"1":"daily","2":"weekly","3":"monthly","4":"rookie","5":"daily_ai","6":"male","7":"female"}
        print(self.searchMode_dict)
        self.searchMode=self.searchMode_dict[input("type in the searchMode you want")]


        self.date=input("Type in the date you want to search.Follow the format like this:20230423")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
            "referer": "https://www.pixiv.net/",

        }
        self.path = input("type in the path where you want to reserve the images:")
        self.paginator = int(input("Type in the number of pages you want.Each page has almost 50 images:"))
        self.url_front = "https://www.pixiv.net/ranking.php?mode={}&date={}&format=json&p=".format(self.searchMode,self.date)


    def get_urls(self):
        """
        @:brief Get the URLs that you need to visit.
        @:return a list of the URLs
        """
        urls=[]
        for i in range(1,self.paginator+1):
            urls.append(self.url_front+str(i))
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

    def get_images_urls(self, urls):
        """
        @:brief Get the URLs of images.
        @:return a list of URLs of images
        """
        images_urls = []
        for each_url in urls:
            response = requests.get(each_url, headers=self.headers)
            if  (response.status_code!=403 and response.status_code!=404):
                url_txt=response.text
                pattern = re.compile('"url":"[^"]+')
                image_list=pattern.findall(url_txt)
                for i in image_list:
                    if i:
                        i=i[i.rfind("img"):]
                        i=i.replace("\\","")
                        images_urls.append("https://i.pximg.net/img-master/"+i)
            else:
                raise Exception("the invalid url:{}!".format(each_url))
        return images_urls

    def get_images(self,images_urls):
        """
        @:brief download the images into the path you set just
        @:return
        """
        m = 1
        for img_url in images_urls:
            #定义一个flag用于判断下载图片是否异常
            flag=True
            try:
                print("第{}张图片的URL是{}".format(m,img_url))
                response=requests.get(img_url,headers=self.headers)
                if (flag):
                    # 下载完成提示
                    with open(self.path + str(m) + img_url[img_url.rfind("."):], "wb+") as f:
                        f.write(response.content)
                        print('**********第' + str(m) + '张图片下载完成********')
                        print("保存于{}".format(os.getcwd() + self.path[1:]))
                        # 每下载完后一张,m累加一次
                        m = m + 1

            except BaseException as error:
                    flag=False
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
        image_url = self.get_images_urls(urls)
        self.get_images(image_url)
        return

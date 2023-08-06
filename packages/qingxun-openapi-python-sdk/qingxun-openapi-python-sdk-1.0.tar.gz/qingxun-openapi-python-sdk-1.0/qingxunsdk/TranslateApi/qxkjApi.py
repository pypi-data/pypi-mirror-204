# -*- coding: UTF-8 -*-
import random
import string
import requests
import hashlib
from requests_toolbelt import MultipartEncoder



class qxkj_api():

    def __init__(self,ip,appid,privatekey):

        self.appid = appid
        self.privatekey = privatekey
        self.ip = "https://"+ip

    def file_md5(self,file_name):
        with open(file_name, 'rb') as fp:
            data = fp.read()
        file_md5 = hashlib.md5(data).hexdigest()
        return file_md5.lower()

    def get_token(self,stringdict):
        stringA = ""
        for key in sorted(stringdict.keys()):
            stringA += key + "=" + stringdict.get(key) + "&"

        token = hashlib.md5(stringA[:-1].encode("utf-8")).hexdigest().upper()

        return token

    def get_nonce_str(self):

        return ''.join(random.choice(string.ascii_letters) for x in range(16))

    # 文件上传
    def uploadTranslate(self,from_,to,filepath,filename,**params):

        """
        文件上传
        :param from_:源语言
        :param to:目标语言
        :param filepath:本地文件地址
        :param filename:文件名
        :param params:可选参数（industryId，transImg，excelMode，bilingualControl）
        :return:
        """

        # 文档上传有四个追加参数
        # industryId	行业代码	int	见行业列表	否
        # transImg	文档内图片翻译	int	0：不翻译文档内图片（默认），1：翻译文档内图片。目前支持中、英、日、韩的文档内图片翻译。（如有需要请联系销售开通）
        # excelMode	指定excel翻译模式	int	0：只翻译当前打开sheet（默认），1：翻译全部sheet（页数按全部sheet字符数来计算）
        # bilingualControl	指定翻译模式	int	0：译文单独为一个文档（默认），1：双语对照（原文和译文在一个文档）
        # 可以在参数后边用（industryId = 0 ,transImg=0 , excelMode = 0,bilingualControl=0）进行追加


        uploadTranslateURL = self.ip + "/TransateApi/api/uploadTranslate"

        filemd5 = self.file_md5(filepath)

        nonce_str = self.get_nonce_str()

        stringdict = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "from": from_,
            "to": to,
            "md5": filemd5,
            "privatekey": self.privatekey
        }
        for key in params.keys():
            stringdict[key] = params.get(key)

        fields = {
            "appid": self.appid,
            "token": self.get_token(stringdict),
            "nonce_str": nonce_str,
            "from": from_,
            "to": to,
            "md5": filemd5,
            'file': (filename, open(filepath, "rb")),
        }

        for key in params.keys():
            fields[key] = params.get(key)


        m = MultipartEncoder(
            fields= fields
        )
        header = {
            'Content-Type': m.content_type,
        }
        response = requests.post(url=uploadTranslateURL, data=m,headers=header)
        return response.json()

    # 获取进度
    def queryTransProgress(self, tid):

        """
        获取翻译进度
        :param tid: 文档id
        :return:
        """

        nonce_str = self.get_nonce_str()

        stringdict = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "tid": tid,
            "privatekey": self.privatekey
        }

        m = MultipartEncoder(

            fields={
                "appid": self.appid,
                "token": self.get_token(stringdict),
                "nonce_str": nonce_str,
                "tid": tid,

            }
        )

        header = {
            'Content-Type': m.content_type,
        }

        return  requests.post(self.ip + "/TranslateApi/api/queryTransProgress", data=m, headers=header).json()

    # 取消任务
    def cancel(self, tid):
        """
        取消翻译任务
        :param tid: 文档id
        :return:
        """
        cancelURL = self.ip + "/TranslateApi/api/cancel"
        nonce_str = self.get_nonce_str()
        stringdict = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "tid": tid,
            "privatekey": self.privatekey
        }

        m = MultipartEncoder(

            fields={
                "appid": self.appid,
                "token": self.get_token(stringdict),
                "nonce_str": nonce_str,
                "tid": tid,
            }
        )

        header = {
            'Content-Type': m.content_type,
        }

        return requests.post(cancelURL, data=m, headers=header).json()

    # 下载
    def downloadFile(self, tid,dtype):

        """
        下载翻译后的文档
        :param tid: 文档id
        :param dtype: 类型
        :return:
        """

        downloadFileURL = self.ip + "/TranslateApi/api/downloadFile"
        nonce_str = self.get_nonce_str()
        stringdict = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "dtype": dtype,
            "tid": tid,
            "privatekey": self.privatekey
        }

        m = MultipartEncoder(

            fields={
                "appid": self.appid,
                "nonce_str": nonce_str,
                "token": self.get_token(stringdict),
                "dtype": dtype,
                "tid": tid,
            }
        )

        header = {
            'Content-Type': m.content_type,
        }

        r = requests.post(downloadFileURL, data=m, headers=header)

        if r.headers["Content-Type"] in 'application/octet-stream;charset=UTF-8':
            return r.text
        else:
            return "下载失败！"

    # 文字翻译
    def trans(self,from_,to,text):
        """
        文字翻译
        :param from_: 源语言
        :param to: 目标语言
        :param text: 文字
        :return:
        """
        transURL = self.ip + "/TranslateApi/api/trans"

        nonce_str = self.get_nonce_str()

        stringdict = {

            "appid": self.appid,
            "nonce_str": nonce_str,
            "from": from_,
            "to": to,
            "text": text,
            "privatekey": self.privatekey
        }

        data = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "token": self.get_token(stringdict),
            "from": from_,
            "to": to,
            "text": text,
        }
        response = requests.post(transURL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

        return response.json()


    #上传文件检测页数
    def detectDocPage(self,filepath,filename):

        """
        上传文件检测页数
        :param filepath: 本地文件地址
        :param filename: 文件名
        :return:
        """

        detectDocPageURL = self.ip + "/TranslateApi/api/detectDocPage"

        nonce_str = self.get_nonce_str()

        filemd5 = self.file_md5(filepath)

        stringdict = {

            "appid": self.appid,
            "nonce_str": nonce_str,
            "md5": filemd5,
            "privatekey": self.privatekey
        }

        fields = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "token": self.get_token(stringdict),
            "md5": filemd5,
            'file': (filename, open(filepath, "rb")),
        }


        m = MultipartEncoder(
            fields=fields
        )
        header = {
            'Content-Type': m.content_type,
        }
        response = requests.post(url=detectDocPageURL, data=m, headers=header)
        return response.json()


    # 检测页数文件提交翻译
    def submitForDetectDoc(self,tid,from_,to,**params):

        """
        检测页数文件提交翻译
        :param tid:文档id
        :param from_:源语言
        :param to:目标语言
        :param params:可选参数（industryIdindustryId,transImg,excelMode,bilingualControl）
        :return:
        """
        # industryId 行业代码 int 见行业列表 否
        # transImg 文档内图片翻译 int 0：不翻译文档内图片（默认），1：翻译文档内图片。目前支持中、英、日、韩的文档内图片翻译。（如有需要请联系销售开通）    否
        # excelMode 指定excel翻译模式 int 0：只翻译当前打开sheet（默认），1：翻译全部sheet（页数按全部sheet字符数来计算）    否
        # bilingualControl  指定翻译模式int 0：译文单独为一个文档（默认），1：双语对照（原文和译文在一个文档）    否

        submitForDetectDocURL = self.ip + "/TranslateApi/api/submitForDetectDoc"

        nonce_str = self.get_nonce_str()

        stringdict = {

            "appid": self.appid,
            "nonce_str": nonce_str,
            "tid": tid,
            "from": from_,
            "to": to,
            "privatekey": self.privatekey
        }

        for key in params.keys():
            stringdict[key] = params.get(key)

        data = {
            "appid": self.appid,
            "token": self.get_token(stringdict),
            "nonce_str": nonce_str,
            "tid": tid,
            "from": from_,
            "to": to,
        }

        for key in params.keys():
            data[key] = params.get(key)

        response = requests.post(submitForDetectDocURL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

        return response.json()

    # 文档转换
    def convert(self,filepath,filename,conversionFormat,**params):

        """
        文档转换
        :param filepath:本地文件地址
        :param filename:文件名
        :param conversionFormat:转换的目标格式
        :param params:一个可选参数（from）源文件的语言（扫描件需设置语言）
        :return:
        """

        convertURL = self.ip + "/TranslateApi/api/convert"

        nonce_str = self.get_nonce_str()

        filemd5 = self.file_md5(filepath)

        stringdict = {

            "appid": self.appid,
            "nonce_str": nonce_str,
            "conversionFormat":conversionFormat,
            "md5": filemd5,
            "privatekey": self.privatekey
        }
        for key in params.keys():
            stringdict[key] = params.get(key)

        fields = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "conversionFormat":conversionFormat,
            "md5": filemd5,
            'file': (filename, open(filepath, "rb")),
            "token": self.get_token(stringdict),
        }

        for key in params.keys():
            fields[key] = params.get(key)

        m = MultipartEncoder(
            fields=fields
        )
        header = {
            'Content-Type': m.content_type,
        }
        response = requests.post(url=convertURL, data=m, headers=header)
        return response.json()

    #获取账户信息
    def getAccount(self,**params):
        """
        获取账户信息
        :param params:type(资源包类型 1.文档翻译 2.文字翻译 3.图片翻译 4.格式转换)
        :return:
        """
        getAccountURL = self.ip + "/TranslateApi/api/getAccount"

        nonce_str = self.get_nonce_str()

        stringdict = {

            "appid": self.appid,
            "nonce_str": nonce_str,
            "privatekey": self.privatekey
        }
        for key in params.keys():
            stringdict[key] = params.get(key)

        data = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "token": self.get_token(stringdict),
        }

        for key in params.keys():
            data[key] = params.get(key)

        response = requests.post(getAccountURL, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})

        return response.json()

    # 图片上传并翻译
    def uploadTranslateImage(self,from_,to,filepath,filename):
        """

        :param from_:源语言
        :param to:目标语言
        :param filepath:图片路径
        :param filename:图片名称
        :return:
        """

        if filepath.split(".")[-1] in ["jpg","jpeg","png","bmp"]:

            uploadTranslateImageURL = self.ip + "/TranslateApi/api/image/uploadTranslateImage"

            nonce_str = self.get_nonce_str()

            filemd5 = self.file_md5(filepath)

            stringdict = {

                "appid": self.appid,
                "nonce_str": nonce_str,
                "from": from_,
                "to": to,
                "md5": filemd5,
                "privatekey": self.privatekey
            }

            fields = {
                "appid": self.appid,
                "nonce_str": nonce_str,
                "from": from_,
                "to": to,
                "md5": filemd5,
                'file': (filename, open(filepath, "rb")),
                "token": self.get_token(stringdict),
            }


            m = MultipartEncoder(
                fields=fields
            )
            header = {
                'Content-Type': m.content_type,
            }
            response = requests.post(url=uploadTranslateImageURL, data=m, headers=header)
            return response.json()
        else:
            return "请上传符合类型的图片！！！"

    #图片翻译获取进度
    def queryImageTransProgress(self,tid):
        """
        图片翻译获取进度
        :param tid:图片id
        :return:
        """
        queryImageTransProgressURL = self.ip + "/TranslateApi/api/image/queryImageTransProgress"


        nonce_str = self.get_nonce_str()

        stringdict = {

            "appid": self.appid,
            "nonce_str": nonce_str,
            "tid": tid,
            "privatekey": self.privatekey
        }


        fields = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "tid": tid,
            "token": self.get_token(stringdict),
        }


        m = MultipartEncoder(
            fields=fields
        )
        header = {
            'Content-Type': m.content_type,
        }
        response = requests.post(url=queryImageTransProgressURL, data=m, headers=header)
        return response.json()

    #图片翻译下载
    def downloadImage(self,tid):

        """
        图片翻译下载
        :param tid: 图片id
        :return:
        """
        downloadImageURL = self.ip + "/TranslateApi/api/image/downloadImage"

        nonce_str = self.get_nonce_str()
        stringdict = {
            "appid": self.appid,
            "nonce_str": nonce_str,
            "tid": tid,
            "privatekey": self.privatekey
        }

        m = MultipartEncoder(

            fields={
                "appid": self.appid,
                "nonce_str": nonce_str,
                "tid": tid,
                "token": self.get_token(stringdict),
            }
        )

        header = {
            'Content-Type': m.content_type,
        }

        r = requests.post(downloadImageURL, data=m, headers=header)

        if r.headers["Content-Type"] in 'application/octet-stream;charset=UTF-8':
            return r.text
        else:
            return "下载失败！"

    # OCR上传
    def ocrUploadImage(self,from_,filepath,filename):
        """
        OCR上传
        :param from_:源语言
        :param filepath:本地文件地址
        :param filename:图片名称
        :return:
        """
        if filepath.split(".")[-1] in ["jpg", "jpeg", "png", "bmp"]:

            ocrUploadImageURL = self.ip + "/TranslateApi/api/image/ocrUploadImage"

            nonce_str = self.get_nonce_str()

            filemd5 = self.file_md5(filepath)

            stringdict = {

                "appid": self.appid,
                "nonce_str": nonce_str,
                "from": from_,
                "md5": filemd5,
                "privatekey": self.privatekey
            }

            fields = {
                "appid": self.appid,
                "nonce_str": nonce_str,
                "from": from_,
                "md5": filemd5,
                'file': (filename, open(filepath, "rb")),
                "token": self.get_token(stringdict),
            }

            m = MultipartEncoder(
                fields=fields
            )
            header = {
                'Content-Type': m.content_type,
            }
            response = requests.post(url=ocrUploadImageURL, data=m, headers=header)
            return response.json()
        else:
            return "请上传符合类型的图片！！！"


    def dict_search(self,word):

        # 词语，小于等于15个字符
        if len(word) > 0 and len(word) < 16:
            dict_searchURL = self.ip + "/TranslateApi/api/dict/search"

            nonce_str = self.get_nonce_str()

            stringdict = {

                "appid": self.appid,
                "nonce_str": nonce_str,
                "word": word
            }

            fields = {
                "appid": self.appid,
                "nonce_str": nonce_str,
                "word": word,
                "token": self.get_token(stringdict)
            }

            m = MultipartEncoder(
                fields=fields
            )
            header = {
                'Content-Type': m.content_type,
            }
            response = requests.post(url=dict_searchURL, data=m, headers=header)
            return response.json()
        else:
            return "参数word不符合规格，字符数需大于0小于等于15！！！"




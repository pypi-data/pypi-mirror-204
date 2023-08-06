import oss2
import datetime
from .config import read, read_alioss, save_config
import argparse
import sys
import asyncio
import logging
from ._result import Result
from .utils import sign_dict
import requests
import json
from itertools import islice

def test():
    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
    auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret')

    # Endpoint以杭州为例，其它Region请按实际情况填写。
    # 填写Bucket名称，例如examplebucket。
    bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'examplebucket')
    # 填写Object的完整路径，完整路径中不能包含Bucket名称，例如exampledir/exampleobject.txt。
    # 需确保该Object的存储类型为标准存储或低频访问类型。
    object_name = 'exampledir/exampleobject.txt'

    # 通过添加存储类型Header，将Object存储类型转换为归档类型。
    headers = {'x-oss-storage-class': oss2.BUCKET_STORAGE_CLASS_ARCHIVE}
    # 通过添加存储类型Header，将Object存储类型转换为冷归档类型。
    # headers = {'x-oss-storage-class': oss2.BUCKET_STORAGE_CLASS_COLD_ARCHIVE}

    # 更改文件存储类型。
    bucket.copy_object(bucket.bucket_name, object_name, object_name, headers)

log = logging.getLogger(__name__)

class AliOSS:
    def __init__(self, version: str, host: str, appid: str, appsecret: str,access_key_id,access_secret) -> None:
        self.version = version
        self.host = host
        self.appid = appid
        self.appsecret = appsecret
        self.auth = oss2.Auth(access_key_id, access_secret)

    async def query(self, url: str, **kwargs):
        sign, nonce = sign_dict(kwargs, self.appsecret)

        url = f'{self.host}{url}&appid={self.appid}&nonce={nonce}&sign={sign}&version={self.version}'

        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(
            kwargs), headers=headers) if kwargs else requests.get(url, headers=headers)

        if(response.status_code == 200):
            value = response.json()

            res = Result(
                success=value.get('success'),
                msg=value.get('msg'),
                data=value.get('data'),
                wait=value.get('wait')
            )
            return res
        else:
            return Result(True, msg=f'{response.text},{response.status_code}', wait=5)

    async def get333(self) -> Result:
        res = await self.query('/publish/archive?action=get')
        if not res.success:
            print(res.msg)
            return
        if not res.data:
            print('没有需要归档的资源')
            return
        for item in res.data:
            print(item)

    async def get(self):
        """ bucket = oss2.Bucket(self.auth, 'https://oss-cn-hangzhou.aliyuncs.com', '6340eddedae02a645bd38226')
        for b in islice(oss2.ObjectIterator(bucket,prefix='20221205/',delimiter='/'),2):
            obj:oss2.models.SimplifiedObjectInfo = b
            print(obj.key,obj.storage_class) """
        bucket = oss2.Bucket(self.auth,'https://oss-cn-hangzhou.aliyuncs.com','zhixiang-video')

        for b in oss2.ObjectIterator(bucket):
            if b.storage_class == oss2.BUCKET_STORAGE_CLASS_STANDARD:
                headers = {'x-oss-storage-class': oss2.BUCKET_STORAGE_CLASS_ARCHIVE}
                res = bucket.copy_object(bucket.bucket_name, b.key, b.key, headers)
                print(b.key,res.status)
        
    async def archive(self,bucket_name:str):
        bucket = oss2.Bucket(self.auth, 'https://oss-cn-hangzhou.aliyuncs.com', bucket_name)
        
        curr = datetime.datetime.now() + datetime.timedelta(days=-100)
        earliest = datetime.datetime(2022,12,5)
        
        while curr>earliest:
            prefix = curr.strftime('%Y%m%d')
            print(f'{"-"*20}{prefix}{"-"*20}')
            i = 0
            for b in oss2.ObjectIterator(bucket,prefix=f'{prefix}/',delimiter='/'):
                obj:oss2.models.SimplifiedObjectInfo = b
                i+=1
                if obj.storage_class==oss2.BUCKET_STORAGE_CLASS_STANDARD:
                    headers = {'x-oss-storage-class': oss2.BUCKET_STORAGE_CLASS_ARCHIVE}
                    res = bucket.copy_object(bucket.bucket_name, b.key, b.key, headers)
                    print(f'{i}){obj.key} {res.status}')

            print(f'结束，共{i}个文件')

            curr = curr + datetime.timedelta(days=-1)
            
    
async def run(version, host, appid, appsecret,access_key_id,access_secret,bucket_name):
    instance = AliOSS(version, host, appid, appsecret,access_key_id,access_secret)
    await instance.archive(bucket_name)

def main():
    version, host, appid, appsecret = read()
    if not appid or not appsecret:
        return
    access_key_id,access_secret,bucket = read_alioss()
    if not access_key_id or not access_secret or not bucket:
        return
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-appid', type=str, default='')
    parser.add_argument('-appsecret', type=str, default='')
    parser.add_argument('-host', type=str, default='')
    parser.add_argument('-bucket', type=str, default='')
    args = parser.parse_args()

    if args.host and args.host!=host:
        host = args.host
        save_config('server','host',host)

    if args.appid and args.appid!=appid:
        appid = args.appid
        save_config('server','appid',appid)

    if args.appsecret and args.appsecret!=appsecret:
        appsecret = args.appsecret
        save_config('server','appsecret',appsecret)
    
    if args.bucket and args.bucket!=bucket:
        bucket = args.bucket
        save_config('alioss','bucket',bucket)

    if sys.version_info.minor >= 10:
        asyncio.run(run(version, host, appid, appsecret,access_key_id,access_secret,bucket))
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(version, host, appid, appsecret,access_key_id,access_secret,bucket))
        loop.close()
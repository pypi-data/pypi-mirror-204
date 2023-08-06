# -*- coding: utf-8 -*-

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging


class COS:
    def __init__(self, secret_id, secret_key, region, bucket, scheme='https'):
        """
        初始化COS对象
        :param secret_id: COS API密钥ID
        :param secret_key: COS API密钥Key
        :param region: COS服务所在地区，例如：ap-guangzhou
        :param bucket: COS Bucket名称
        """
        self.region = region
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.bucket = bucket
        self.scheme = scheme
        # self.endpoint = f'cos.{region}.myqcloud.com'
        # self.domain = f'cos.{region}.myqcloud.com'
        config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Scheme=self.scheme
                           # Endpoint=self.endpoint, Domain=self.domain,
                           )
        self.client = CosS3Client(config)

    def set_log_level(self, level=logging.INFO):
        logging.basicConfig(level=level, stream=sys.stdout)

    def upload_file(self, local_file, cos_file):
        """
        上传文件到COS
        :param local_file: 本地文件路径，例如：/path/to/local_file.txt
        :param cos_file: COS文件路径，例如：/data/cos_file.txt
        """
        # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
        try:
            response = self.client.upload_file(
                Bucket=self.bucket,
                LocalFilePath=local_file,
                Key=cos_file,
                PartSize=1,
                MAXThread=10,
                EnableMD5=False
            )
            print("COS：文件上传成功, ", response['ETag'])
            return True
        except Exception as e:
            raise Exception("upload_file error", e)

    def download_file(self, cos_file, local_file):
        """
        从COS下载文件
        :param cos_file: COS文件路径，例如：/data/cos_file.txt
        :param local_file: 本地文件路径，例如：/path/to/local_file.txt
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket,
                Key=cos_file,
            )
            response['Body'].get_stream_to_file(local_file)
            return True
        except Exception as e:
            raise Exception("download_file error", e)

from .oss_config import oss_info
import oss2

def oss_endpoint():
    info = oss_info()
    return info['oss_endpoint']

def oss_access_key():
    info = oss_info()
    return info['oss_access_key_id']

def oss_access_secret():
    info = oss_info()
    return info['oss_access_key_secret']

def oss_bucket():
    info = oss_info()
    return info['oss_bucket']


def show_list():
    access_id = oss_access_key()
    access_secret = oss_access_secret()
    bucket = oss_bucket()
    endpoint = oss_endpoint()

    auth = oss2.Auth(access_id, access_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket)
    for object_info in oss2.ObjectIterator(bucket):
        print(object_info.key)



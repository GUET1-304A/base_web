import logging
import oss2
from flask import current_app

logger = logging.getLogger(__name__)

_bucket = None


def get_bucket():
    global _bucket
    if _bucket is not None:
        return _bucket

    ak = current_app.config.get('ALIYUN_ACCESS_KEY_ID', '')
    sk = current_app.config.get('ALIYUN_ACCESS_KEY_SECRET', '')
    endpoint = current_app.config.get('ALIYUN_OSS_ENDPOINT', '')
    bucket_name = current_app.config.get('ALIYUN_OSS_BUCKET_NAME', '')

    if not all([ak, sk, endpoint, bucket_name]):
        return None

    auth = oss2.Auth(ak, sk)
    _bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return _bucket


def _get_public_url(key):
    bucket_name = current_app.config.get('ALIYUN_OSS_BUCKET_NAME', '')
    endpoint = current_app.config.get('ALIYUN_OSS_ENDPOINT', '')
    cdn = current_app.config.get('ALIYUN_OSS_CDN_URL', '')

    if cdn:
        return f"{cdn.rstrip('/')}/{key}"
    return f"https://{bucket_name}.{endpoint}/{key}"


def upload_file(key, data):
    bucket = get_bucket()
    if not bucket:
        return None

    try:
        bucket.put_object(key, data)
        logger.info(f"OSS upload success: {key}")
        return _get_public_url(key)
    except Exception as e:
        logger.error(f"OSS upload failed: {e}")
        return None


def delete_file(key):
    bucket = get_bucket()
    if not bucket:
        return False

    try:
        bucket.delete_object(key)
        logger.info(f"OSS delete success: {key}")
        return True
    except Exception as e:
        logger.error(f"OSS delete failed: {e}")
        return False

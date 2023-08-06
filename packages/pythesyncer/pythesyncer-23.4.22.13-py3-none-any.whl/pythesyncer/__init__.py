# --------------------------------------------
import asyncio
import os
import sys
import threading
from enum import Enum
import aiohttp
import boto3
import codefast as cf
import fire
from boto3.s3.transfer import TransferConfig
from codefast.asyncio import asyncformer
from rich import print

from .auth import auth

# —--------------------------------------------
KEY = 'pythesyncer'
REDIS_API = auth.redis_api


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" %
                (self._filename, self._seen_so_far, self._size, percentage))
            sys.stdout.flush()
        return "ok"


def upload_file(fn: str):
    config = TransferConfig(max_concurrency=3)
    s3 = boto3.client('s3',
                      endpoint_url=auth.r2_endpoint,
                      aws_access_key_id=auth.r2_access_key_id,
                      aws_secret_access_key=auth.r2_access_key_secret)

    bn = cf.io.basename(fn)
    return s3.upload_file(fn,
                          'cache',
                          bn,
                          Callback=ProgressPercentage(fn),
                          Config=config)


class Action(Enum):
    up = 'up'
    down = 'down'


async def sync(action: Action, obj):
    if action == Action.up:
        await sync_up(obj)
    elif action == Action.down:
        await sync_down(obj)


async def sync_up(obj):
    file_name=cf.io.basename(obj)
    if os.path.isfile(obj):
        cf.info('Uploading file: {}'.format(obj))
        await asyncformer(upload_file, obj)

    elif os.path.isdir(obj):
        cf.info('Uploading dir: {}'.format(obj))
        zipname = cf.random_string(16)
        zipfile = zipname+'.7z'
        os.system(
            '7z a -t7z -m0=lzma2 -mx=9 -mfb=64 -md=32m -ms=on {} {}'.
            format(zipfile, obj))
        await asyncformer(upload_file, zipfile)
        os.remove(zipfile)
        cf.info("Upload done: {}".format(zipfile))
        file_name = zipfile

    async with aiohttp.ClientSession() as session:
        async with session.post(REDIS_API, json={'key': KEY, 'value': file_name}) as resp:
            if resp.status != 200:
                cf.error('Failed to get redis key: {}'.format(KEY))


async def sync_down(obj):
    if not obj:
        async with aiohttp.ClientSession() as session:
            async with session.post(REDIS_API, json={'key': KEY}) as resp:
                if resp.status != 200:
                    cf.error('Failed to get redis key: {}'.format(KEY))
                js = await resp.json()
                obj = js['value']
    remote_file = os.path.join(auth.host_api, obj)
    await asyncformer(cf.net.download, remote_file, obj)


def entry(action: str, obj: str = None):
    if action not in [a.value for a in Action]:
        print('Action must be one of {}'.format([a.value for a in Action]))
        return
    action = Action(action)
    if action == Action.up and not obj:
        print('Uploading object must be specified')
        return
    asyncio.run(sync(action, obj))


def main():
    fire.Fire(entry)

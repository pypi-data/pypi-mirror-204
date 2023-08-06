import json

import requests
from loguru import logger

from . import bottle, utils


def response_json(data, **kwargs):
    # 解决字符编码问题: ensure_ascii=False
    return json.dumps(data, default=str, ensure_ascii=False, sort_keys=True, **kwargs)

def enable_cors(fn):
    # 参考文档:
    # https://stackoverflow.com/a/17262900
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
    def _enable_cors(*args, **kwargs):
        bottle.response.headers['Access-Control-Allow-Headers'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = '*'
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        if bottle.request.method != 'OPTIONS':
            return fn(*args, **kwargs)
    return _enable_cors

def download(request: dict, file: dict, chunks: bool = None, iter_content: dict | None = None, echo: bool = None, info: str = None) -> bool:

    if utils.vTrue(request, dict):
        request_arguments = {'method': 'GET', 'stream': True, **request}
    else:
        return False

    if utils.vTrue(file, dict):
        file_arguments = {'mode': 'wb', **file}
    else:
        return False

    if utils.vTrue(iter_content, dict):
        iter_content_arguments = {'chunk_size': 1024, **iter_content}
    else:
        iter_content_arguments = {'chunk_size': 1024}

    info = f'下载 {info}' if utils.vTrue(info, str) else f'下载'

    try:

        logger.info(f'{info} ......') if echo != False else next

        response = requests.request(**request_arguments)

        with open(**file_arguments) as _file:

            if utils.vTrue(chunks, bool):
                for _chunk in response.iter_content(**iter_content_arguments):
                    _file.write(_chunk)
            else:
                _file.write(response.content)

        logger.success(f'{info} [成功]') if echo != False else next

        return True

    except Exception as e:
        logger.exception(e)
        logger.error(f'{info} [失败]') if echo != False else next
        return False

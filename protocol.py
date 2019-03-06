#created by SamJ
#github:github.com/BDeMo
#2019-3-5- 21:19:40

import json

encoding = 'utf-8'

#Type

StatusCode = b'1001\n'

#Status

ConnectionSuccess = b'0000\n'
FullPullRejection = b'0001\n'
ReactorClosed = b'0002\n'

#function

def preTran(message):
    msg = None
    if isinstance(message, (str, dict)):
        msg = bytes(json.dumps(message), encoding=encoding)
    return msg

def preUse(message):
    msg = None
    if isinstance(message, (bytes)):
        msg = json.loads(str(message, encoding=encoding))
    return msg
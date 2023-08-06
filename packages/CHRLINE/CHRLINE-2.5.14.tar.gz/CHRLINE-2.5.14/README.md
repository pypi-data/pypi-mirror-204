# LINE DemoS Bot - CHRLINE API

>What is CHRLINE?\
>It is LINE Chrome API, just for debug

>If you can help update this project, \
Welcome join our [Discord](https://discord.gg/vQrMbjA)

## About Project
This project is for debug only, because it does not use thrift

So I don't recommend you to use this to run the bot, even if it has many functions

## What can it do?
If you have a certain degree of understanding of Line thrift, then you must have heard of **TMoreCompact** \
But for most people, it is difficult to decompile TMoreCompact, even if it has lower confusion in some version \
But if you can use this project to understand the differences in LINE thrift

## TMoreCompactProtocol
We added the simple function of TMoreCompact for the [first time on 26 May](https://github.com/DeachSword/CHRLINE/commit/3192377714730ddf83208836661182d641d21cb0) \
And added TMoreCompact to [the development version at Jul 8](https://github.com/DeachSword/CHRLINE/commit/d7d8430e74417a06c9ad159a5675b7787ec75c54) \
It's based on the thrift of the LINE Android version \
Its purpose is to effectively compress mid (32 bytes) to 16 bytes



####  Example
```
from CHRLINE import *

cl = CHRLINE() # login

print('/S3 - len: %s' % len(cl.testTBinary()))
print('/S4 - len: %s' % len(cl.testTCompact()))
print('/S5 - len: %s' % len(cl.testTMoreCompact()))
```
####  Result
```
> /S3 - len: 576
> /S4 - len: 528
> /S5 - len: 496
```
This shows that TMoreCompact has the best compression\
If you want to write TMoreCompact, only need to sniff results and reverse engineer

####  Requirement
- Python 3.6
    - pycrypto
    - pycryptodemo
    - xxhash
    - httpx[http2]
    - gevent
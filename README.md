# Interest.blog
Development of a team blog driven by interests and hobbies.

## Environment
> 1. Python Version: 2.6, 2.7
> 2. Web Framework: Flask
> 3. Required Modules:

```
Flask==0.10.1
tornado
gevent
setproctitle
requests
```

## Usage

```

0. Depend:
    0.0 部署Api(https://github.com/staugur/Api)
    0.1 部署Passport(https://github.com/staugur/passport)

1. Requirement:
    1.0 yum install -y gcc gcc-c++ python-devel libffi-devel openssl-devel
    1.1 pip install -r requirements.txt

2. modify config.py or add environment variables(os.getenv key in the reference configuration item):

3. run:
    3.1 python main.py        #开发模式
    3.2 sh Control.sh         #生产模式
    3.3 python -O Product.py  #生产模式，3.2中方式实际调用此脚本
    3.4 python super_debug.py #性能分析模式

```

## Design
![Design][1]

[1]: ./misc/design.png

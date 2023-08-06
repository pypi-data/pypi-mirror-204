# zq-config


----

# Introduction

zq-config is wrapper library for config centers, such as nacos, etcd, apollo.

Here is a program to use `nacos` :

```python
from zq_config import ZQ_Config

SERVER_ADDRESSES = "localhost:8848"
NAMESPACE = "sho-test"
USER_NAME= "nacos"
PASSWORD= "nacos"

zq = ZQ_Config("nacos", server_addresses=SERVER_ADDRESSES, namespace=NAMESPACE, username=USER_NAME, password=PASSWORD)

config = zq.get("config-id", "dev")

print(config)
```

# TODO

- [x] nacos
- [ ] etcd
- [ ] apollo

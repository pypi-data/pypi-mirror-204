# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from zq_config.zq_configs import ZQ_Config

SERVER_ADDRESSES = "localhost:8848"
NAMESPACE = "sho-test"
USER_NAME= "nacos"
PASSWORD= "nacos"

class TestSimple(unittest.TestCase):

    def test_nacos(self):
        zq = ZQ_Config("nacos", server_addresses=SERVER_ADDRESSES, namespace=NAMESPACE, username=USER_NAME, password=PASSWORD)
        self.assertEqual(zq.get_raw("test-config"), "test")


if __name__ == '__main__':
    unittest.main()

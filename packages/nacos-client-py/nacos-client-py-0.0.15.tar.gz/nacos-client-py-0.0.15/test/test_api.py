import json
import logging
import time

import makepath

import config
from nacos import NacosClient

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s [%(pathname)s:%(lineno)d] %(message)s')
logger = logging.getLogger(__name__)

namespace_id = '26b052f1-f8c9-4f31-8900-affd3c4c9e1c'
service_name = ''
group_name = 'public'
ip = '127.0.0.1'
port = 5000

nc = NacosClient(**config.NACOS_CONFIG)

while True:
    print(nc.get_random_instance('monitor'))
    time.sleep(2)

# print(nc.service.get_by_namespace(namespace_id, with_instances=True).content)
# print(nc.service.get('hsdp-schedule', namespace_id=namespace_id, group_name=group_name))

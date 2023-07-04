from RestApi.ontomodeler_lib import *
from service_utility import *
from config_server import *
target_login='admin'
target_passw='ykgI2Krwt1Uz'
target_url='http://ontogovorun.ru/'
target_host=HostInfo(target_url,target_login, target_passw)
target_agent=JsonData(target_host)
target_mng=ModelManager(target_agent)
copy_agent=ModelCopyAgent(target_mng,target_mng)
import re

data = ['172.20.1.37', '60.205.83.248', '8.131.119.148', '39.105.11.225', '39.96.102.119', '172.20.1.38', '60.205.12.32', '39.105.240.30', '39.106.253.234', '60.205.82.126', '182.92.100.172', '101.201.178.233', '59.110.40.111', '39.107.141.164', '47.94.163.89', '8.140.60.140', '39.107.209.69', '47.94.79.57', '123.56.255.102', '8.136.152.62', '60.205.14.128', '47.95.128.67', '47.94.79.204', '47.94.220.64', '39.96.102.128', '101.201.176.28', '60.205.14.24', '60.205.85.245', '39.97.6.97', '123.57.236.50', '47.52.21.232', '172.20.1.39', '8.131.117.109', '182.92.140.26', '123.57.54.198', '39.105.16.197', '39.105.109.132', '39.105.241.141', '60.205.123.158', '47.91.94.72', '60.205.109.148', '39.105.11.57', '8.131.118.19', '182.92.212.238', '47.114.125.233', '8.140.12.212', '8.131.107.109', '182.92.222.218', '59.110.126.184', '39.107.217.79', '47.95.128.8', '39.105.241.209', '39.107.207.235', '172.16.190.89', '47.95.130.239', '59.110.92.153', '120.55.90.62', '59.110.244.181', '101.200.236.37', '8.209.108.211']

def rex_ip(data: list):
    """
    内网ip过滤
    :param data:
    :return:
    """
    rex = re.compile('^(127\\.0\\.0\\.1)|(localhost)|(10\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})|(172\\.((1[6-9])|(2\\d)|(3[01]))\\.\\d{1,3}\\.\\d{1,3})|(192\\.168\\.\\d{1,3}\\.\\d{1,3})$')
    internal_network_ip = [rex.search(i).group() for i in data if rex.search(i)]
    external_network_ip = [i for i in data if not rex.search(i)]
    print(internal_network_ip)
    print(external_network_ip)
    return internal_network_ip, external_network_ip

rex_ip(data)
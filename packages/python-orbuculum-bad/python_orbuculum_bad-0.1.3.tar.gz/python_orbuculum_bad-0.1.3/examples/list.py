from orbuculum_bad import OrbuculumEtherClient
import json

client = OrbuculumEtherClient("localhost:15051")

print("获取第一块网卡: " + client.get_first_port())
print("获取最后一块网卡: " + client.get_last_port())
print("获取第一块电口: " + client.get_first_no_fibre_port())
print("获取最后一块电口: " + client.get_last_no_fibre_port())
print("获取第一块光口: " + client.get_first_fibre_port())
print("获取最后一块光口: " + client.get_last_fibre_port())
print("当前主机IP地址: " + ", ".join(client.get_all_ip_addresses()))
print("获取网卡映射关系: " + json.dumps(client.get_interface_mapping()))
print("获取连接映射关系: " + json.dumps(client.get_connection_mapping()))

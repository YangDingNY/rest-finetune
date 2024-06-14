from scapy.all import rdpcap
from scapy.layers.http import *

pcapFilePath = 'E:\\y1\\api test\\code\\mycode\\finetune-data-collect\\data\\requests-evomaster-warehouse.pcap'

# read pcap file
print("reading pcap file...")
packets = rdpcap(pcapFilePath)
print(len(packets))
print("read pcap file successfully")

# check packet one by one
idx = 0
last_idx = len(packets) - 1
while idx <= 5:
	packet = packets[idx]
	print(idx)
	print(packet.show())
	if 'HTTPRequest' in packet:
		print('this is a http request')
		headers = packet['HTTPRequest'].fields
		print(headers)
		print(type(headers))
	if 'HTTPResponse' in packet:
		print('this is a http response')
	idx += 1
from netpack.func import NetPack

ips = '198.199.108.201'
results = NetPack.ping(ips, 64, "tcp", 0.1, 1, 10)
print(results)

import ipaddress
import os

def main():
    path_list = []
    for a,b,c in os.walk('info'):
        for i in c:
            path = a + '/' + i
            path_list.append(path)

    ip_set = set()
    for i in path_list:
        for j in open(i).readlines():
            info = j[:-1]
            ip = info.split('/')[0]
            mask = info.split('/')[1]
            print j[:-1]
            _ = [ip_set.add(i) for i in get_ip_list(ip, mask)]

    print len(ip_set)


def get_ip_list(ip, mask):
    return ipaddress.IPv4Network(u'%s/%s'%(ip,mask), strict=False).hosts()

def test():
    ip = '1.51.0.0'
    mask = '16'
    ip_list = ipaddress.IPv4Network(u'%s/%s'%(ip,mask), strict=False).hosts()
    for i in ip_list:
        print i


if __name__ == '__main__':
    main()

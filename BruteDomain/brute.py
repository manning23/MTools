#!/usr/bin/python
# -*-coding:utf-8-*-
import os
import time
import dns.resolver
import Queue
import random
import threading
import optparse

'''
You must install dnspython, so you can do this order in linux "pip install dnspython"
'''





domains_queue = Queue.Queue()
info_queue = Queue.Queue()
next_prefix_list = sorted(list(set([i.replace('\r','').replace('\n','') for i in open("next_sub.txt")])))

def generate_domain(start_domain = ""):
    '''
    Creat start urls
    '''
    prefix_list = sorted(list(set([i.replace('\r','').replace('\n','') for i in open("subnames_largest.txt")])))

    domain_list = []
    random.shuffle(prefix_list)

    for i in prefix_list:
        domain = i + '.' + start_domain
        domain_list.append(domain)

    domain_list = domain_list[::-1]
    return domain_list

def server(start_domain, thread_num):
    global domains_queue

    for i in generate_domain(start_domain):
        domains_queue.put(i)

    print 'BruteDomain start !!!'
    print '--------------------------------'

    threads = []
    for i in xrange(thread_num):
        thread = threading.Thread(target = brute_worker)
        threads.append(thread)

    thread = threading.Thread(target = print_worker)
    threads.append(thread)

    for i in threads:
        i.setDaemon(True)
        i.start()

    time.sleep(60)
    while domains_queue.qsize() > 0:
        time.sleep(60)
    print 'BruteDomain finish !!!'
    print '--------------------------------'

def brute_worker():
    '''
    You can change dns server in [res.nameservers]
    '''
    global domains_queue
    global info_queue

    res = dns.resolver.Resolver()
    res.nameservers = ['119.29.29.29','180.76.76.76','182.254.116.116','114.114.114.114','114.114.115.115']

    while True:
        if domains_queue.qsize() > 0:
            domain = domains_queue.get()
            ip_list = []
            try:
                for i in res.query(domain).response.answer:
                    for item in i.items:
                        item = str(item)
                        if not item.endswith('.'):
                            ip_list.append(item)
                    ip_list = sorted(ip_list)
            except Exception as e:
                pass
            if ip_list == [] or len(ip_list) >= 3:
                continue

            for i in next_prefix_list:
                new_domain = i + '.' + domain
                domains_queue.put(new_domain)

            ip_str = ', '.join(ip_list)
            info = (domain,ip_str)
            info_queue.put(info)
        else:
            time.sleep(1)

def print_worker():
    global info_queue
    info_dict = {}
    while True:
        if info_queue.qsize() > 0:
            info = info_queue.get()
            domain,ip_str = info

            if ip_str in info_dict:
                info_dict[ip_str].add(domain)
            else:
                info_dict[ip_str] = set()
                info_dict[ip_str].add(domain)

            if len(info_dict[ip_str]) < 2:
                print ip_str, ' ', ','.join(sorted(list(info_dict[ip_str])))

        else:
            time.sleep(1)

def set_args():
    usage = '''

  __  __ _______          _         ____             _       _____                        _
 |  \/  |__   __|        | |       |  _ \           | |     |  __ \                      (_)
 | \  / |  | | ___   ___ | |___    | |_) |_ __ _   _| |_ ___| |  | | ___  _ __ ___   __ _ _ _ __
 | |\/| |  | |/ _ \ / _ \| / __|   |  _ <| '__| | | | __/ _ \ |  | |/ _ \| '_ ` _ \ / _` | | '_ \\
 | |  | |  | | (_) | (_) | \__ \   | |_) | |  | |_| | ||  __/ |__| | (_) | | | | | | (_| | | | | |
 |_|  |_|  |_|\___/ \___/|_|___/   |____/|_|   \__,_|\__\___|_____/ \___/|_| |_| |_|\__,_|_|_| |_|

                                                                                    By Manning23
    '''
    parser = optparse.OptionParser(usage='')
    parser.add_option('-u',
                    dest = 'url',
                    help = 'Start domain',
                    default = 'suning.com'
                        )
    parser.add_option("-t",
                    dest = "thread_num",
                    help = 'Count for threads',
                    default = 10
                        )
    print usage
    (options, args) = parser.parse_args()
    start_domain  = options.url
    thread_num = options.thread_num
    return (start_domain, thread_num)

if __name__ == '__main__':
    try:
        start_domain, thread_num = set_args()
        server(start_domain, thread_num)
    except KeyboardInterrupt:
        print "User Press Ctrl+C,Exit"
    except EOFError:
        print "User Press Ctrl+D,Exit"

    # single_test()

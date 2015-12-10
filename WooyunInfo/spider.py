import requests
import lxml.html
import Queue
import urllib2

URL_QUEUE = Queue.Queue()

def fetcher(url):
    myheaders = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0"}
    html = ''
    try:
        response = requests.get(url, timeout=15, headers=myheaders)
        if response.status_code == 200:
            html = response.content
    except Exception as e:
        pass
    return html

def save_page(html, url):
    name = url.split('bugs/')
    if len(name) != 2:
        return 0

    name  = name[1]

    if 'wooyun-' not in name:
        return 0

    info = 'vuls/' + name
    t = open(info, 'w')
    t.write(html)
    t.close()


def crawler(html, url):
    try:
        tmp = lxml.html.document_fromstring(urllib2.unquote(html))
        tmp.make_links_absolute(url)
        links = tmp.iterlinks()
        links = [i[2] for i in links]
        return links

    except Exception as e:
        return []

def spider():
    global URL_QUEUE

    url = 'http://www.wooyun.org'
    URL_QUEUE.put(url)

    url_set = set()

    while URL_QUEUE.qsize() > 0:
        url = URL_QUEUE.get()
        html = fetcher(url)

        if len(html) == 0:
            continue

        save_page(html, url)

        for i in crawler(html, url):
            i = i.replace('#comment', '')
            if 'http://www.wooyun.org' not in i:
                continue
            if '/bugs' not in i:
                continue
            if '/new_' in i:
                continue
            if 'type=button' in i:
                continue
            if '/claim' in i:
                continue

            if i not in url_set:
                print i
                url_set.add(i)
                URL_QUEUE.put(i)
        pass

if __name__ == '__main__':
    try:
        spider()
    except KeyboardInterrupt:
        print "User Press Ctrl+C,Exit"
    except EOFError:
        print "User Press Ctrl+D,Exit"

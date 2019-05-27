import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code == 200:
            results=get_one_page_content(response.text)
            return results
    except RequestException:
        return None


def save_file(result):
    with open('top100.txt','a',encoding='utf-8') as f:#将字符串存入文件中
        f.write(json.dumps(result,ensure_ascii=False)+'\n',)#将unicode存成正常的中文
        f.close()

def get_one_page_content(text):
    pattern=re.compile('<dd.*?board-index.*?>(\d+)</i>.*?<a.*?title="(.*?)".*?'
                       +'data-src="(.*?)".*?class="star">(.*?)<.*?class="releasetime">(.*?)<.*?'
                       +'class="integer">(.*?)</i>.*?class="fraction">(\d+)</i>.*?</dd>',re.S)
    results=re.findall(pattern,text)
    print(results)
    for result in results:
        yield {
            'index':result[0],
            'title':result[1],
            'img':result[2],
            'star':re.sub('\s','',result[3])[3:],
            'time':result[4][5:],
            'integer':result[5],
            'fraction':result[6]
        }

def main(offset):
    url="https://maoyan.com/board/4?offset=%s"%offset
    results=get_one_page(url)
    for result in results:
        save_file(result)

if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])
    pool.close()#关闭pool，不接受新的（主进程）任务
    pool.join() #主进程阻塞后，让子进程继续运行完成，子进程运行完后，再把主进程全部关掉。
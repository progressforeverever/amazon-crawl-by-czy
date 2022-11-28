import aiohttp
import time
from lxml import etree
import asyncio



cnt = 0     #计数器
url='https://www.amazon.com/The-Dark-Forest-audiobook/product-reviews/B010R28SZ4/ref=cm_cr_dp_d_show_all_btm?pageNumber='
url_list=[]
for i in range(1,101):
    url_in_list=url+str(i)
    url_list.append(url_in_list)

async def start_request(url):
    async with aiohttp.ClientSession() as sess:     #实例化一个请求对象
        async with await sess.get(url=url) as response:
            page_text = await response.text()
            return page_text

def parse_comment(task):
    #获取请求到页面源码数据
    page_text = task.result()
    tree=etree.HTML(page_text)
    result=tree.xpath("//div[@class='a-row a-spacing-small review-data']//text()")

    global cnt
    with open("./TheDarkForest.txt",mode='a',encoding='utf-8') as f:
        for i in range(0,len(result)-1):
            #find里面的内容是评论开始的标志，定位作用
            if(result[i].find('\n\n\n\n\n\n\n\n  \n  \n    ')!=-1):
                f.write('\n')
                cnt=cnt+1
                line="第"+str(cnt)+"条评论: "
                f.write(line)
            if(result[i].find('\n')!=-1):
                continue    #判断是否是多余的换行，该判断后文件就不会写入多余的换行
            else:                        
                f.write(result[i])  #写入评论
                
        f.close()   #保存文件



if __name__=="__main__":
    start = time.time()
    tasks_list = [] # 多任务列表
    # 1.创建协程对象
    for url in url_list:
        c = start_request(url)
        # 2.创建任务对象
        task = asyncio.ensure_future(c)
        task.add_done_callback(parse_comment)
        tasks_list.append(task)
    # 3.创建事件循环对象
    loop = asyncio.get_event_loop()
    # 4.将任务对象注册到事件循环中且开启事件循环
    loop.run_until_complete(asyncio.wait(tasks_list))# 必须使用wait方法对tasks_list封装
    print("总耗时:",time.time()-start)
import requests
from lxml import etree
import time


def is_dict_all_True(dict_params:dict)->bool:
    for i in range(1,len(dict_params)):
        if dict_params[str(i)]==False:
            return False


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'}  
url='https://www.amazon.com/Deaths-End-audiobook/product-reviews/B01LW7NVP0/ref=cm_cr_arp_d_paging_btm_2?'

dict_is_crawl={}
for i in range(1,101):
    str_i=str(i)
    dict_is_crawl[str_i]=False


'''
range_list=range(1,101)
page_list=list(range_list)
'''

cnt=0
while not is_dict_all_True(dict_is_crawl):
    for page_num in range(1,101):
        if dict_is_crawl[str(page_num)]==True:
            continue
        else:
            data={'ie':'UTF8','reviewerType':'all_reviews','pageNumber':page_num}
            response=requests.get(url=url,headers=headers,params=data)
            page_text=response.text
            print(page_text)
            print()
            tree=etree.HTML(page_text)
            result=tree.xpath("//div[@class='a-row a-spacing-small review-data']//text()")
            print(result)
            print(len(result))


            with open("./Deaths_end.txt",mode='a',encoding='utf-8') as f:
                for i in range(0,len(result)-1):
                    if(result[i].find('\n\n\n\n\n\n\n\n  \n  \n    ')!=-1):
                        f.write('\n')
                        cnt=cnt+1
                        line="第"+str(cnt)+"条评论: "
                        f.write(line)
                        dict_is_crawl[str(page_num)]=True
                    if(result[i].find('\n')!=-1):
                        continue
                    else:
                        f.write(result[i])
            f.close()   #保存文件
            print(page_num)
            print(cnt)

print("结束")



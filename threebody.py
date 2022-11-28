import requests
from lxml import etree
import time



#用于判断字典的value值是否全是True 若有一个的value值是False,即没有被爬取，返回False
def is_dict_all_True(dict_params:dict)->bool:
    for i in range(1,len(dict_params)):
        if dict_params[str(i)]==False:
            return False


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'}  
#除去请求头的url
url='https://www.amazon.com/The-Three-Body-Problem-audiobook/product-reviews/B00P00QPPY/ref=cm_cr_getr_d_paging_btm_next_3?'

#构造页面是否被爬取的字典，key值是页面值（1,2...100）(字符串形式，方便传参)，
# value值全部初始化为False,若页面被爬取到，则把相应地value值置为true
dict_is_crawl={}
for i in range(1,101):
    str_i=str(i)
    dict_is_crawl[str_i]=False


cnt=0   #记录爬取的评论数量

#当还有页面没有被爬取的时候
while not is_dict_all_True(dict_is_crawl):
    #爬取1-100页的评论，要和那字典dict_is_crawl对应的上
    for page_num in range(1,101):
        if dict_is_crawl[str(page_num)]==True:
            #如果已经被爬取到了，跳出当前循环
            continue
        else:
            #请求所携带的参数，封装成字典，page_num是评论的第几页
            data={'ie':'UTF8','reviewerType':'all_reviews','pageNumber':page_num}
            #发送请求，params=data传递请求所携带的参数，这样可以避免直接写url带来的url长度过长和复用性不高的问题
            response=requests.get(url=url,headers=headers,params=data)
            page_text=response.text

            print(page_text)
            print()
            #以上print只是用来测试，看看反馈

            #实例化tree对象
            tree=etree.HTML(page_text)
            #xpath定位 所有的评论都位于 class(类)为 'a-row a-spacing-small review-data' 的div标签下  这个是观察页面得到的
            result=tree.xpath("//div[@class='a-row a-spacing-small review-data']//text()")
            print(result)
            print(len(result))

            #数据解析及写入文件  上面的result返回的是列表
            # mode='a'以追加的方式写入
            with open("./ThreeBody.txt",mode='a',encoding='utf-8') as f:
                for i in range(0,len(result)-1):
                    #find里面的内容是评论开始的标志，定位作用
                    if(result[i].find('\n\n\n\n\n\n\n\n  \n  \n    ')!=-1):
                        f.write('\n')
                        cnt=cnt+1
                        line="第"+str(cnt)+"条评论: "
                        f.write(line)
                        dict_is_crawl[str(page_num)]=True   #将页面是否爬取到的标志置为True,下次循环时就会跳过
                    if(result[i].find('\n')!=-1):
                        continue    #判断是否是多余的换行，该判断后文件就不会写入多余的换行
                    else:                        
                        f.write(result[i])  #写入评论
            f.close()   #保存文件
            print(page_num)
            print(cnt)
print("结束")



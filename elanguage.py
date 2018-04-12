import requests
from lxml import etree
import traceback,os,socke

#获取链接函数
def getpage(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        traceback.print_exc()


def parseHtml():
    #设置超时时间为5s
    socket.setdefaulttimeout(5)
    source_url = 'http://www.5a5x.com/wode_source/'
    r = getpage(source_url)
    page_source = etree.HTML(r)
    typeList = page_source.xpath('//*[@id="main_l"]/div/div/a/@href')

    #获取各种类型连接，并创建对应文件夹
    for type in typeList:
        type = type.split('/')[-2]
        typeurl = source_url + '/' + type + '/'
        if  not os.path.exists('F:\python_workplace\Elanguage\\'+type):
            os.mkdir('F:\python_workplace\Elanguage\\'+type)
        type_page = getpage(typeurl)
        type_html =etree.HTML(type_page)
        pageTotal = type_html.xpath('//*[@id="pages"]/b[2]/text()')[0].replace('/','')
    #获取各个类型的源码列表页
        for i in range(1,int(pageTotal)+1):
            page_url = typeurl+str(i)+'.html'
            page_text=getpage(page_url)
            page_html = etree.HTML(page_text)
            alist = page_html.xpath('//*[@id="main_l"]/dl/dt/a/@href')
            #获取源码链接
            for hrefs in alist:
                download_url=''
                try:
                    code_url = 'http://www.5a5x.com/' + hrefs
                    codepage = getpage(code_url)
                    codehtml = etree.HTML(codepage)
                    code_title = codehtml.xpath('//*[@id="content"]/table/caption/span/text()')[0]
                    download_url = 'http://www.5a5x.com/' + codehtml.xpath('//*[@id="down_address"]/a/@href')[0]
                    downpage = getpage(download_url)
                    downhtml = etree.HTML(downpage)
                    file_url = 'http://www.5a5x.com/' + downhtml.xpath('//a/@href')[0]
                    r= requests.get(file_url)
                    r.encoding=r.apparent_encoding
                    #将下载文件存储到指定类型的文件夹，并以zip形式存储
                    with open('F:\\python_workplace\\Elanguage\\'+ type +'\\'+ code_title + ".zip", 'wb') as f:
                        f.write(r.content)
                    print(type+ ','+ code_title)
                except Exception as e:
                    print(download_url)

if __name__ == '__main__':
    parseHtml()

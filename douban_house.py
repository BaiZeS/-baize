import requests
from lxml import etree
import user_agent

import xlwt
import time

link = 'https://www.douban.com/group/CQrent/'
delay = 1


# 生成链接
def creat_links():
    links = []
    link = 'https://www.douban.com/group/CQrent/discussion?start='
    for i in range(0, 500, 25):
        links.append(link+str(i))
    # print(links)
    return links


# 将数据写入新xls文件
def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    #将数据写入第 i 行，第 j 列
    i = 0
    for row_data in datas:
        j = 0
        for cloumn_data in row_data:
            sheet1.write(i, j, cloumn_data)
            j = j + 1
        i = i + 1
    f.save(file_path)  # 保存文件


# 获取每页评论标题、时间、二级链接
def get_titles(link):
    header = user_agent.get_user_agent_pc()
    re = requests.get(link, headers={'User-Agent': header})
    html = etree.HTML(re.text)
    titles = html.xpath('//div[@id="content"]//table[@class="olt"]//td[@class="title"]/a/@title')
    rent_times=html.xpath('//div[@id="content"]//table[@class="olt"]//td[@class="time"]/text()')
    next_links = html.xpath('//div[@id="content"]//table[@class="olt"]//td[@class="title"]/a/@href')
    # time.sleep(delay)
    return titles, rent_times, next_links


if __name__ == '__main__':
    links = creat_links()
    titles = []
    rent_times = []
    next_links = []
    # 合并数据
    for link in links:
        title, rent_time, next_link = get_titles(link)
        for data in title:
            titles.append(data)
        for data in rent_time:
            rent_times.append(data)
        for data in next_link:
            next_links.append(data)
    save_data = list(zip(titles, rent_times, next_links))
    # 写入xls文件保存
    data_write(r'../scrapy/data/house_data.xls', save_data)

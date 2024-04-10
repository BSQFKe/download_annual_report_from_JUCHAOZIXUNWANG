"""
配套Symbol.txt 完成爬取任务
"""
from helper import createFilter,isNeed,isLast
from helper import changeUrlDicToTxt
from helper import stopWords
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from totalSet import totalFilter,allSymbols,recordedCode,toDownloadUrlTxt
from totalSet import abnormalFilter,allExceptionTxt,noCompanyName,jjjl,notTarget
from totalSet import checkFlag
import os

abnormalFilter = createFilter(abnormalFilter) # 异常下载url 的 文件总路径
totalFilter = createFilter(totalFilter)  # 下载的pdf 的 文件夹总路径

# 设置目标任务的symbolLis列表
totalSymbolLis = [] # 全部的公司编码号
with open(allSymbols) as f:
    for line in f.readlines():
        totalSymbolLis.append(line.strip())
recordLis = [] # 已经记录过url的证券编号
if os.path.exists(recordedCode):
    with open(recordedCode,'r',encoding='utf-8') as f:
        for line in f.readlines():
            recordLis.append(line.strip())
symbolLis = list(set(totalSymbolLis)-set(recordLis))
symbolLis.sort()

def getShowPageUrl(browser:webdriver,code:str):
    # 获取展示界面url 与 其 题目
    path = f"http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord={code}%20年度报告"
    # 下为测试用path
    # path = "http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=000002%202019%E5%B9%B4%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A"
    browser.get(path)
    totalUrlLis = []
    totalTitleLis = []
    while True:
        time.sleep(2)
        eleTitle = browser.find_elements(By.XPATH,"//span[@class='sub-content-flow' or @class='tileSecName-content']") # 标题元素
        if len(eleTitle)==0:
            break
        eleLink = browser.find_elements(By.XPATH,"//div[@class='cell']//a[@target='_blank']")[-1*len(eleTitle):] # 可访问链接的元素
        flag = [isNeed(item.text) for item in eleTitle]
        targetTitleLis= [eleTitle[i].text for i in range(len(eleTitle)) if flag[i]]
        targetLinkLis = [eleLink[i] for i in range(len(eleLink)) if flag[i] ] # 符合条件的链接元素
        targetUrlLis = [target.get_attribute("href") for target in targetLinkLis] # 待点击的url列表
        
        totalUrlLis+=targetUrlLis # url列表
        totalTitleLis+=targetTitleLis # 名字列表
        # 如果是最后一页 退出
        if isLast(browser):
            break
        # break # 测试用
        btn = browser.find_element(By.XPATH,"//button[@class='btn-next']")
        btn.click() # 换页
    urlShowDic = dict(zip(totalUrlLis,totalTitleLis))
    return urlShowDic # 返回一个字典  url对应标题名

def getDownLoadUrl(browser:webdriver,code:str,urlShowDic:dict):
    """传入公司号,urlShow字典 (展示页的url字典)
    获取下载的链接
    返回 一个字典 下载url 对应 code_title  
    """
    downLoadUrlDic = {}
    for key,value in urlShowDic.items():
        browser.get(key) # 访问目标页
        time.sleep(1)
        # 07年之前的都不要了
        year = browser.find_element(By.XPATH,"//div[@class='month ' or @class='sub-month']").text[:4]
        if int(year)<2007:
            break
        
        # 找公司号 没找到就算了
        try:
            check = browser.find_element(By.XPATH,"//div[@class='stock']//span[@class='code f16']//a")
            name = browser.find_element(By.XPATH,"//div[@class='stock']//span[@class='name f16']//a").text
            for stop in stopWords:
                if stop in name:
                    continue # 再次筛掉一批
        except NoSuchElementException:
            # 记找公司名异常页面
            path = os.path.join(abnormalFilter,noCompanyName)
            mode = 'a' if os.path.exists(path) else 'w'
            with open(path,mode,encoding='utf-8') as f:
                f.write(key+'\n')
            continue
        # 大部分满足jjjl的开放股 但还有一些看不懂的开放股特例 我真的已经尽力了
        if 'jjjl' in check.get_attribute("href"):
            path = os.path.join(abnormalFilter,jjjl)
            mode = 'a' if os.path.exists(path) else 'w'
            with open(path,mode,encoding='utf-8') as f:
                f.write(key+'\n')
            continue
        # 判断是不是目标公司的文件 不是的话退出
        if code not in check.get_attribute("href"):
            path = os.path.join(abnormalFilter,notTarget)
            mode = 'a' if os.path.exists(path) else 'w'
            with open(path,mode,encoding='utf-8') as f:
                f.write(key+'\n')
            continue

        # 找下载链接
        a = browser.find_element(By.XPATH,"//div[@class='fullscreen']//a")
        downloadUrl = a.get_attribute("href")
        downLoadUrlDic[downloadUrl] = f"{code}_{name}_{value}.pdf".replace(' ','') # 去除文件中的空格
    return downLoadUrlDic # 链接 与 文件名


def recordToDownloadUrl():
    # 记录待下载的url
    browser = webdriver.Chrome() # 浏览器对象
    browser.implicitly_wait(1) # 设置超时
    
    for code in symbolLis:
        try:
            urlShowDic = getShowPageUrl(browser,code)
            downloadDic = getDownLoadUrl(browser,code,urlShowDic)
            # batchDownload(downloadDic) # 先不下载 光记录url
            changeUrlDicToTxt(downloadDic,toDownloadUrlTxt)
            mode = 'a' if os.path.exists(recordedCode) else 'w'
            with open(recordedCode,mode,encoding='utf-8') as f:
                f.write(code+'\n')
        except: # 但凡报错直接下一个
            # 推荐主体爬完后使用 如果需要进行异常筛查 将set中checkFlag设置为True 会将异常部分进行记录
            if checkFlag:
                mode = 'a' if os.path.exists(allExceptionTxt) else 'w'
                with open(allExceptionTxt,mode,encoding='utf-8') as f:
                    f.write(code+'\n')

if __name__ == "__main__":
    # recordToDownloadUrl()
    pass
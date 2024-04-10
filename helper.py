"""
配合scraw.py 使用
"""
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from totalSet import stopWords

# 辅助用函数0 检查文件夹的函数 如果没有则创建
def createFilter(filterPath:str):
    """检查文件夹是否被创建 如果没有 创建"""
    if not os.path.exists(filterPath):
        os.makedirs(filterPath)
    return filterPath

# 辅助用函数1  引入停词表 判断是否为所需要的内容
def isNeed(text:str):
    """判断是否为我们需要的元素"""
    for stop in stopWords:
        if stop in text:
            return False        
    if re.findall(r"\d{4}年年度报告", text): # 有XXXX年年度报告 这四个字直接过
        return True
    if text.endswith("年报"): # 有年报这俩字 过
        return True
    # 默认为真
    return True

# 辅助用函数2 判断是否为最后一页
def isLast(browser:webdriver):
    """判断是不是最后一页"""
    flag = True # 默认是
    try:
        next = browser.find_element(By.XPATH,"//button[@class='btn-next' and @disabled='disabled']")
    except:
        # 没找到不可点击的下一页
        flag=False # 所以不是最后一页
        next = browser.find_element(By.XPATH,"//button[@class='btn-next']")
    return flag

def changeUrlDicToTxt(dic,txtPath):
    """
    将dic的键值对 写成空格链接并换行的txt文件 保存至txtPath
    """
    mode = 'a'if os.path.exists(txtPath) else 'w'
    with open(txtPath,mode,encoding='utf-8') as f:
        for key,value in dic.items():
            f.write(f'{key} {value}\n')

def readTxt(txtPath:str):
    """将字典txt读入为字典"""
    keyLis = []
    valueLis = []
    if os.path.exists(txtPath):
        with open(txtPath,encoding='utf-8') as f:
            for line in f.readlines():
                key,value = line.strip().split()
                keyLis.append(key)
                valueLis.append(value)
    return dict(zip(keyLis,valueLis))
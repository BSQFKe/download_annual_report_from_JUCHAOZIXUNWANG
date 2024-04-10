from helper import readTxt
import os
from totalSet import totalFilter,toDownloadUrlTxt,finiehedDownloadUrlTxt
def batchDownload(downLoadUrlDic,recordTxt=None):
    """传入一个 下载url的字典 与记录已经完成下载的url的Txt路径
    实现下载
    无返回
    """
    def downloadOne(url,fileName):
        path = os.path.join(totalFilter,fileName) # 总路径
        # 已经下好了的就不下了
        if os.path.exists(path):
            return
        os.system(f"wget {url} -O {path}")

    for key,value in downLoadUrlDic.items():
        downloadOne(key,value)
        mode = 'a' if os.path.exists(recordTxt) else 'w'
        with open(recordTxt,mode,encoding='utf-8') as f:
            f.write(f"{key} {value}\n")

def downloadPdfs():
    print("开始进行下载任务")
    # 读取待下载urltxt 批量下载
    urlDic = readTxt(toDownloadUrlTxt)
    finishedDic = readTxt(finiehedDownloadUrlTxt)
    # 删除已经被下载的url
    toDelKeys = []
    for key in urlDic.keys():
        if key in finishedDic.keys():
            toDelKeys.append(key)
    for toDel in toDelKeys:
        urlDic.pop(toDel,None)
    # 批量下载
    batchDownload(urlDic,finiehedDownloadUrlTxt)
if __name__ =="__main__":
    # downloadPdfs()
    pass
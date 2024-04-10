from scraw import recordToDownloadUrl
from download import downloadPdfs
# 推荐优先执行记录函数 免费网区域执行下载函数
if __name__ =="__main__":
    recordToDownloadUrl() # 记录url
    # downloadPdfs() # 下载pdf
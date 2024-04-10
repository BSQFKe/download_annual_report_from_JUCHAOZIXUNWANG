"""
设置文件
"""
# 状态设置
checkFlag = False# 筛查哪部分出现了异常需要重爬，True为进行筛查
# 总任务设置
allSymbols = "Symbol.txt"# 全部的公司编码号txt路径

# 爬取与下载相关设置
totalFilter = "DownLoad" # 下载的pdf 的 文件夹总路径
recordedCode = "已记录待下载url的证券代码号.txt"
toDownloadUrlTxt = "全部待下载url.txt"
finiehedDownloadUrlTxt = "已完成下载的url.txt"

# 异常相关设置
abnormalFilter = "Abnormal"# 异常下载url 的 文件总路径
noCompanyName = "找公司名异常页面.txt"
jjjl = "jjjl页面.txt"
notTarget = "非目标公司页面.txt"
allExceptionTxt = "代码号-出现各种各样的异常都往这里丢-最后需要从已记录的待下载里剔除掉.txt"

# 停词表
stopWords = "摘要 半年度 英文版 有关 关于 公告 预案 财务 回复 补充 英文 取消 董事 延期 披露 股东 意见 监事会 内幕 审核 说明 记录 审计".split()

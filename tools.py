"""
通用的工具方法
"""
import xlwt
import time

from fake_useragent import UserAgent
from datetime import datetime

# 红色 用于输出报警信息
def error(Str):
    print("\033[0;31;40m" + Str + "\033[0m")

# 获取当前时间 年月日
def getNowTime():
    # return time.strftime('%Y.%m.%d-%Hh%Mm%Ss', time.localtime(time.time()))
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

# 获取随机userAgent
def getRandomUserAgent():
    try:
        return UserAgent().random
    except IndexError:
        pass
    return UserAgent().random

# 将时间戳转换为时间
def timeStampToTime(timeStamp):
    return str(datetime.utcfromtimestamp(timeStamp))

# 获取下载地址
def getDownAddress():
    # TODO 通过配置文件读取下载地址
    return "D:/System_default/下载/bilibili/"

"""
解析后的数据对应>>>
0:comment, 1:typeid, 2:play, 3:pic, 4:subtitle, 
5:description, 6:copyright, 7:title, 8:review, 9:author,
10:mid, 11:created, 12:length, 13:video_review, 14:aid,
15:bvid, 16:hide_click, 17:is_pay, 18:is_union_video, 19:is_steins_gate,
20:is_live_playback
"""
# 获取导出excel的题头
def getTitleList(functionName):
    excelTitle = []
    match functionName:
        case "getUpAll":
            # 获取excel题头
            titleList = ['序号', 'bvid', '标题', '时长', '上传时间', '描述']
            excelTitle.append(titleList)
            # list中对应的数据的key
            listKey = ['', 'bvid', 'title', 'length', 'created', 'description']
            excelTitle.append(listKey)
            # 设置列宽
            titleWidth = [1200, 5000, 12000, 1500, 5000, 50000]
            excelTitle.append(titleWidth)
            return excelTitle
        case functionName:
            error("方法【" + functionName + "】的excel导出异常")

# 获取excel的名字
def getExcelName(dataList, functionName):
    match functionName:
        case "getUpAll":
            return "【" + dataList[0]['author'] + "】所有视频" + getNowTime() + ".xls"
        case functionName:
            error("方法【" + functionName + "】的excel导出异常")

# 获取sheet
def getSheetName(dataList, functionName):
    match functionName:
        case "getUpAll":
            return "【" + dataList[0]['author'] + "】所有视频"
        case functionName:
            error("方法【" + functionName + "】的excel导出异常")

# 获取bat文件名
def getBatName(dataList, functionName):
    match functionName:
        case "getUpAll":
            return "【" + dataList[0]['author'] + "】所有视频"
        case functionName:
            error("方法【" + functionName + "】的excel导出异常")

# 获取BBDown的下载命令
def getDownCommand(dataList, functionName):
    downCommand = "\n"
    match functionName:
        case "getUpAll":
            for i in range(len(dataList)):
                downCommand += "BBDown -tv --work-dir " + getDownAddress() + dataList[0][
                    'author'] + " https://www.bilibili.com/video/" + dataList[i]['bvid'] + "\n"
        case functionName:
            error("方法【" + functionName + "】的bat生成异常")
    return downCommand

# 根据list直接生成excel 无调用,但后续有需要的话可以根据这个改造
def createExcel(dataList, fileName):
    titleList = []
    for keys, value in dataList[0].items():
        # 提取dataList中的键值
        temp = keys
        titleList.append(temp)
    workbook = xlwt.Workbook(encoding="utf-8")  # 实例化book对象
    sheet = workbook.add_sheet("Sheet1")  # 生成sheet
    # 写入标题
    for col, column in enumerate(titleList):
        sheet.write(0, col, column)
    # 写入每一行
    for row, data in enumerate(dataList):
        for col, col_data in enumerate(data):
            sheet.write(row + 1, col, data[col_data])
    workbook.save(fileName + ".xls")

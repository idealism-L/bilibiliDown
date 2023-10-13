"""
主要方法
"""
import requests
import json
import xlwt

import tools

# 获取各页的视频bvid
def getPagesBvId(mid):
    # 初始化变量
    videoDataLists = []
    index = 0
    pages = 0
    # 循环取bvid
    while True:
        # 测试数据：https://api.bilibili.com/x/space/arc/search?mid=691415738&jsonp=jsonp&pn=1
        pageURL = "https://api.bilibili.com/x/space/arc/search?mid=" + mid + "&jsonp=jsonp&pn=" + str(index + 1)
        videoDataList = grab_info(pageURL)
        # 如果是第一页，就去判断是否有数据，顺便获取总共有几页视频和作者信息
        if index == 0:
            if videoDataList == "":
                tools.error("【error】：mid为【" + mid + "】的UP没有视频，请重新选择操作！")
                return False
            elif videoDataList == "null":
                tools.error("【error】：查不到mid为：【" + mid + "】的UP数据，请重新选择操作！")
                return False
            # 计算该UP总共有多少个视频
            pages = int(
                (videoDataList['page']['count'] + videoDataList['page']['ps'] - 1) / videoDataList['page']['ps'])
            author = videoDataList['list']['vlist'][0]['author']
            print("【" + author + "】总共有", pages, "页视频")
        # 如果是最后一页 则去计算最后一页有多少个视频
        if videoDataList['page']['pn'] == pages:
            videoDataList['page']['ps'] = videoDataList['page']['count'] - (videoDataList['page']['pn'] - 1) * 30
        # 获取视频数据，添加到videoDataLists
        for i in range(videoDataList['page']['ps']):
            videoDataLists.append(videoDataList['list']['vlist'][i])
        print("第", index + 1, "页:", pageURL, "完成")
        # 累加页码
        index += 1
        # 当最后一页执行完之后 退出循环
        if index == pages:
            break
    return videoDataLists

# 获取地址的json信息
def grab_info(FullURL):
    # 代理头部
    headers = {
        "User-Agent": tools.getRandomUserAgent()
    }
    # 获取一个返回信息
    response = requests.get(FullURL, headers=headers).content.decode('utf-8')
    # 把json转换为python对象
    content = json.loads(response)
    # 利用json提取主体视频信息
    if content['code'] == 0:
        data = content['data']
        if len(data['list']['vlist']) == 0:
            return ""
    else:
        return "null"
    return data

# 根据list生成excel文件
def createExcel(dateList, functionName):
    workbook = xlwt.Workbook(encoding="utf-8")  # 实例化book对象
    sheet = workbook.add_sheet(tools.getSheetName(dateList, functionName))  # 生成sheet

    # 设置excel的title、数据列表中的key和列宽
    titleList = tools.getTitleList(functionName)[0]
    listKey = tools.getTitleList(functionName)[1]
    titleWidth = tools.getTitleList(functionName)[2]

    # 设置title宽度
    for i in range(len(titleWidth)):
        sheet.col(i).width = titleWidth[i]

    # 写入标题
    for col, column in enumerate(titleList):
        sheet.write(0, col, column)

    # 写入数据
    for row, data in enumerate(dateList):
        for i in range(len(listKey)):
            # 0为序号列 i>0为数据列
            if i == 0:
                sheet.write(row + 1, i, row + 1)
            else:
                if listKey[i] == 'created':
                    # 如果该列为created:上传时间,需要将时间戳转换为时间
                    sheet.write(row + 1, i, tools.timeStampToTime(data[listKey[i]]))
                else:
                    sheet.write(row + 1, i, data[listKey[i]])
    workbook.save(tools.getExcelName(dateList, functionName))

# 创建bat文件
def createBat(dataList, functionName):
    # TODO 通过配置文件读取cd地址
    cdCommand = "CD D:/Project/PyCharm/bilibiliDown/downloader\nD:\n"
    downCommand = tools.getDownCommand(dataList, functionName)

    # 生成bat文件 common.getBatName(dateList, functionName)=>获取bat文件名
    with open(tools.getBatName(dataList, functionName) + ".bat", 'w', encoding='utf-8') as f:
        f.write(cdCommand + downCommand)
    f.close()

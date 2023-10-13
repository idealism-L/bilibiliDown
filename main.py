import sys

import methods
import tools
import os

def main():
    # 展示操作菜单
    menu()
    # 选择需要的操作
    operate()

def menu():
    print("【B站视频爬虫】\n"
          "【1】下载UP所有视频\n"
          "【0】退出本程序"
          )

def operate():
    while True:
        code = input("【根据序号选择操作】：")
        match code:
            case "0":
                # 退出本程序
                getSystemOut()
            case "1":
                # 下载UP所有视频 测试id：691415738, 13153406, 9554603
                getUpAll()
            case code:
                tools.error("【error】：操作【" + code + "】不是有效的操作，请重新选择！")
        menu()

"""【0】.退出本程序"""
def getSystemOut():
    sys.exit(0)

"""【1】.下载UP所有视频"""
def getUpAll():
    print("\n操作【1】.下载UP所有视频")
    mid = input("请输入Up主id:")
    # 根据mid获取所有分页的bvid
    videoDataLists = methods.getPagesBvId(mid)
    if videoDataLists:
        # 选择是否需要生成excel
        code = input(videoDataLists[0]['author'] + "共有" + str(len(videoDataLists)) + "个视频，是否生成excel文件?Y/N\n")
        if code == 'y' or code == 'Y':
            # 通过数据列表和方法名生成excel
            methods.createExcel(videoDataLists, sys._getframe().f_code.co_name)
        methods.createBat(videoDataLists, sys._getframe().f_code.co_name)
        print("文件生成完成.\n")
    batRunCode = input("是否直接执行下载命令？Y/N\n")
    if batRunCode == 'y' or batRunCode == 'Y':
        os.system("D:\\Project\\PyCharm\\bilibiliDown\\" + tools.getBatName(videoDataLists, sys._getframe().f_code.co_name))

if __name__ == '__main__':
    main()

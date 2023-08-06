# encoding=utf8
import csv
from genericpath import exists
import json
import os
import sys


def write_csv_file(path, head, data):
    '''
    用途：把list数据写入csv文件中
    path 文件地址
    head 标题行内容，格式list
    data 正式内容，格式list
    '''
    try:
        with open(path, 'w', newline='', encoding='utf8') as csv_file:
            writer = csv.writer(csv_file, dialect='excel')
            if head is not None:
                writer.writerow(head)
            for row in data:
                writer.writerow(row)
            print("Write a CSV file to path %s Successful." % path)
    except Exception as e:
        print("Write an CSV file to path: %s, Case: %s" % (path, e))


def toFile(xuid, pid, data, fileName):
    '''
    用途：把数据整理成list，写入csv文件中
    xuid 需求id 
    pid p账号
    '''
    datas = []
    csvList = ['用例目录', '用例名称', '需求ID', '前置条件', '用例步骤', '预期结果', '用例类型', '用例状态',
               '用例等级', '创建人', '是否实现自动化', '是否上架', '自动化测试类型', '自动化测试平台', '移动系统', '是否自动化', '标签']
    for k, v in data.items():
        tmpList = []
        tmpDict = {'用例名称': str(k)[1:], '需求ID': str(
            xuid), '用例步骤': k[1:], '预期结果': v, '用例类型': '功能测试', '用例状态': '正常', '用例等级': '中', '创建人': str(pid)}
        for vdata in csvList:
            if vdata in tmpDict:
                tmpList.append(tmpDict.get(vdata))
            else:
                tmpList.append("")
        datas.append(tmpList.copy())

    write_csv_file(fileName, csvList, datas)


def getDataFromKM(root, data, nowList):
    '''
    用途：使用嵌套循环获取km文件内容并生产list数据
    root 文件目录
    data 获取单层内容
    nowList 当前已获取的数据
    '''
    tmpData = str(data['data']['text']).strip()  # 临时数据报保存当前值
    if len(data['children']) > 0:  # 判断是否含有子目录
        for childrenData in data['children']:
            getDataFromKM(root+','+tmpData, childrenData, nowList)
    else:
        nowList.append({root: tmpData})
    return nowList


def getFile(path):
    '''
    用途：获取文件并转成dict格式
    path 文件路径
    '''
    if not os.path.exists(path):
        print("文件不存在："+str(path))
        sys.exit(1)
    data = {}  # 存数据用
    with open(path, encoding='utf8') as f:
        data = f.read()
    return json.loads(data, encoding='utf8')


def run(filepath, xuid, pid):
    '''
    用途：执行脚本
    filepath km文件的绝对路径
    xuid 需求id 
    pid p账号
    '''
    fileLine = getDataFromKM('', getFile(filepath)['root'], [])
    caseDict = {}
    for line in fileLine:
        for k, v in line.items():
            if caseDict.get(k) is None:
                caseDict[k]=v
            else:
                caseDict[k]+="\n"+v
    toFile(str(xuid), pid, caseDict, filepath.replace('.km', '.csv'))

# if __name__ == "__main__":
def main():
    f=""
    if (len(sys.argv)==1):
        f=input("请填写文件地址：")
        sys.argv.append(f)
    x=""
    if  (len(sys.argv)==2):
        x=input("请填写需求id：")
        sys.argv.append(x)
    p=""
    if  (len(sys.argv)==3):
        pv=""
        
        if os.environ.get('HOME') is not None:
            pv=os.path.join(os.environ.get('HOME'),".km")
        elif os.environ.get('HOMEPATH') is not None:
            pv=os.path.join(os.environ.get('HOMEPATH'),".km")
        if len(pv)>0:
            if os.path.exists(pv):
                for i in os.listdir(pv):
                    if i.startswith('pzhanghaofile.'):
                        p=i[14:]
                        break
            else:
                p=input("请填写p账号：")
                try:
                    os.makedirs(pv)
                    with open(os.path.join(pv,'pzhanghaofile.'+p),"w") as f1:
                        f1.write("\n")
                except:
                    pass
    else:
        print("输入的参数过多~",sys.argv)
    print(f,x,p)

        

    


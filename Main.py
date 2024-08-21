import time
import json
import os





def unique(id,idList):
    '''
    :function: 保证书籍登录号唯一
    :param id: 传入的登录号
    :param idList：现有登录号库
    :return: 是否唯一
    '''
    if id in idList:
        return False
    return True




def IO_read(path,books,idList):
    '''
    :function: 用于从文件中读取图书信息
    :param path: 路径
    :return: 返回读入的图书信息
    '''
    count = 0
    errCount = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for item in content.splitlines():
        id = json.loads(item)['登录号']
        if(unique(id,idList)):
            books.append(json.loads(item))
            count+=1
            idList.append(id)
        else:
            errCount += 1
    print(f"已完成对{count}本书的导入,存在{errCount}本书因登录号重复而无法导入")
    print("===========================")
    return books



def IO_write(path,datas):
    '''
    :function: 用于将现有图书信息保存至文件
    :param path:存入路径
    :param data:现有图书信息
    :return:返回写入状态
    '''
    count = 0
    errCount = 0
    idListIO=[] # 用于记载目前文件数据库中的登录号
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for item in content.splitlines():
        idListIO.append(json.loads(item)['登录号'])

    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as file:
            for data in datas:
                if unique(data['登录号'],idListIO):
                    file.write(json.dumps(data, ensure_ascii=False) + '\n')
                    count+=1
                else:
                    errCount += 1
    else:
        with open(path, 'a', encoding='utf-8') as file:
            for data in datas:
                if unique(data['登录号'],idListIO):
                    file.write(json.dumps(data, ensure_ascii=False) + '\n')
                    count+=1
                else:
                    errCount += 1
    print(f"已完成{count}本书的写入,存在{errCount}本书因登录号重复而无法写入")
    print("===========================")



def books_add(books,idList):
    '''
    :function: 用于以控制台输入模式向已有图书库中添加图书信息
    :param books: 原图书库
    :return: 返回添加图书后的图书库
    '''
    try:
        id = int(input("请输入登录号:"))
        book_name = (input("请输入书名:"))
        author_name = (input("请输入作者："))
        classID = input("请输入分类号：")
        publisher = input("请输入出版单位：")
        publish_data = input("请输入出版时间：")
        price=float(input("请输入价格："))
        book = {
            '登录号':id,
            '书名': book_name,
            '作者': author_name,
            '分类号': classID,
            '出版单位': publisher,
            '出版时间': publish_data,
            '价格': price
        }
        if(id not in idList):
            books.append(book)  # 数据正常则插入已有书单中
            idList.append(id)
            print("---------------------------")
            print(f"【反馈】\n登录号{id}  书名《{book_name}》  作者{author_name}  分类号{classID} 的图书已成功加入图书库\n其出版单位：{publisher}  出版时间：{publish_data}  价格：{price}")
        else:
            print("---------------------------")
            print(f"登录号：{id} 的书籍已存在")
        time.sleep(1) # 延时1秒 用于阅读反馈 然后返回主菜单
        print("===========================")
        return books,idList
    except ValueError:
        print("输入数据类型异常，请检查输入数据是否正常")
        books_add(books,idList)




def books_preview(books:list):
    lenth = len(books)
    print(f"目前图书管理系统中记载图书：{lenth}本")
    if lenth != 0:
        print("图书信息简要如下：\n---------------------------")
        print("书名  --  作者  --  价格")
        for book in books:
            print(f"《{book['书名']}》 -- {book['作者']} -- {book['价格']}")
    print("===========================")





def books_quary(books:list):
    info = input("请输入作者名或者书名以查找\n输入：")
    print("---------------------------")
    count = 0  # 用于统计结果数
    for book in books:
        if book['作者'] == info or book['书名'] == info:
            if(count == 0):
                print("登录号  --  书名  --  作者  --  分类号  --  出版单位  --  出版时间  --  价格")
            print(f"{book['登录号']} -- 《{book['书名']}》 -- {book['作者']} -- {book['分类号']} --  {book['出版单位']} --  {book['出版时间']} -- {book['价格']}")
            count+=1
    if count == 0:
        print("未查找到相关书籍")
    else:
        print(f"查找到{count}本相关书籍")
    print("===========================")




# 启动程序
print("欢迎使用图书管理系统\n===========================")
print("【1】载入图书信息")  #
print("【2】添加图书信息")  # Finish
print("【3】获取图书信息")  # Finish
print("【4】查询图书信息")  # Finish
print("【5】保存图书信息")  #
print("【0】退出系统")
print("请输入【】内数字选择相应功能\n==========================\n选择:" , end='')
books = []   # 用于存储系统已有图书库
idList = []  # 用于维护唯一的登录号 以保证登录号唯一
while True:
    # 输入数据检查
    try:
        choice = int(input())
    except ValueError:
        print("请输入数字")   # 若输入非数字进行反馈
    if choice>=0 and choice<=5 :
        if choice == 1:
            books = IO_read(os.path.join("D:\\", "Documents", "Library", "books.txt"),books,idList)
        elif choice == 2:
            books,idList = books_add(books,idList)
        elif choice == 3:
            books_preview(books)
        elif choice == 4:
            books_quary(books)
        elif choice == 5:
            IO_write(os.path.join("D:\\", "Documents", "Library", "books.txt"),books)
        elif choice == 0:
            print("程序已结束")
            exit(0)





# 版权信息
# 作者：湖南工商大学 智管2201 严于思


# 使用说明
# 需要在D盘的Documens（系统自带的文档）文件夹下创建一个文件夹Library，并在该文件夹中创建一个名为books的txt文件






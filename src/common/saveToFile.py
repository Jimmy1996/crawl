# coding : UTF-8
import csv

'''
将内容存储至文件的类
'''
class save:
    '''
    存储至csv文件
    '''
    def toCsv(path,contentList):
        """
        :param contentList: 需要存储的内容
        :return: 无返回值
        """
        out = open(path, 'w', newline='')
        csv_write = csv.writer(out)
        for i in contentList:
            csv_write.writerow(i)
        out.close()
    '''
    存储至txt文件
    '''
    def toTxt(path,contentList):
        out = open(path,'a+')
        for i in contentList:
            out.write(i+"\n")
        out.close()


if __name__ == '__main__':
    list = []
    list.append("hhh")
    # save.toCsv('test.csv',list)
    save.toTxt('test.txt',list)
from page1.infoboard import Data
from page1.custsearch import CustSearch

def mainpage1():
    '''
    第一页内容函数
    '''
    ## 数据看板
    if len(Data.codepool) == 0:
        with open ('page1\stockcode.txt', 'r') as f:
            Data.codepool = f.read().splitlines()
            print(f"Data.codepool init success len:{len(Data.codepool)}")
    Data.infoboard()
    
    ## 自定义查询
    CustSearch.panel()
    

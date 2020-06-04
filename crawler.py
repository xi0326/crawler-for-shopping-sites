from filter import Filter
from sorter import Sorter
import search
import string

def isFilterWanted():
    wanted = input('Do you want filter?\ninput y or yes if you want\n')
    return True if wanted == 'y' or wanted == 'yes' else False

def isSortWanted():
    wanted = input('Do you want sort?\ninput y or yes if you want\n')
    return True if wanted == 'y' or wanted == 'yes' else False



def main():

    keyword = str(input('please input keyword\n'))
    targetSite = str(input('please input target site\n'))

    if keyword == '':
        print('no keyword')

    else:
        if isFilterWanted():
            filter = Filter()
            filter.set()
        else:
            filter = Filter()

        if isSortWanted():
            sorter = Sorter()
            sorter.set()
        else:
            sorter = Sorter()

        if targetSite.lower() == 'pchome':
            search.searchOnPChome(keyword, filter, sorter)
            
        elif targetSite.lower() == 'shopee' or  targetSite.lower() == 'xiapi' or targetSite == '蝦皮':
            search.searchOnShopee(keyword, filter, sorter)
 
        elif targetSite.lower() == 'qoo10':
            search.searchOnQoo10(keyword, filter, sorter)

        elif targetSite.lower() == 'etmall' or targetSite == '東森':
            search.searchOnEtmall(keyword, filter, sorter)

        elif targetSite.lower() == 'rakuten' or targetSite == '樂天':
            search.searchOnRakuten(keyword, filter, sorter)

        elif targetSite.lower() == 'all':
            search.searchOnPChome(keyword, filter, sorter)
            search.searchOnShopee(keyword, filter, sorter)
            search.searchOnQoo10(keyword, filter, sorter)
            search.searchOnEtmall(keyword, filter, sorter)

        elif targetSite.lower() == 'exit':
            exit()

        else:
            print('target site is not supported\nPlease input again or exit')
            main()  #recursive





if __name__== "__main__":
    main()
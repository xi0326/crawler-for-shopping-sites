from goods import Goods
from multiprocessing import Pool
import urllib.parse
import re
from bs4 import BeautifulSoup
import json
import time
import getResponse
from outputWithCSV import outputWithCSV

def timeCost(startTime, finTime, targetSite):
    if finTime - startTime < 60:
        print('cost time in ' + targetSite + ': '+ str(finTime - startTime) + ' secs\n')

    else:
        print('cost time in ' + targetSite + ': '+ str((finTime - startTime)/60) + ' mins\n')

def getProductInfoShopee(productUrl):
    result = Goods()
    response = getResponse.getResponseByGet(productUrl)

    if response == None:
        return None

    itemData = json.loads(response.text)
    result.setName(itemData.get('item').get('name'))
    result.setPrice(int(itemData.get('item').get('price')/100000))               
    result.setSite('https://shopee.tw/' + urllib.parse.quote(itemData.get('item').get('name').replace(' ', '-')) + '-i.' + str(itemData.get('item').get('shopid')) + '.' + str(itemData.get('item').get('itemid')))
    return result

def searchOnPChome(keyword, filter, sorter):
    startTime = time.time()
    print('Crawling(PChome)\n')
    results = []
    success = False
    page = 0
    while(True):
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + urllib.parse.quote(keyword) + '&page=' + str(page) + '&sort=sale/dc'
        page += 1
        response = getResponse.getResponseByGet(url)
        if response == None:
            break

        pageData = json.loads(response.text)
        productDatas = pageData.get('prods')
        if productDatas == None:
            break
        else:
            success =True

            for productData in productDatas:
                result = Goods()
                result.setName(productData.get('name'))
                result.setPrice(productData.get('price'))
                result.setSite('https://24h.pchome.com.tw/prod/' + productData.get('Id'))
                results.append(result)
                #result.show_detail()

    if success:
        outputWithCSV('PChome', keyword, results, startTime, filter, sorter)

    else:
        print('no result from PChome\n')

    print('crawled(PChome)')
    finTime = time.time()
    timeCost(startTime, finTime, 'PChome')

def searchOnShopee(keyword, filter, sorter):
    startTime = time.time()
    print('Crawling(Shopee)\n')
    results = []
    success = False
    newest = 0
    while(True):
        url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword=' + urllib.parse.quote(keyword) + '&limit=50&newest=' + str(newest) + '&order=desc&page_type=search&version=2'
        newest += 50
        productUrls = []
        response = getResponse.getResponseByGet(url)
        if response == None:
            break

        pageData = json.loads(response.text)      
        productDatas = pageData.get('items')
        if productDatas == None:
            break
        else:
            success =True

            for productData in productDatas:
                productUrl = 'https://shopee.tw/api/v2/item/get?itemid=' + str(productData.get('itemid')) + '&shopid=' + str(productData.get('shopid'))
                productUrls.append(productUrl)

            pool = Pool()
            productResults = pool.map(getProductInfoShopee, productUrls)            
            pool.close()
            pool.join()
            for r in productResults:
                results.append(r)

    if success:
        outputWithCSV('Shopee', keyword, results, startTime, filter, sorter)
    else:
        print('no result from shopee\n')

    print('crawled(Shopee)')
    finTime = time.time()
    timeCost(startTime, finTime, 'Shopee')

def searchOnQoo10(keyword, filter, sorter):
    startTime = time.time()
    print('Crawling(Qoo10)\n')
    results = []
    success = False
    page = 0
    while(True):
        url = 'https://www.qoo10.tw/gmkt.inc/Search/DefaultAjaxAppend.aspx?search_keyword=' + urllib.parse.quote(keyword) + '&search_type=SearchItems&f=&st=TW&s=r&v=lt&p=' + str(page) + '&pm=&so=&cc=N&cb=N'
        page += 1

        response = getResponse.getResponseByGet(url)
        if response == None:
            break

        pageData = BeautifulSoup(response.text, 'lxml')
        productNames = []
        productPrices = []
        productSites = []
        productDatas = pageData.find('table')
        if productDatas == None:
            break

        else:
            success =True
            ns = productDatas.find_all('div', class_='sbj')
            ps = productDatas.find_all('strong', title='折扣價')
            ss = productDatas.find_all('a', href = re.compile('https://www.qoo10.tw/item/'), attrs={'data-type': 'goods_url'})
            
            for n in ns:
                productNames.append(n.text)
            for p in ps:
                productPrices.append(int(p.text[3:].replace(',', '')))
            for i in range(len(ss)):
                if i % 2 == 0:
                    productSites.append(ss[i].get('href'))

            for i in range(len(productSites)):
                result = Goods()
                result.setName(productNames[i])
                result.setPrice(productPrices[i])
                result.setSite(productSites[i])
                results.append(result)
                #result.show_detail()

    if success:
        outputWithCSV('Qoo10', keyword, results, startTime, filter, sorter)
    else:
        print('no result from Qoo10\n')

    print('crawled(Qoo10)')
    finTime = time.time()
    timeCost(startTime, finTime, 'Qoo10')

def searchOnEtmall(keyword, filter, sorter):
    startTime = time.time()
    print('Crawling(ETMall)\n')
    results = []
    success = False
    page = 0
    while(True):
        url = 'https://www.etmall.com.tw/Search/Get'
        payload = {'keyword':keyword,
                    'model[cateName]':'全站',
                    'model[page]':'0',
                    'model[storeID]':'',
                    'model[cateID]': '-1',
                    'model[filterType]':'',
                    'model[sortType]':'',
                    'model[moneyMaximum]':'',
                    'model[moneyMinimum]':'',
                    'model[pageSize]':'48',
                    'model[SearchKeyword]':'',
                    'model[fn]':'',
                    'model[fa]':'',
                    'model[token]':'',
                    'model[bucketID]':'1',
                    'page':str(page)
                    }
        payloadType = 'data'
        response = getResponse.getResponseByPost(url, payload, payloadType)
        page += 1
        if response == None:
            break

        pageData = json.loads(response.text)
        productDatas = pageData.get('searchResult').get('products')

        if productDatas == []:
            break

        else:
            success =True
            for productData in productDatas:
                result = Goods()
                result.setName(productData.get('title'))
                result.setPrice(int(productData.get('finalPrice')))
                result.setSite('https://www.etmall.com.tw/' + urllib.parse.quote(productData.get('pageLink')))
                results.append(result)
                #result.show_detail()

    if success:
        outputWithCSV('ETMall', keyword, results, startTime, filter, sorter)
    else:
        print('no result from ETMall\n')

    print('crawled(ETMall)')
    finTime = time.time()
    timeCost(startTime, finTime, 'ETMall')

def searchOnRakuten(keyword, filter, sorter):
    startTime = time.time()
    print('Crawling(Rakuten)\n')
    results = []
    success = False
    page = 0
    while(True):
        page += 1
        url = 'https://www.rakuten.com.tw/graphql'
        payloadJson = json.loads('{"operationName":"fetchSearchPageResults","variables":{"parameters":{"pageNumber":' + str(page) + ',"keyword":"' + keyword + '"}},"query":"query fetchSearchPageResults($parameters: SearchInputType!) {\n  searchPage(parameters: $parameters) {\n    serializedKey\n    title\n    result {\n      abTestVariation\n      items {\n        ...SearchResultItemFragment\n        __typename\n      }\n      totalItems\n      conjunction\n      isSecondSearch\n      __typename\n    }\n    recommendationRefItem {\n      shopId\n      itemId\n      rakutenCategoryTree\n      __typename\n    }\n    pagination {\n      itemsPerPage\n      pageNumber\n      totalItems\n      __typename\n    }\n    currentCategoryInfo {\n      ...BaseCategoryFragment\n      __typename\n    }\n    parentCategoryInfoList {\n      ...BaseCategoryFragment\n      __typename\n    }\n    baseFacetCategoryList {\n      ...FacetCategoryFragment\n      __typename\n    }\n    brandList {\n      id\n      name\n      count\n      __typename\n    }\n    appliedFilter {\n      brandList {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    seoMeta {\n      title\n      description\n      keywords\n      paginationPrev\n      paginationNext\n      canonical\n      robots\n      __typename\n    }\n    seoOverwritePath\n    dataLayer {\n      page_info {\n        marketplace\n        device\n        ctrl\n        project\n        page_products {\n          brand\n          currency\n          item_id\n          prod_id\n          prod_image_url\n          prod_name\n          prod_uid\n          prod_url\n          stock_available\n          __typename\n        }\n        page_cat {\n          cat_id\n          cat_name\n          cat_mpath\n          __typename\n        }\n        __typename\n      }\n      search_info {\n        search_keyword\n        raw_search_keyword\n        search_type\n        filters {\n          filter_active\n          filter_name\n          filter_value\n          filter_list {\n            filter_checked\n            filter_label\n            filter_qty\n            __typename\n          }\n          __typename\n        }\n        campaigns {\n          campaign_active\n          campaign_name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SearchResultItemFragment on SearchResultItem {\n  baseSku\n  itemId\n  itemName\n  itemUrl\n  itemPrice {\n    min\n    max\n    __typename\n  }\n  itemListPrice {\n    min\n    max\n    __typename\n  }\n  itemOriginalPrice {\n    min\n    max\n    __typename\n  }\n  itemStatus\n  itemImageUrl\n  shopId\n  shopUrl\n  shopPath\n  shopName\n  review {\n    reviewScore\n    reviewCount\n    reviewUrl\n    __typename\n  }\n  point {\n    min\n    max\n    magnification\n    __typename\n  }\n  campaignType\n  isAdultProduct\n  hideDiscountInfo\n  __typename\n}\n\nfragment BaseCategoryFragment on SearchPageCategoryType {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  __typename\n}\n\nfragment FacetCategoryFragment on SearchPageFacetCategory {\n  id\n  isLeafNode\n  level\n  name\n  parentId\n  count\n  __typename\n}\n"}', strict=False)
        payloadType = 'json'
        response = getResponse.getResponseByPost(url, payloadJson, payloadType)
        if response == None:
            break

        pageData = json.loads(response.text)
        productDatas = pageData.get('data').get('searchPage').get('result').get('items')
        if productDatas == []:
            break
        else:
            success =True

            for productData in productDatas:
                result = Goods()
                result.setName(productData.get('itemName'))
                result.setPrice(productData.get('itemPrice').get('min'))
                result.setSite(productData.get('itemUrl'))
                results.append(result)
                #result.show_detail()
            
    if success:
        outputWithCSV('Rakuten', keyword, results, startTime, filter, sorter)

    else:
        print('no result from Rakuten\n')

    print('crawled(Rakuten)')
    finTime = time.time()
    timeCost(startTime, finTime, 'Rakuten')

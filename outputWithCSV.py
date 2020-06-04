import csv
import time
import os

def outputWithCSV(targetSite, keyword, results, startTime, filter, sorter):
    startTimeStr = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(startTime))
    print('result amounts from ' + targetSite + ' without filter:', len(results), '\n')
    results = filter.priceFilter(results)
    print('result amounts from ' + targetSite + ' with filter:', len(results), '\n')
    results = sorter.sort(results)
    if not os.path.exists(keyword):
        os.mkdir(keyword)

    with open(keyword + '\\' + startTimeStr + ' from ' + targetSite + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'price', 'site'])
        for result in results:
            writer.writerow(result.getByList())

from selenium import webdriver

import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

link = "https://locator.chase.com/search?q=&l=en"

chrome_options = Options()  
chrome_options.add_argument("--headless")     
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options)  
driver.get(link)

buttonXpath = '//*[@id="js-locator"]/div[2]/div[4]/div[2]/ul'
resultsXpath = '//*[@id="js-locator"]/div[2]/div[4]/div[1]/div[2]/ol'
resultSummaryCount = driver.find_element_by_class_name('ResultSummary-count').text

pageResults = driver.find_element_by_xpath(resultsXpath).find_elements_by_tag_name('li')

resultItem = pageResults[0]
# name
print(resultItem.find_element_by_class_name('LocationName-geo').text)
# addressLine
print(resultItem.find_element_by_class_name('c-address-street-1').text)
# city
print(resultItem.find_element_by_class_name('c-address-city').text)
# state
print(resultItem.find_element_by_class_name('c-address-state').text)
# zipCode
print(resultItem.find_element_by_class_name('c-address-postal-code').text)

outputFile = open('result.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)



while True:
    pageLastItemCount = resultSummaryCount.split()[2]
    totalLastItemCount = resultSummaryCount.split()[-1]

    print(resultSummaryCount)

    while True:
        try:
            pageResults = driver.find_element_by_xpath(resultsXpath).find_elements_by_tag_name('li')

            for resultItem in pageResults:
                    tempList = []
                    # name
                    tempList.append(resultItem.find_element_by_class_name('LocationName-geo').text)
                    # addressLine
                    tempList.append(resultItem.find_element_by_class_name('c-address-street-1').text)
                    # city
                    tempList.append(resultItem.find_element_by_class_name('c-address-city').text)
                    # state
                    tempList.append(resultItem.find_element_by_class_name('c-address-state').text)
                    # zipCode
                    tempList.append(resultItem.find_element_by_class_name('c-address-postal-code').text)
                    # print(tempList)
                    outputWriter.writerow(tempList)
            break
        except:
            continue

    oldResultSummaryCount = resultSummaryCount

    if int(pageLastItemCount) == int(totalLastItemCount):
        break

    while True:
        try:
            nextButton = driver.find_element_by_xpath(buttonXpath).find_elements_by_tag_name('li')[-1]
            nextButton.find_element_by_tag_name('button').click()
            break
        except:
            continue

    while resultSummaryCount == oldResultSummaryCount:
        try:
            # nextButton = driver.find_element_by_xpath(buttonXpath).find_elements_by_tag_name('li')[-1]
            # nextButton.find_element_by_tag_name('button').click()
            resultSummaryCount = driver.find_element_by_class_name('ResultSummary-count').text
        except:
            continue

outputFile.close()
driver.close()
from selenium import webdriver
from splinter import Browser
import time

def wevi_automate(wevi_data, num_iterations):
    with Browser('firefox') as browser:
        url = 'http://localhost:63342/zdm_centrality/wevi2/wevi/index.html?_ijt=5r1umtb21b54k6emr31kqu4ssb'
        browser.visit(url)
        text_input_place = browser.find_by_id('input-text')
        text_input_place.fill(wevi_data)
        time.sleep(10)
        iterations_input_box = browser.find_by_id('num-iterations')
        iterations_input_box.fill(num_iterations)
        # Find and click the 'update and restart' button
        button = browser.find_by_id('btn-restart')
        button.click()
        time.sleep(10)
        # Find and click the 'update and restart' button
        button = browser.find_by_id('btn-nextcustome')
        button.click()
        while True:
            try:
                alert = browser.get_alert()
                if alert is not None :
                    break
                time.sleep(10)
            except:
                    time.sleep(10)
                    print "tried so hard and got so far"
            # We expect "Done" to be printed
        print alert.text
        alert.accept()
        # Find and click the 'click all neurons' button
        button = browser.find_by_id('btn-click-all')
        button.click()
        # Find and click the 'show numeric data' button
        button = browser.find_by_id('btn-show-numbers')
        button.click()
        alert = browser.get_alert()
        print 'In the end - it doesnt even matter!'
        return alert.text
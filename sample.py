import string
import subprocess,os
from time import sleep
from xml.dom.expatbuilder import parseString
from clicknium import clicknium as cc, locator, ui
from clicknium.common.enums import ClickType,ClearHotKey,PreAction
import requests
import math

search_key_word = 'camisetas'

def main():
    # open website
    tab = cc.chrome.open("https://www.redbubble.com/es/")

    # input search key word, and click the search button
    tab.find_element(locator.redbubble.txt_search).set_text(search_key_word)
    tab.find_element(locator.redbubble.btn_search).click()

    # sleep 4 seconds,wait the page loading
    sleep(4)

    # set the filter 
    tab.find_element(locator.redbubble.radio_mujer).click()
    tab.find_element(locator.redbubble.radio_camiseta_ancha).click()
    sleep(4)

    # get top 3 pages image
    for x in range(0,3):
        # scroll page to load all item's image
        tab.find_element(locator.redbubble.nav_scroll).hover()
        cc.mouse.scroll(-100)
        
        # get the similar elements
        similar_elements_img = tab.find_elements(locator.redbubble.similar_img)
        print(f'similar_elements_img count:{len(similar_elements_img)}')
        index = 0
        for img in similar_elements_img:
            download_img(img,index)
            index+=1
        
        exist_next_page = tab.wait_appear(locator.redbubble.btn_next_page,wait_timeout=5)
        if(exist_next_page != None):
            # tab.find_element(locator.redbubble.btn_next_page).click()
            exist_next_page.click()
            sleep(4)
        else:
            break

    sleep(3)
    tab.close()
    

def download_img(img_obj,index):
    img_src = img_obj.get_property('src')
    print(f'index:{index},start download: {img_src}...')
    
    # img = requests.get(img_src, 
    #                 proxies=dict(http='socks5://127.0.0.1:10808',
    #                              https='socks5://127.0.0.1:10808'))
    
    img = requests.get(img_src)
    filepath = './download/'+img_src.split('/')[-1]
    filepath = filepath.replace(',','_').replace(':','_')
    print(f'---------------{filepath}----------')
    i = 1
    while(os.path.exists(filepath)):
        filepath = f'./download/{img_src.split("/")[-1].split(".jpg")[0].replace(",","_").replace(":","_")}-{i}.jpg'
        i+=1
    
    with open(filepath,'wb') as f:
        f.write(img.content)
    print(f'index:{index},download success!')

if __name__ == "__main__":
    main()
    
    

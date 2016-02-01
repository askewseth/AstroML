# coding: latin-1

from selenium import webdriver

driver = webdriver.Firefox()

driver.get("http://basebe.obspm.fr/basebe/BeSS/Consul.php")


#Elements on page
star_name = driver.find_element_by_name("req_objet")
resolution_min = driver.find_element_by_name("req_resolution§min")
date_min = driver.find_element_by_name("req_date§min")
wave_min = driver.find_element_by_name("req_wave§1")
wave_max = driver.find_element_by_name("req_wave§2")
submit_button = driver.find_element_by_name("submit")

#keys to send
date_min.send_keys("1990-01-01") #YYYY-MM-DD
resolution_min.send_keys("10000")
star_name.send_keys("Psi Per")

#click submit to go to next page
submit_button.click()


#sort by latest date
sort_date_dec = driver.find_element_by_name("req_tri_hjdm")
sort_date_dec.click()

#click all of the checkboxes for download
checkboxes = driver.find_elements_by_name("check[]")
for x in checkboxes:
    x.click()

#download the files
download_button = driver.find_element_by_name("multidownload")
download_button.click()

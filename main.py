from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable as pt

# path for phantomjs binary
path_phantom = "/home/nox/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"

# Create a new instance of the Firefox driver
# driver = webdriver.Firefox()

# create an instance of phantomjs
driver = webdriver.PhantomJS(executable_path = path_phantom)

driver.implicitly_wait(20)
# go to the google home page
driver.get("http://gen.lib.rus.ec/")

# inputElement = driver.findElement(By.id("searchform"))
inputElement = driver.find_element_by_id("searchform")


# type in the search
inputElement.send_keys("when breath becomes air")
# inputElement.send_keys(Keys.RETURN)
# driver.find_element_by_css_selector('input[type=\"submit\"]').click()
inputElement.submit()

# the page is ajaxy so the title is originally this:
print driver.title

# WebDriverWait(driver, 10).until(EC.)
table = driver.find_element_by_class_name("c")

rows = table.find_elements_by_tag_name("tr")
columns = rows[0].find_elements_by_tag_name("td")

print "Rows: " + str(len(rows))
print "Columns: " + str(len(columns))

header=[]
for i in range(1,9):
	header.append(columns[i].text)

columns1 = rows[1].find_elements_by_tag_name("td")
each_row = []
for i in range(1,9):
	each_row.append(columns1[i].text)

table = pt(header)
table.add_row(each_row)
print table
# href = rows[1].find_element_by_partial_link_text("md5")
# print href

# print columns[2].find_element_by_partial_link_text("When Breath Becomes Air").get_attribute("href")


# driver.quit()
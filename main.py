from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable as pt
# from tabulate import tabulate
import textwrap
import re

# path for phantomjs binary
path_phantom = "phantomjs/bin/phantomjs"

# Create a new instance of the Firefox driver
# driver = webdriver.Firefox()

# create an instance of phantomjs
driver = webdriver.PhantomJS(executable_path = path_phantom)

print("Fetching results. Please wait...")
driver.implicitly_wait(20)

driver.get("http://gen.lib.rus.ec/")

inputElement = driver.find_element_by_id("searchform")

# type in the search
inputElement.send_keys("harry potter and the deathly hallows")
inputElement.submit()

# the page is ajaxy so the title is originally this:
print driver.title

table = driver.find_element_by_class_name("c")

rows = table.find_elements_by_tag_name("tr")
columns = rows[0].find_elements_by_tag_name("td")

# print "Rows: " + str(len(rows))
# print "Columns: " + str(len(columns))

header=[]
# for i in range(1,9):
for i in [1,2,6,7]:
	header.append(columns[i].text)
header.append("md5")
table = pt(header)

print "\nOK. Done!"

# Testing purposes :
# ------------------
# columns1 = rows[1].find_elements_by_tag_name("td")
# each_row = []
# italics = columns1[2].find_elements_by_tag_name("i")
# print type(italics)
# print italics
# italics = italics[-1].text
# # print italics
# a = columns1[2].text
# # a = str(a)
# a = a.replace(italics, '')
# print a
# print type(a)
# allrows = []

for i in range(1, len(rows)):
	all_columns = rows[i].find_elements_by_tag_name("td")
	each_row = []
	# for j in range(1,9):
	for j in [1,2,6,7]:
		# to remove the italics
		if j == 2:
			string = all_columns[j].text
			italics = all_columns[j].find_elements_by_tag_name("i")
			if italics:
				italics = italics[-1].text
				string = string.replace(italics, '')
			string = "\n".join(textwrap.wrap(string, 60))
			string = string.encode('ascii', 'ignore')
			each_row.append(string)
			href = all_columns[j].find_element_by_id(str(all_columns[0].text)).get_attribute("href")
			md5 = (re.findall("md5=(.*)", href))[0]
		else:
			each_row.append((all_columns[j].text).encode('ascii', 'ignore'))
	each_row.append(md5)
	table.add_row(each_row)

# table = tabulate(allrows, header, tablefmt = "simple")
print table


# driver.quit()
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable as pt
import textwrap

# path for phantomjs binary
path_phantom = "phantomjs/bin/phantomjs"

# Create a new instance of the Firefox driver
# driver = webdriver.Firefox()

# create an instance of phantomjs
driver = webdriver.PhantomJS(executable_path = path_phantom)

print("Fetching results. Please wait...")
driver.implicitly_wait(20)
# go to the google home page
driver.get("http://gen.lib.rus.ec/")

# inputElement = driver.findElement(By.id("searchform"))
inputElement = driver.find_element_by_id("searchform")


# type in the search
inputElement.send_keys("harry potter and the deathly hallows")
# inputElement.send_keys(Keys.RETURN)
# driver.find_element_by_css_selector('input[type=\"submit\"]').click()
inputElement.submit()

# the page is ajaxy so the title is originally this:
print driver.title

# WebDriverWait(driver, 10).until(EC.)
table = driver.find_element_by_class_name("c")

rows = table.find_elements_by_tag_name("tr")
columns = rows[0].find_elements_by_tag_name("td")

# print "Rows: " + str(len(rows))
# print "Columns: " + str(len(columns))

header=[]
# for i in range(1,9):
for i in [1,2,6,7]:
	header.append(columns[i].text)

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
		else:
			each_row.append((all_columns[j].text).encode('ascii', 'ignore'))
	# print each_row, "\n\n"
	table.add_row(each_row)

print table

# print columns[2].find_element_by_partial_link_text("When Breath Becomes Air").get_attribute("href")


# driver.quit()
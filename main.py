import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable as pt
import textwrap

def connection_init():
	try:
		# path for phantomjs binary
		path_phantom = "phantomjs/bin/phantomjs"

		# Create a new instance of the Firefox driver
		# driver = webdriver.Firefox()

		# create an instance of phantomjs
		driver = webdriver.PhantomJS(executable_path = path_phantom)

		print("Fetching results. Please wait...")
		driver.implicitly_wait(20)

		driver.get("http://gen.lib.rus.ec/")
		return driver
	except:
		print "\nSorry, there seems to be some problem. (1)Check your internet connection. (2)The libgen servers might be down\nPlease try again"

def get_search_results_name(driver, search_str):
	try:
		inputElement = driver.find_element_by_id("searchform")

		# type in the search
		inputElement.send_keys(search_str)
		inputElement.submit()

		# the page is ajaxy so the title is originally this:
		print driver.title

		# the table which contains all the data has class name 'c'
		table = driver.find_element_by_class_name("c")

		# extract all rows and columns from table
		rows = table.find_elements_by_tag_name("tr")
		columns = rows[0].find_elements_by_tag_name("td")

		# add header to thhe table. The format is [No., Author, Title, Language, Size, md5]
		header=[]
		header.append("No.")
		for i in [1,2,6,7]:
			header.append(columns[i].text)
		header.append("md5")
		table = pt(header)


		# add all rows to the table
		for i in range(1, len(rows)):
			all_columns = rows[i].find_elements_by_tag_name("td")
			each_row = []
			each_row.append(i)
			for j in [1,2,6,7]:
				if j == 1:
					# wrap the author name to 20 chars to avoid overruning
					string = all_columns[j].text
					string = "\n".join(textwrap.wrap(string, 20))
					string = string.encode('ascii', 'ignore')
					each_row.append(string)
				# to remove the italics
				elif j == 2:
					string = all_columns[j].text
					italics = all_columns[j].find_elements_by_tag_name("i")
					if italics:
						italics = italics[-1].text
						string = string.replace(italics, '')
					# wrap title to 60 chars
					string = "\n".join(textwrap.wrap(string, 60))
					string = string.encode('ascii', 'ignore')
					each_row.append(string + "\n")
					# get the a tag to extract the href attribute which contains md5
					href = all_columns[j].find_element_by_id(str(all_columns[0].text)).get_attribute("href")
					md5 = (re.findall("md5=(.*)", href))[0]
				else:
					each_row.append((all_columns[j].text).encode('ascii', 'ignore'))
			each_row.append(md5)
			table.add_row(each_row)

		print "\nOK. Done!"
		print table

	except:
		print "\nSorry, there seems to be some problem. (1)Check your internet connection (2)The libgen server did not respond\nPlease try again"
		driver.quit()

def get_search_results_md5(driver, md5_search_str):
	pass


if __name__ == "__main__":
	driver = connection_init()
	if len(sys.argv) == 1:
		search_str = raw_input("The book you want to search:\n")
		get_search_results_name(driver, search_str)
	elif len(sys.argv) == 2:
		get_search_results_md5(driver, sys.argv[1])
	else:
		print "Sorry, invalid option. Please try again"
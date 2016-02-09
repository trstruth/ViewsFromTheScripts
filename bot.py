from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def loadInfo(filepath):

	infoDict = {}
	with open(filepath) as userInfo:
		for line in userInfo:
			thisInfo = line.split(':')
			infoDict[thisInfo[0]] = thisInfo[1].rstrip()
	return infoDict

def login(driver, infoDict):

	driver.get('http://www.octobersveryown.com/accounts/login/?next=/shop/')

	emailField = driver.find_element_by_id('id_username')
	emailField.send_keys(infoDict['email'])

	passwordField = driver.find_element_by_id('id_password')
	passwordField.send_keys(infoDict['password'])

	submitBtn = driver.find_element_by_xpath("//div[@id='main']/form/input[@value='Login']")
	submitBtn.click()

def waitForNewProduct(driver):

	productList = driver.find_element_by_xpath("//div[@id='main']/ul[@class='product-grid clearfix']").find_elements_by_xpath(".//li[@class='product']")
	numProducts = len(productList)

	while(True):
		productList = driver.find_element_by_xpath("//div[@id='main']/ul[@class='product-grid clearfix']").find_elements_by_xpath(".//li[@class='product']")
		if len(productList) > numProducts:
			return
		driver.refresh()

def navigateToProductPage(driver, keyword):

	productList = driver.find_element_by_xpath("//div[@id='main']/ul[@class='product-grid clearfix']").find_elements_by_xpath(".//li[@class='product']")

	for aProduct in productList:
		descriptor = aProduct.find_element_by_xpath(".//a[1]").get_attribute("href")
		if keyword in descriptor:
			aProduct.click()
			return

def addToCart(driver, infoDict):

	mySize = infoDict['size']
	options = driver.find_element_by_id('options') 
	sizing = options.find_element_by_name('Size')
	sizeMenu = sizing.find_element_by_tag_name('select').find_elements_by_tag_name('option')
	sizing.click()

	for aSize in sizeMenu:
		sizing.click()
		if aSize.get_attribute('value') == mySize:
			break

	options.find_element_by_id('addcart').click()

def checkout(driver):

	driver.find_element_by_xpath(".//div[@id='main']/div[@class='cart-foot']/a").click()

def billShip(driver):

	driver.find_element_by_id('id_paymentmethod_1').click()
	driver.find_element_by_xpath("//div[@id='main']/form[@class='pay-info']/input[@type='submit']").click()

def secureCheckout(driver, infoDict):

	cardNumber = infoDict['cardNumber']
	cardExpMonth = infoDict['cardExpMonth']
	cardExpYear = infoDict['cardExpYear']
	cardCCV = infoDict['cardCCV']

	driver.find_element_by_id('id_credit_number').send_keys(cardNumber)

	month_expires = driver.find_element_by_id('id_month_expires')
	months = month_expires.find_elements_by_tag_name('option')
	month_expires.click()
	for aMonth in months:
		if aMonth.get_attribute('value') == cardExpMonth:
			aMonth.click()
			break

	year_expires = driver.find_element_by_id('id_year_expires')
	years = year_expires.find_elements_by_tag_name('option')
	year_expires.click()
	for aYear in years:
		if aYear.get_attribute('value') == cardExpYear:
			aYear.click()
			break

	driver.find_element_by_id('id_ccv').send_keys(cardCCV)
	
	driver.find_element_by_xpath("//div[@id='main']/form[@method='post']/input[@type='submit']").click()

def main():

	# intializes a new driver
	driver = webdriver.Chrome()

	# loads the information from the info.txt file in the same directory
	infoDict = loadInfo("info.txt")

	# logs into your ovo acc using the information provided in info.txt
	login(driver, infoDict)

	# navigates to the shop page
	driver.get('http://www.octobersveryown.com/shop/')

	# waits for the new product to be posted on the page, returns when a new product has been posted
	waitForNewProduct(driver)

	# finds the first product whos url contains the given keyword, and navigates to its page
	navigateToProductPage(driver, infoDict['keyword'])

	# adds the item to cart with the correct sizing
	addToCart(driver, infoDict)

	# clicks checkout and proceeds to the payment step
	checkout(driver)

	# selects the credit card option and continues
	billShip(driver)

	# fills out payment information and continues
	secureCheckout(driver, infoDict)

	driver.close()

if __name__ == '__main__':
	main()
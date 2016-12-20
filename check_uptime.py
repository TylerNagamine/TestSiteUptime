import requests
import json
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

slackUrl = ''

def postToSlack(message):
	data = '{"text": "' + message + '"}'

	r = requests.post(slackUrl, data)

def slack_message_on_error(func):
	def wrapper(driver):
		try:
			func(driver)
		except NoSuchElementException as err:
			
			error = json.loads(err.msg)
			errorMessage = error["errorMessage"]
			timestamp = datetime.now()
			slackMessage = "{0}: Tests failed: {1} in function {2}".format(str(timestamp), errorMessage, str(func.__name__))
			postToSlack(slackMessage)
	return wrapper

class LoginSmokeTests(object):
	finagraph_username_id = 'UserName'
	finagraph_password_id = 'Password'

	moodys_username_id = 'email'
	moodys_password_id = 'password'

	def __init__(self, driver):
		self.driver = driver

	@slack_message_on_error
	def TestBbcLoginPage(self):
		self.driver.get("https://bbceasy.com/login")
		username_element = self.driver.find_element_by_id(self.finagraph_username_id)
		password_element = self.driver.find_element_by_id(self.finagraph_password_id)

	@slack_message_on_error
	def TestFinagraphLoginPage(self):
		self.driver.get("https://app.finagraph.com/login")
		username_element = self.driver.find_element_by_id(self.finagraph_username_id)
		password_element = self.driver.find_element_by_id(self.finagraph_password_id)

	@slack_message_on_error
	def TestMarqLoginPage(self):
		self.driver.get("https://www.marqscore.com/login")
		username_element = self.driver.find_element_by_id(self.moodys_username_id)
		password_element = self.driver.find_element_by_id(self.moodys_password_id)

def main():
	global slackUrl
	slackUrl = ''

	driver = webdriver.PhantomJS()
	driver.set_window_size(1024, 768)
	# driver.implicitly_wait(30)

	tests = LoginSmokeTests(driver)
	tests.TestBbcLoginPage()
	tests.TestFinagraphLoginPage()
	tests.TestMarqLoginPage()

if __name__ == "__main__":
	main()
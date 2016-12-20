import requests
import json
import time
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
	marq_score_guage_id = 'score'

	def __init__(self):
		self.driver = webdriver.PhantomJS()

		self.driver.set_window_size(1024, 768)
		self.driver.implicitly_wait(30)

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
		self.driver.get("https://qab.marqscore.com/login")
		# self.driver.get("https://qab.test.marq.finagraph.com/login")
		username_element = self.driver.find_element_by_id(self.moodys_username_id)
		password_element = self.driver.find_element_by_id(self.moodys_password_id)

		username_element.send_keys('')
		password_element.send_keys('')

		password_button = self.driver.find_element_by_css_selector('button[data-bind="click: login"]')
		password_button.click()

		score = self.driver.find_element_by_id(self.marq_score_guage_id)

def main():
	global slackUrl
	slackUrl = ''

	print('\n{0}: Running tests...'.format(str(datetime.now())))

	for i in range(0, 2):
		tests = LoginSmokeTests()

		print('	Test {0} of login pages.'.format(str(i + 1)), end='')
		start_time = time.time()
		tests.TestBbcLoginPage()
		tests.TestFinagraphLoginPage()
		tests.TestMarqLoginPage()
		print('		...Complete.  Run time: {0} seconds.'.format(str(time.time() - start_time)))

	print('{0}: Tests complete.\n'.format(str(datetime.now())))

if __name__ == "__main__":
	main()
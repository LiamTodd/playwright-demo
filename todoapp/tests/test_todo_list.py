from playwright.sync_api import expect

from todoapp.tests.base_playwright_test_case import BasePlaywrightTestCase


class TodoTestCase(BasePlaywrightTestCase):

	def go_to_todo_list(self):
		page = self.browser.new_page()
		page.goto(f"{self.live_server_url}/todoapp/")
		return page

	def test_todo_items_are_added(self):
		# manually
		pass

	def test_todo_items_are_deleted(self):
		# code gen
		pass

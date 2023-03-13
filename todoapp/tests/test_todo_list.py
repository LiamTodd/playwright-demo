from playwright.sync_api import expect

from todoapp.tests.base_playwright_test_case import BasePlaywrightTestCase


class TodoTestCase(BasePlaywrightTestCase):

	def go_to_todo_list(self):
		page = self.browser.new_page()
		page.goto(f"{self.live_server_url}")
		return page

	def test_todo_items_are_added(self):
		# manually
		test_content = 'test item content'
		page = self.go_to_todo_list()
		page.locator("[id=todo-input]").fill(test_content)
		page.locator("[type=submit][value='Add Todo Item']").click()
		expect(page.get_by_role("list")).to_contain_text(test_content)

	def test_todo_items_are_deleted(self):
		# code gen
		pass

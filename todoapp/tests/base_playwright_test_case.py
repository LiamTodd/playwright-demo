import os

from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright


class BasePlaywrightTestCase(LiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		# This allows playwright to run sync operations inside its event loop. By default, DJANGO_ALLOW_ASYNC_UNSAFE
		# it is set to "false" so that sync operations inside event loops don't block the entire loop, but in the test
		# environment, blocking the event loop is ok.
		# See https://github.com/microsoft/playwright-python/issues/224
		os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
		super().setUpClass()
		cls.playwright = sync_playwright().start()

	@classmethod
	def tearDownClass(cls):
		os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "false"
		super().tearDownClass()
		cls.playwright.stop()

	def setUp(self):
		super().setUp()
		self.browser = self.playwright.chromium.launch(headless=False)

	def tearDown(self):
		super().tearDown()
		self.browser.close()

### What is Playwright?
- Browser automation tool
  - Chromium, Firefox and WebKit
- Node, Python, Java, .NET
- https://playwright.dev/python/docs/api/class-playwright
- https://playwright.dev/docs/intro
- https://github.com/microsoft/playwright
### Use cases
- Automated testing
  - End-to-end and UI testing
    - https://playwright.dev/python/docs/writing-tests
  - Performance testing
    - https://www.artillery.io/docs/guides/guides/playwright
- Web scraping
### Compared to Selenium
- Playwright
  - Out-of-the-box, has
    - Multi-browser support
    - Code gen tool
  - Has simpler installation and setup
  - Is generally faster
- Selenium
  - Has an older and larger community and more comprehensive docs
  - Has broader language and browser support
### Installing playwright:
1. `pip install playwright`
   - Installs the sync and async APIs
2. `playwright install`
   - Installs web browsers
     - Chromium, Webkit, Firefox
##### FYI:
Installing playwright on DERMS required us to install an additional linux package (libasound2) on our base image.
### Writing tests
We used LiveServerTestCase with the playwright_sync library and Playwright's built-in assertions (expect)
- LiveServerTestCase
  - Allows the use of automated test clients other than Django's own dummy client
  - Runs a server on a free port assigned by your OS, the URL of which is accessible via `self.live_server_url`
  - https://docs.djangoproject.com/en/4.1/topics/testing/tools/#liveservertestcase
- sync_api
  - Blocking behaviour, which is slower, but also what you'd want in end-to-end tests
  - We tried using the async_api in order to allow the `DJANGO_ALLOW_ASYNC_UNSAFE` environment variable to be `False`, as recommended
    - Ended up needing `await` on every single line
    - Pretty ugly code was needed to replicate the synchronous behaviour which we required
    - `DJANGO_ALLOW_ASYNC_UNSAFE = True` is acceptable in test cases: https://github.com/microsoft/playwright-python/issues/224
  - If you want tests to run in parallel, Django has another way to achieve this
    - https://docs.djangoproject.com/en/4.1/topics/testing/overview/#running-tests-in-parallel
  - Some use cases for the asynchronous API
    - Web scraping
  - https://playwright.dev/python/docs/api/class-playwright
```
from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright, expect


class BasePlaywrightTestCase(LiveServerTestCase):
  ...
```
Set up
```
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
browser = playwright.chromium.launch()
page = browser.new_page()
page.goto(...)
```
Clean up
```
page.close()
browser.close()
cls.playwright.stop()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "false"
```
#### Manually
https://playwright.dev/python/docs/intro
#### Playwright test generator
- `playwright codegen <your url>`
- `page.pause()`
- Beware of
  - Ambiguous locators
  - Unnecessary code
    - Clicking into input fields first

### Running tests
#### Headed vs headless
- Headed mode opens up a live browser window
  - Debugging
  - Code gen
  - Slow
  - Requires additional software*
```
self.browser = self.playwright.chromium.launch(headless=False)
```
- Headless mode does not open a live browser window
  - Faster
  - Pipeline friendly
```
self.browser = self.playwright.chromium.launch(headless=True)
```
OR 
```
self.browser = self.playwright.chromium.launch()
```
- Configure the mode via an environment variable
#### Static files
- For DERMS, a front-end build was needed in the pipeline
```
docker-compose run front_end npm run build
docker-compose run django ./manage.py test
```
- And `collectstatic` needed to be called within the test cases
```
from django.core.management import call_command

setUpClass(cls):
    ...
    call_command("collectstatic", interactive=False)
```
#### Separation from unit tests
- Prefix all test cases with `e2e_test`

##### Integration tests:
```
./manage.py test --pattern="e2e_test_*.py"
```
##### Unit tests
```
./manage.py test --exclude="e2e_test_*.py"
```

### Playwright in CI
Added two steps to the test stage of our pipeline:
```
- docker-compose run front_end npm run build
- docker-compose run django RUN_PLAYWRIGHT_HEADLESS=True ./manage.py test --pattern="e2e_test*.py"
```
#### Performance
- Running 27 test methods takes around 200 seconds locally
  - Scales quite linearly with the number of tests, so parallelization would become important as more tests are written
- The time varies significantly on the pipeline
- Currently, our pipeline runs in 10-13 minutes with 27 test methods
  - 2-4 minute increase
- There SEEMs to be ways to parallelize tests, however we are yet to do so on DERMS
  - https://docs.djangoproject.com/en/4.1/topics/testing/overview/#speeding-up-the-tests
  - https://playwright.dev/python/docs/test-parallel :(
    - Although parallelization is supported for the Node package


<br><br><br>
<p>*</p>

 The following instructions assume you are using MacOS.
 ##### 1. Install XQuartz. You only need to do this once.
1. Install XQuartz locally by running:
```
brew install --cask xquartz
```
2. Open XQuartz, go to Preferences -> Security, and check "Allow connections from network clients".
3. Restart your machine.
 
4. Open Docker and go to Settings -> Resources -> File sharing, and give access to `/tmp/.X11-unix`. If `/tmp` already has access, this is sufficient.
 ##### 2. Before running the test cases in headed mode, start XQuartz by running:
```
xhost +localhost
```

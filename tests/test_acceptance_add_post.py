# We will continue the test_views_acceptence.py all the way to adding a post, and verify that it appears in homepage. 
import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User

import datetime

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
                         password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=app.run, kwargs={"port": 8080})
        self.process.start()
        time.sleep(1)


    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()
    
    def test_2_add_post (self):
        self.browser.visit("http://127.0.0.1:8080")
        print ("current url = ", self.browser.url)
        
        self.browser.driver.set_window_size(1920, 1080)
        self.browser.click_link_by_text('login')
        print ("current url = ", self.browser.url)
        
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        print (self.browser.url)
        
        add_link=self.browser.find_link_by_partial_text('add')
        add_link.click()
        print (self.browser.url)
        
        title="test_acceptance_add_post"
        self.browser.fill("title", title)
        now=datetime.datetime.now()
        now=str(now)
        self.browser.fill("content", now)
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        print(self.browser.url)
        
        new_post_appears=self.browser.is_text_present(title) and self.browser.is_text_present(now)
        print ("new_post_appears = ", new_post_appears)
        self.assertEqual(new_post_appears, True)

if __name__ == "__main__":
    unittest.main()
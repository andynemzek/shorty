import run
import unittest

class ShortyTestCase(unittest.TestCase):

    def setUp(self):
        run.app.config['TESTING'] = True
        self.app = run.app.test_client()

    def tearDown(self):
        pass

    def test_load_main_page(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b"Shorten your URL" in resp.data)
        self.assertTrue(b"Here's your new url" not in resp.data)
        self.assertTrue(b"url-error" not in resp.data)

    def test_post_main_page(self):
        resp = self.app.post('/', data={"input-url": "http://google.com"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b"Shorten your URL" in resp.data)
        self.assertTrue(b"Here's your new url" in resp.data)
        self.assertTrue(b"url-error" not in resp.data)

    def test_post_main_page_w_error(self):
        resp = self.app.post('/', data={"input-url": "asdf"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b"Shorten your URL" in resp.data)
        self.assertTrue(b"Here's your new url" not in resp.data)
        self.assertTrue(b"url-error" in resp.data)

    def test_short_url_redirect(self):
        url = "http://google.com"
        with run.app.app_context():
            short_url_code = run.store_url(url)
        resp = self.app.get('/' + short_url_code)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, url)

if __name__ == '__main__':
    unittest.main()
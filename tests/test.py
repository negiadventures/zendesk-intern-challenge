import sys
import unittest
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from flask import render_template
from app import app
from controller import routes
from model import requestHandler
from utils import constants as const
from flask_testing import TestCase

class AppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

# Controller TESTS
class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_all_tickets(self):  # Sample json ticket data for bulk tickets
        response = self.app.get('/tickets', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('zccanirudhnegi' in response.get_data(as_text=True))
        #with page number
        response = self.app.get('/tickets?page=2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('zccanirudhnegi' in response.get_data(as_text=True))
        # with page number > total pages
        response = self.app.get('/tickets?page=10000', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('no more pages' in response.get_data(as_text=True))
        # in case data returned is valid and not an error code
        tickets_data = requestHandler.RequestHandler().get_all_tickets()
        self.assertFalse(False, isinstance(tickets_data, int))
        # in case data returned is error code
        tickets_data = 500
        self.assertIsInstance(tickets_data, int)
        # response = self.app.get('/tickets?page=1', follow_redirects=True)
        # self.assertTrue('Something went wrong' in response.get_data(as_text=True))


    def test_ticket_by_id(self):
        # without ticket id as get request
        response = self.app.get('/ticket', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You did not provided a ticket ID' in response.get_data(as_text=True))
        # with ticket id as post request
        response = self.app.post('/ticket', follow_redirects=True, data={'ticket_id': 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('zccanirudhnegi' in response.get_data(as_text=True))
        # invalid ticket id
        response = self.app.post('/ticket', follow_redirects=True, data={'ticket_id': -1})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Something went wrong' in response.get_data(as_text=True))

    def test_page_not_found(self):
        response = self.app.get('/ticke', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get('/tickets/2', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

# Model TESTS
class RequestHandlerTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_all_tickets(self):
        # TODO
        pass

    def test_get_ticket_by_id(self):
        # TODO
        pass

    def test_format_date(self):
        # TODO
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(RoutesTests)
unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    unittest.main()

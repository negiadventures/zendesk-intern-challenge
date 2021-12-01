import sys
import unittest
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from app import app
from model import requestHandler
from utils import constants as const
from unittest.mock import patch, MagicMock
from utils import request_util as req


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

    def test_fetch_all_tickets(self):  # Sample json ticket data for bulk tickets
        response = self.app.get('/tickets', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('zccanirudhnegi' in response.get_data(as_text=True))
        # with page number
        response = self.app.get('/tickets?page=2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('zccanirudhnegi' in response.get_data(as_text=True))
        # with page number > total pages
        response = self.app.get('/tickets?page=10000', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('no more pages' in response.get_data(as_text=True))

    def test_fetch_by_id(self):
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

    @patch('utils.conf.subdomain_url')
    def test_get_all_tickets(self, url):
        # valid case
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response, api=const.api_single_ticket).get_all_tickets()
        self.assertIsInstance(response, dict)
        self.assertTrue('zccanirudhnegi' in str(response))
        # different protocol (http instead of https)
        url.return_value = MagicMock(status_code=200, response='http://zccanirudhnegi.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response).get_all_tickets()
        self.assertIsInstance(response, int)
        self.assertEqual(response, 403)
        # Invalid subdomain
        url.return_value = MagicMock(status_code=200, response='https://invalid_subdomain.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response).get_all_tickets()
        self.assertIsInstance(response, int)
        self.assertEqual(response, 404)
        # invalid api
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response, api="/api/p1/tickets").get_all_tickets()
        self.assertIsInstance(response, int)
        self.assertEqual(response, 404)
        # invalid domain
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendeskks.com')
        response = requestHandler.RequestHandler(url.return_value.response).get_all_tickets()
        self.assertIsInstance(response, int)
        self.assertEqual(response, 500)
        # different port
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com:80')
        response = requestHandler.RequestHandler(url.return_value.response).get_all_tickets()
        self.assertIsInstance(response, int)
        self.assertEqual(response, 500)

    @patch('utils.conf.subdomain_url')
    def test_get_ticket_by_id(self, url):
        # valid case
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response, api=const.api_single_ticket).get_ticket_by_id(ticket_id=1)
        self.assertIsInstance(response, dict)
        self.assertTrue('zccanirudhnegi' in str(response))
        # different protocol (http instead of https)
        url.return_value = MagicMock(status_code=200, response='http://zccanirudhnegi.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response).get_ticket_by_id(1)
        self.assertIsInstance(response, int)
        self.assertEqual(response, 403)
        # Invalid subdomain
        url.return_value = MagicMock(status_code=200, response='https://invalid_subdomain.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response).get_ticket_by_id(1)
        self.assertIsInstance(response, int)
        self.assertEqual(response, 404)
        # invalid api
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = requestHandler.RequestHandler(url.return_value.response, api="/api/v2/ticket/").get_ticket_by_id(1)
        self.assertIsInstance(response, int)
        self.assertEqual(response, 404)
        # invalid domain
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendeskks.com')
        response = requestHandler.RequestHandler(url.return_value.response).get_ticket_by_id(1)
        self.assertIsInstance(response, int)
        self.assertEqual(response, 500)
        # different port
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com:80')
        response = requestHandler.RequestHandler(url.return_value.response).get_ticket_by_id(1)
        self.assertIsInstance(response, int)
        self.assertEqual(response, 500)
        # invalid id
        response = requestHandler.RequestHandler().get_ticket_by_id(-100)
        self.assertEqual(response, 500)

    def test_format_date(self):
        date = requestHandler.RequestHandler().format_date('2021-12-01T01:30:56Z')
        self.assertEqual(date, '2021-12-01 01:30:56')


# rest_util TESTS
class RequestTests(unittest.TestCase):
    @patch('utils.conf.subdomain_url')
    def test_get(self, url):
        # valid case
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = req.Request().get(url=url.return_value.response + "/api/v2/tickets.json")
        self.assertIsInstance(response, dict)
        self.assertTrue('zccanirudhnegi' in str(response))
        # invalid token
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = req.Request(api_token='DUMMY_TOKEN').get(url=url.return_value.response + "/api/v2/tickets.json")
        self.assertIsInstance(response, int)
        self.assertEqual(response, 401)
        # invalid login_id
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = req.Request(login_id='DUMMY_LOGIN_ID').get(url=url.return_value.response + "/api/v2/tickets.json")
        self.assertIsInstance(response, int)
        self.assertEqual(response, 401)
        # different protocol
        url.return_value = MagicMock(status_code=200, response='http://zccanirudhnegi.zendesk.com')
        response = req.Request().get(url=url.return_value.response + "/api/v2/tickets.json")
        self.assertIsInstance(response, int)
        self.assertEqual(response, 403)
        # Invalid subdomain
        url.return_value = MagicMock(status_code=200, response='https://invalid_subdomain.zendesk.com')
        response = req.Request().get(url=url.return_value.response + "/api/v2/tickets.json")
        self.assertIsInstance(response, int)
        self.assertEqual(response, 404)
        # invalid api
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com')
        response = req.Request().get(url=url.return_value.response + "/api/v2/ticketsss.json")
        self.assertIsInstance(response, int)
        self.assertEqual(response, 404)
        # invalid domain
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendeskks.com')
        response = req.Request().get(url=url.return_value.response + "/api/v2/tickets.json")
        self.assertIsInstance(response, int)
        self.assertEqual(response, 500)
        # different port
        url.return_value = MagicMock(status_code=200, response='https://zccanirudhnegi.zendesk.com:80')
        response = req.Request().get(url=url.return_value.response + "/api/v2/tickets.json")
        self.assertIsInstance(response, int)
        self.assertEqual(response, 500)


suite = unittest.TestLoader().loadTestsFromTestCase(RoutesTests)
unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    unittest.main()

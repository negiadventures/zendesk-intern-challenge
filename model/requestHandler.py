import datetime

from utils import constants, conf
from utils.request_util import Request


class RequestHandler:
    def __init__(self):
        self.url = conf.subdomain_url
        self.data = {}

    def get_all_tickets(self):
        '''
        This method fetches all the tickets from Zendesk API for a user.
        :return: all tickets info in the account or error code in case of failure
        '''
        response = Request().get(url=self.url + "/api/v2/tickets.json")
        self.data = response
        if isinstance(self.data, int):
            return self.data
        next_page = []  # single API call reads only 100 tickets we use next page URL to fetch all the tickets
        while self.data["next_page"] is not None and self.data["next_page"] not in next_page:
            new_url = self.data["next_page"]
            next_page.append(new_url)
            response = Request().get(url=new_url)
            new_data = response
            self.data["tickets"].extend(new_data["tickets"])
        for i in range(len(self.data["tickets"])):
            self.data["tickets"][i]["created_at"] = self.format_date(self.data['tickets'][i]['created_at'])
            self.data["tickets"][i]["updated_at"] = self.format_date(self.data['tickets'][i]['updated_at'])
        return self.data

    # Method to get one ticket details from API and return it, or return appropriate error value
    def get_ticket_by_id(self, ticket_id):
        '''
        This method fetches a single ticket from Zendesk API for a user.
        :param ticket_id: ID of the ticket to retrieve.
        :return: ticket info for which id was passed or error code in case of failure
        '''
        response = Request().get(url=self.url + "/api/v2/tickets/" + str(ticket_id) + ".json")
        self.data = response
        if isinstance(self.data, int):
            return self.data
        self.data["ticket"]["created_at"] = self.format_date(self.data['ticket']['created_at'])
        self.data["ticket"]["updated_at"] = self.format_date(self.data['ticket']['updated_at'])
        return self.data

    def format_date(self, date):
        '''
        This method formats the date in the required format
        :param date: date to be formatted
        :return: formatted date
        '''
        return str(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"))

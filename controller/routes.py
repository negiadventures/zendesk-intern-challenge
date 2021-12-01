from flask import request, render_template, Blueprint
import math
import utils.constants as const
from model.requestHandler import RequestHandler

urls = Blueprint('home_urls', __name__, )


@urls.route('/')
def home():
    '''
    :return: View for home page
    '''
    return render_template('home.html')


@urls.route('/tickets')
def fetch_all_tickets():
    '''
    This method calls get_all_tickets() methods to fetch all tickets from zendesk api and renders data in the view, or renders error page in case of error.
    :param :page Accepts optional page parameter (defaults 1) to display a specific page (Each page contains 25 tickets)
    :return: View for All Tickets page displaying list of all tickets or an Error page displaying the error.
    '''
    tickets_data = RequestHandler().get_all_tickets()
    if isinstance(tickets_data, int):
        return render_template('error.html', message=const.error_messages[str(tickets_data)])
    page_num = request.args.get('page')
    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)
    total_page_num = math.ceil(len(tickets_data['tickets'])/const.page_size)
    if page_num > total_page_num:
        return render_template('error.html', message=const.error_messages['ERR_NO_MORE_PAGES'])
    start_ticket_num = (page_num * const.page_size) - const.page_size
    end_ticket_num = start_ticket_num + const.page_size
    tickets_data['tickets'] = tickets_data['tickets'][start_ticket_num:end_ticket_num]
    return render_template('tickets.html', data=tickets_data, page_num=page_num, total_pages = total_page_num)


@urls.route('/ticket', defaults={'ticket_id': None}, methods=["POST","GET"])
@urls.route('/ticket/<ticket_id>', methods=["GET"])
def fetch_ticket_by_id(ticket_id):
    '''
    This method calls get_ticket_by_id method to fetch data for the ticket and renders data in the view, or renders error page in case of error.
    :param ticket_id: Ticket ID of the ticket to be displayed
    :return: view for single ticket info or an error page displaying the error message
    '''
    if request.method == "POST":
        ticket_id = request.form['ticket_id']
    if ticket_id is None:
        return render_template('error.html', message=const.error_messages['ERR_NO_TICKET_ID'])
    ticket_data = RequestHandler().get_ticket_by_id(ticket_id)
    if isinstance(ticket_data, int):
        return render_template('error.html', message=const.error_messages[str(ticket_data)])
    return render_template('ticket.html', data=ticket_data)


@urls.errorhandler(404)
def page_not_found(e):
    '''
    This method renders error page in case of invalid request by the client.
    :param e: error message
    :return: View for error page
    '''
    return render_template('error.html', message=const.error_messages['ERR_PAGE_NOT_FOUND']),404
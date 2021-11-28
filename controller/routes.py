from flask import request, render_template, Blueprint

import utils.constants as const
from model.requestHandler import RequestHandler

urls = Blueprint('home_urls', __name__, )


@urls.route('/')
def home():
    return render_template('home.html')


@urls.route('/tickets')
def get_all_tickets():
    tickets_data = RequestHandler().get_all_tickets()
    return render_template('tickets.html', data=tickets_data)


@urls.route('/ticket', defaults={'ticket_id': None}, methods=["POST","GET"])
@urls.route('/ticket/<ticket_id>', methods=["GET"])
def get_ticket_by_id(ticket_id):
    if request.method == "POST":
        ticket_id = request.form['ticket_id']
    if ticket_id is None:
        return render_template('error.html', message=const.error_messages['ERR_NO_TICKET_ID'])
    ticket_data = RequestHandler().get_ticket_by_id(ticket_id)
    return render_template('ticket.html', data=ticket_data)


@urls.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message=const.error_messages['ERR_PAGE_NOT_FOUND']),404
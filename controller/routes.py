from flask import request, render_template, Blueprint

urls = Blueprint('home_urls', __name__, )


@urls.route('/')
def home():
    return render_template('home.html')


@urls.route('/tickets')
def get_all_tickets():
    tickets_data = {}
    return render_template('tickets.html', data=tickets_data)


@urls.route('/ticket', defaults={'ticket_id': None}, methods=["POST"])
@urls.route('/ticket/<ticket_id>', methods=["GET"])
def get_ticket_by_id(ticket_id):
    if request.method == "POST":
        ticket_id = request.form['ticket_id']
    ticket_data={}
    return render_template('ticket.html', data=ticket_data)

# Error messages with error codes
# TODO: Update error messages for respective codes
error_messages = {
    'ERR_PAGE_NOT_FOUND': 'What you were looking for is just not there.',
    'ERR_NO_MORE_PAGES': 'Sorry, no more pages. Please go back where you left of.',
    'ERR_NO_TICKET_ID': 'Sorry, You did not provided a ticket ID. Please try again with a valid ticket ID.',
    '401': 'Something went wrong! Please try again.',
    '403': 'Something went wrong! Please try again.',
    '404': 'Something went wrong! Please try again.',
    '500': 'Something went wrong! Please try again.',
    '503': 'Something went wrong! Please try again.'
}

page_size = 25
api_all_tickets = "/api/v2/tickets.json"
api_single_ticket = "/api/v2/tickets/"
format_json = ".json"
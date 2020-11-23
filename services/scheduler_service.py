from extensions import scheduler
from models.order import Order
from models.ticket import Ticket
from services import square_service

global app


@scheduler.task('interval', id='process_transactions', minutes=5, misfire_grace_time=900)
def process_transactions():
    print('Running Process Transactions')
    global app

    # Get a list of orders that have a payment status of PENDING
    with app.app_context():
        pending_orders = Order.query.filter_by(payment_status='PENDING').all()
        for order in pending_orders:
            # Get order details from square
            details = square_service.get_transaction(order)
            if details['success'] is not True:
                print(f"Error processing transaction: {details['errors'][0]}")
                continue
            else:
                print(f"Successfully fetched order details for order {order.id}")
                print(details['order_details'])

            # Update our order record
            details = details['order_details']
            order.square_order_id = details['id']
            order.payment_status = details['state']
            order.order_total = details['total_money']['amount'] / 100
            order.user_id = int(details['customer_id'])
            order.update()

            # If the order payment is marked as COMPLETED, create ticket records
            if order.payment_status == 'COMPLETED':
                for item in details['line_items']:
                    # Use the quantity field to determine how many tickets to create
                    for x in range(int(item['quantity'])):
                        ticket = Ticket()
                        ticket.user_id = order.user_id
                        ticket.active = True
                        ticket.item_id = item['metadata']['item_id']
                        ticket.order_id = order.id
                        ticket.update()


def init_scheduler_service(application):
    print("Scheduler service is running")
    global app
    app = application

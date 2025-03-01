from top1phsmm.api import top1phsmm
from top1phsmm.api import Autmate
from mahdix import *
darkblue = "\033[34m"
red = "\033[1;31m"
hotpink = "\033[38;5;197m"
from threading import Thread
from concurrent.futures import ThreadPoolExecutor as thd
import requests

# Initialize classes
connect = top1phsmm(api_key='lfqctrg88akz3oamcd1uae9j1rtph1qz1ano87m24gthyzsg6cx2ds4yjfnqxqi1')
connect_automate = Autmate()

order_delev_list = []  # List to track processed orders

# Method to process each order
def submit(token, post_url, order_id):
    url = 'https://graph.facebook.com/v13.0/me/feed'
    datas = {
        'link': post_url,
        'published': '0',
        'privacy': '{"value":"SELF"}',
        'access_token': token
    }
    try:
        res = requests.post(url, data=datas, headers={  # Posting to Facebook
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'connection': 'keep-alive',
            'content-length': '0',
            'host': 'graph.facebook.com'
        }).json()
        if res.get('id'):
            order_delev_list.append(order_id)  # Add successful submission to list
            count_of_2 = order_delev_list.count(order_id)
            print(f'\033[1;31m[\033[1;31m{order_id}\033[1;31m]\033[1;34m Currently Sharing\033[1;35m [{count_of_2}] \033[1;31m\n', end='\r')
    except Exception as e:
        print(f"Error submitting order: {e}")


# Simulate reading from file
my_cookes = list(open('input_file.txt', 'r', encoding='utf-8').read().splitlines())
print(f'Total accounts: {len(my_cookes)}')

def process_orders():
    print("Checking for new orders on \033[1;31m[TOP1PHSMM.COM]")  # Print each time we are checking for new orders
    get_orders = connect.get_orders()

    if get_orders:  # If there are orders, process them
        new_order_found = False  # Flag to check if we found any new orders
        for order in get_orders:
            service_id = order['service_id']
            quantity = order['quantity']
            order_link = order['link']
            order_id = order['id']
            status = order['status']

            # Skip orders that are already completed or being processed
            if status == 'completed' or order_id in order_delev_list:
                continue

            # Only process orders with specific service_ids (1204, 1199, 1229)
            if service_id in [1204, 1199, 1229] and status == 'pending':  # Processing when the order status is 'pending'
                new_order_found = True  # Mark that we found a new order
                order_delev_list.append(order_id)
                # Update status to "In Progress"
                connect.update_order_status(order_id, status='In Progress')  
                print(f"Processing Order ID: {order_id}")
                        
                if '/share/' in order_link:
                    retx = requests.get(order_link, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate',
                    }, allow_redirects=True)
                    order_link = retx.url

                # Track deliveries and ensure the number of deliveries does not exceed the quantity
                while order_delev_list.count(order_id) < quantity:
                    for cokis in my_cookes:
                        token = cokis.split('|')[1]
                        count_of_2 = order_delev_list.count(order_id)

                        # Stop if we've reached the target quantity (exact match)
                        if count_of_2 + 702 >= quantity:
                            print(f"Order {order_id} is completed!")
                            connect.set_orders_completed(order_id)
                            break  # Exit loop once the order is completed

                        elif count_of_2 < quantity:
                            try:
                                thdes = Thread(target=submit, args=(token, order_link, order_id,))
                                thdes.start()  # Start a new thread to submit
                            except Exception as e:
                                print(f"Error starting thread: {e}")
                else:
                    print(f"Skipping order {order_id} due to invalid service_id or link.")
        if not new_order_found:
            print("\033[90mNo New Pending Orders Yet Every 10 Second Checking\033[0m")  # Print message if no new orders found

# Running the main method periodically
while True:
    process_orders()
    time.sleep(10)  # Wait 10 seconds before checking again

import requests
import json
from threading import Thread
import time

class top1phsmm:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_key_V2 = 'rfiecqd5p0ucagww27epdswm6n5jymd8jac30ucns4ux1xc713mdzynr6iyh3zfo'  # Replace with your correct API key
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }

    def update_order_link(self, orderID, text='Order is Done Successfully!'):
        return requests.post(
            f'https://top1phsmm.com/adminapi/v2/orders/{orderID}/edit-link',
            headers=self.headers,
            json={'link': text}
        ).text

    def update_order_status(self, orderID, status='In Progress'):
        url = "https://top1phsmm.com/adminapi/v1"
        data = {
            "key": self.api_key_V2,
            "action": "setInprogress",  # This should set the status to "In Progress"
            "id": orderID
        }
        try:
            response = requests.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                print(f"Order {orderID} status updated to In Progress.")
            else:
                print(f"Failed to update order status. HTTP Status Code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while updating the order status: {e}")

    def set_orders_completed(self, orderID):
        url = "https://top1phsmm.com/adminapi/v1"
        data = {
            "key": self.api_key_V2,
            "action": "setCompleted",  # Action to mark the order as completed
            "id": orderID
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                print(f"Order {orderID} marked as Completed.")
            else:
                print(f"Failed to set order as completed. HTTP Status Code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while marking the order as completed: {e}")

    def get_orders(self):
        try:
            response = requests.get('https://top1phsmm.com/adminapi/v2/orders', headers=self.headers)
            if response.status_code == 200:
                response_data = response.json()  # Parse the response as JSON
                if 'data' in response_data and 'list' in response_data['data']:
                    return response_data['data']['list']  # Return list of orders
                else:
                    return []  # If no orders or data key missing
            else:
                return []  # If request failed, return empty list
        except Exception as e:
            print(f"An error occurred while fetching orders: {e}")
            return []


class Automate:
    def __init__(self):
        pass

    def submit(self, token, post_url, order_id):
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
                return True
            return False
        except Exception as e:
            print(f"Error submitting post: {e}")
            return False
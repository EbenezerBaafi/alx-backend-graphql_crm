#!/usr/bin/env python
"""
Django-integrated script to send order reminders for pending orders.
This version uses Django ORM directly instead of GraphQL queries.
Recommended for better performance and reliability.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Set up Django environment
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Order

# Configuration
LOG_FILE = "/tmp/order_reminders_log.txt"


def get_pending_orders():
    """
    Get orders from the last 7 days using Django ORM.
    """
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    orders = Order.objects.filter(
        order_date__gte=seven_days_ago
    ).select_related('customer').prefetch_related('products')
    
    return orders


def log_order_reminder(order_id, customer_email, timestamp):
    """
    Log order reminder to file.
    """
    log_entry = f"[{timestamp}] Order ID: {order_id}, Customer Email: {customer_email}\n"
    
    try:
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}", file=sys.stderr)


def process_orders(orders):
    """
    Process orders and log reminders.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    processed_count = 0
    
    if not orders.exists():
        log_message = f"[{timestamp}] No pending orders found in the last 7 days\n"
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_message)
        return 0
    
    for order in orders:
        order_id = str(order.id)
        customer_email = order.customer.email
        
        log_order_reminder(order_id, customer_email, timestamp)
        processed_count += 1
    
    return processed_count


def main():
    """
    Main function to run the order reminder process.
    """
    try:
        print("Fetching pending orders from database...")
        
        # Get orders from last 7 days
        orders = get_pending_orders()
        
        # Process and log orders
        count = process_orders(orders)
        
        print(f"Order reminders processed! ({count} orders)")
        
        return 0
    
    except Exception as e:
        print(f"Error processing order reminders: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

    # from gql import", "gql", "Client
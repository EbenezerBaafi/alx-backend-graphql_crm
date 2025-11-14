#!/bin/bash

# Script to clean up inactive customers (no orders in the last year)
# This script should be run via cron job

# Set the project directory (adjust this to your actual project path)
PROJECT_DIR="/path/to/your/alx_backend_graphql"
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Change to project directory
cd "$PROJECT_DIR" || exit 1

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Python command to delete inactive customers
PYTHON_COMMAND="
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders in the last year
# Customers with no orders at all OR customers whose last order is older than a year
inactive_customers = Customer.objects.filter(
    orders__isnull=True
) | Customer.objects.exclude(
    orders__order_date__gte=one_year_ago
).distinct()

# Count before deletion
count = inactive_customers.count()

# Delete inactive customers
if count > 0:
    inactive_customers.delete()
    print(f'{count}')
else:
    print('0')
"

# Execute the Python command and capture output
DELETED_COUNT=$(python manage.py shell -c "$PYTHON_COMMAND" 2>&1 | tail -n 1)

# Log the result
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"

# Optional: Print to console as well
echo "[$TIMESTAMP] Customer cleanup completed. Deleted: $DELETED_COUNT customers"

# Exit successfully
exit 0
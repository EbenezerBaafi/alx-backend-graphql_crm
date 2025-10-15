import django_filters
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """
    Filter class for Customer model with advanced filtering options.
    """
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    # Case-insensitive partial match for email
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    # Date range filters for created_at
    created_at__gte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_at__lte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    # Custom filter for phone number pattern (starts with specific prefix)
    phone_pattern = django_filters.CharFilter(
        field_name='phone',
        lookup_expr='startswith'
    )
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'created_at']


class ProductFilter(django_filters.FilterSet):
    """
    Filter class for Product model with price and stock filtering.
    """
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    # Price range filters
    price__gte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    price__lte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )
    
    # Stock range filters
    stock__gte = django_filters.NumberFilter(
        field_name='stock',
        lookup_expr='gte'
    )
    stock__lte = django_filters.NumberFilter(
        field_name='stock',
        lookup_expr='lte'
    )
    
    # Exact match for stock
    stock = django_filters.NumberFilter()
    
    # Custom filter for low stock products (stock < 10)
    low_stock = django_filters.BooleanFilter(
        method='filter_low_stock',
        label='Low Stock (less than 10)'
    )
    
    def filter_low_stock(self, queryset, name, value):
        """
        Custom method to filter products with low stock (< 10).
        """
        if value:
            return queryset.filter(stock__lt=10)
        return queryset
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']


class OrderFilter(django_filters.FilterSet):
    """
    Filter class for Order model with related field lookups.
    """
    # Total amount range filters
    total_amount__gte = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='gte'
    )
    total_amount__lte = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='lte'
    )
    
    # Order date range filters
    order_date__gte = django_filters.DateTimeFilter(
        field_name='order_date',
        lookup_expr='gte'
    )
    order_date__lte = django_filters.DateTimeFilter(
        field_name='order_date',
        lookup_expr='lte'
    )
    
    # Filter by customer name (related field lookup)
    customer_name = django_filters.CharFilter(
        field_name='customer__name',
        lookup_expr='icontains'
    )
    
    # Filter by product name (related field lookup through many-to-many)
    product_name = django_filters.CharFilter(
        field_name='products__name',
        lookup_expr='icontains',
        distinct=True  # Avoid duplicate results
    )
    
    # Filter orders that include a specific product ID
    product_id = django_filters.NumberFilter(
        field_name='products__id',
        distinct=True
    )
    
    class Meta:
        model = Order
        fields = ['total_amount', 'order_date', 'customer']
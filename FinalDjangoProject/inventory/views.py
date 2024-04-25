from django.shortcuts import render
from django.core.paginator import Paginator

def show_inventory(request):
    equipments = [
        {'device_name': 'Laptop', 'device_type': 'Portable', 'serial_number': '12345', 'cpu': 'Intel i7', 'availability': 'Available'},
        {'device_name': 'Desktop', 'device_type': 'Stationary', 'serial_number': '67890', 'cpu': 'AMD Ryzen 7', 'availability': 'Unavailable'},
    ]
    for i in range(2, 40):
        equipments.append({
            'device_name': f'Product {i}',
            'device_type': f'Device Type {i}',
            'serial_number': f'Serial {i}',
            'cpu': f'CPU {i}',
            'availability': 'Available' if i % 2 == 0 else 'Unavailable'
        })

    paginator = Paginator(equipments, 10)  # 10 equipments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/admin-itemlist.html', {'page_obj': page_obj})

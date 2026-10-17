from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from .db import call_function, call_procedure

def products_list(request):
    rows, _ = call_procedure('sp_products_list', [], fetch=True)
    products = [
        {'id': r[0], 'name': r[1], 'category': r[2],
         'price': r[3], 'stock': r[4]}
        for r in rows
    ]
    return render(request, 'products_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        name        = request.POST['name']
        category_id = int(request.POST['category_id'])
        price       = float(request.POST['price'])
        stock       = int(request.POST['stock'])

       
        with connection.cursor() as cursor:
            cursor.execute(
                "CALL sp_product_add(%s, %s, %s, %s, @new_id)",
                [name, category_id, price, stock]
            )
            
            cursor.execute("SELECT @new_id")
            result = cursor.fetchone()
            
            new_id = result[0] if result else None

        messages.success(request, f'Товар #{new_id} добавлен')
        return redirect('products_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT category_id, name FROM categories ORDER BY name")
        raw_categories = cursor.fetchall()
        
        categories = [{'id': row[0], 'name': row[1]} for row in raw_categories]

    return render(request, 'product_add.html', {'categories': categories})

def order_create(request):
    if request.method == 'POST':
        customer_id = int(request.POST['customer_id'])
        _, out = call_procedure(
            'sp_order_create',
            [customer_id],
            out_count=1,
            fetch=False,
        )
        order_id = out[0]
        messages.success(request, f'Заказ #{order_id} создан')
        return redirect('customer_orders', pk=customer_id)

    return render(request, 'order_create.html')

def call_procedure(proc_name, args=None, out_count=0, fetch=False):
    if args is None:
        args = []
        
    with connection.cursor() as cursor:
        proc_args = cursor.callproc(proc_name, args)
        
        out_values = proc_args[-out_count:] if out_count > 0 else []
        
        rows = []
        if fetch:
            if hasattr(cursor.cursor, 'stored_results'):
                for result in cursor.cursor.stored_results():
                    rows = result.fetchall()
            else:
                rows = cursor.fetchall()
                
        return rows, out_values


def discount_view(request):
    result = None
    if request.method == 'POST':
        customer_id = int(request.POST['customer_id'])
        amount      = float(request.POST['amount'])
        percent     = call_function('fn_customer_discount', [customer_id, amount])
        total       = amount * (1 - percent / 100)
        result = {
            'customer_id': customer_id,
            'amount': amount,
            'percent': percent,
            'total': round(total, 2),
        }
    return render(request, 'discount.html', {'result': result})

def product_update_price(request, pk):
    if request.method == 'POST':
        new_price = request.POST.get('price')
        
        if new_price:
            with connection.cursor() as cursor:
                cursor.callproc('sp_product_update_price', [pk, new_price])
            
            return redirect('products_list') 
            
    return render(request, 'product_upd_price.html', {'product_id': pk})

def customer_orders(request, pk):
    with connection.cursor() as cursor:
        cursor.callproc('sp_customer_orders', [pk])
        
        raw_orders = cursor.fetchall()
        orders = []
        for row in raw_orders:
            orders.append({
                'id': row[0],
                'date': row[1],
                'total_amount': row[2],
                'avg_check': row[3]
            })

    context = {
        'orders': orders,
        'customer_id': pk
    }
    return render(request, 'customer_orders.html', context)

def category_stats(request):
    with connection.cursor() as cursor:
        cursor.callproc('sp_category_stats')        
        raw_stats = cursor.fetchall()        
        categories = []
        max_revenue = 0.0
                
        for row in raw_stats:
            revenue = float(row[3]) if row[3] is not None else 0.0            
            if revenue > max_revenue:
                max_revenue = revenue                
            categories.append({
                'name': row[0],
                'products_count': row[1],
                'units_sold': row[2],
                'revenue': row[3],
                'is_top': False
            })
        if max_revenue > 0:
            for cat in categories:
                cat_revenue = float(cat['revenue']) if cat['revenue'] is not None else 0.0
                if cat_revenue == max_revenue:
                    cat['is_top'] = True
    return render(request, 'category_stats.html', {'categories': categories})
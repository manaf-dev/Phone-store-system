from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import ListView


from .forms import *
from .models import *


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'store/dashboard.html')

# def sales(request):
#     return render(request, 'store/sales.html')

@login_required
def place_order(request):
    if request.method == 'POST':
        form =  OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            quantity = form.cleaned_data['quantity']
            product_id = form.cleaned_data['product'].productid
            tel = form.cleaned_data['tel']
            paymode = form.cleaned_data['paymode']

            customer = Customer.objects.create(
                name=name, 
                address=address, 
                phone=tel, 
                gender=gender
                )
            
            Product.objects.filter(productid=product_id).update(quantityInStock=F('quantityInStock') - quantity)
            product = Product.objects.get(productid=product_id)
            unit_price = product.price
            #product.update_stock(quantity)   #updating the quantity in stock with the order quantity

            invoice = Invoice.objects.create(
                user=request.user, 
                pay_mode=paymode, 
                amount=(unit_price * int(quantity))
                )
            
            invoice = invoice.id
            order = Order.create_order(invoice, customer)
            
            order_id = Order.objects.latest('id')
            orderDetail = OrderDetail.objects.create(
                orderID = order_id, 
                productID = product, 
                quantity = quantity
                )
        
            messages.success(request, 'Your order has been placed!')
            return redirect(receipt, pk=orderDetail.pk)

    form = OrderForm()
    context = {'form':form}
    return render(request, 'store/place_order.html', context)


@login_required
def receipt(request, pk):
    orderdetail = get_object_or_404(OrderDetail, pk=pk)
    context={'orderdetail' : orderdetail }
    return render (request,'store/receipt.html',context)



@login_required
def add_product(request):
    if request.method == 'POST':
        form =AddProductForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['productid']
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            type = form.cleaned_data['product_type']
            brand = form.cleaned_data['brand']
            quantity = form.cleaned_data['quantity']

            Product.objects.create(
                productid = product_id,
                name = name,
                price = price,
                type = type,
                brand = brand,
                quantityInStock = quantity
            )
            messages.success(request, f'You have added {name} to product stock!')
            return redirect('add_product')

    form = AddProductForm()
    context = {'form':form}
    return render(request, 'store/add_product.html', context)

# @login_required
class SalesList(ListView):
    model = OrderDetail
    context_object_name = 'orderdetails'
    template_name = 'store/sales.html'

#replaced function view with class-based list view
# def view_sales(request):
#    orderdetails = OrderDetail.objects.all()
#    context = {'orderdetails': orderdetails}
#    return render(request , 'store/sales.html', context)

@login_required
def view_customers(request):
    form = SearchCustomerForm(request.GET)
    customers = Customer.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        customers = Customer.objects.filter(
            Q(id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(phone__icontains=search_query)
            ).distinct().order_by('-id')

    context = {'form':form, 'customers':customers}
    return render(request, 'store/customers.html', context)

@login_required
def view_products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/products.html', context)

@login_required
def add_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']
            Customer.objects.create(
                name=name,
                address=address,
                phone=phone,
                gender=gender
            )
            messages.success(request, f'You have added {name} to the customers!')
            return redirect('add_customer')
    context = {'form':form}
    return render(request, 'store/add_customer.html', context)

@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'You have deleted {customer.name} from the customers!')
        return redirect('view_customers')
    context = {'customer':customer}
    return render(request, 'store/delete_customer.html')
    
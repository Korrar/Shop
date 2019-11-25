from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import *
from .models import *
import datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
import schedule



def invoice(order):
    os.environ["INVOICE_LANG"] = "en"

    info = UserAddress.objects.get(user=order.client)
    info_seller = UserAddress.objects.get(user=User.objects.get(username='Seller'))
    client = Client('{}'.format(info.company_name), '{} {}'.format(info.home_number, info.local_number),'{} {}'.format(info.post, info.city))
    provider = Provider('{}'.format(info_seller.company_name), '{} {}'.format(info_seller.home_number, info_seller.local_number),'{} {}'.format(info_seller.post, info_seller.city),bank_account='00000', bank_code='0000')
    creator = Creator('Shop')

    invoice = Invoice(client, provider, creator)
    invoice.currency_locale = 'en_US.UTF-8'
    for item in order.product_list.product_list.all():
        invoice.add_item(Item('{}'.format(item.amount), '{}'.format(item.product.price), description="{}".format(item.product.name)))

    pdf = SimpleInvoice(invoice)
    pdf.gen("pro-forma.pdf")



def home(request):

    form = RegisterForm(request.POST or None)

    if 'Submit' in request.POST and request.method == "POST":
        if form.is_valid():
            form.save()
            cart = Cart()
            cart.user = User.objects.get(username=form.cleaned_data['username'])
            cart.save()
        return redirect('/')

    if 'logout' in request.POST and request.method == 'POST':
        logout(request)
        return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'home.html', context)





@login_required
def cart_view(request):
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    user = User.objects.get(username=request.user)
    cart = Cart.objects.filter(user=user)

    if request.method == 'POST' and 'order' in request.POST:
        cart_one = Cart.objects.get(user=User.objects.get(username=request.user))
        if cart_one.product_list.exists():
            sum_price = 0
            for item in cart_one.product_list.all():
                sum_price = sum_price + (item.product.price * item.amount)
            order = Order()
            order.product_list = cart_one
            order.enter_date = today
            order.client = User.objects.get(username=request.user)
            order.payment_deadline = next_week
            order.summary_price = sum_price
            order.save()
            invoice(order)
            email = EmailMessage(
                'Order number {}'.format(order.pk),
                'Confirmation of your order',
                'someemail4567@gmail.com',
                ['{}'.format(user.email)],
            )
            email.attach_file('pro-forma.pdf')
            email.send()

            cart_one.product_list.all().delete()
            messages.add_message(request, messages.INFO,
                                 'Your order was created')
        else:
            messages.add_message(request, messages.ERROR,
                                 'You do not have anything in the cart')

    if 'remove' in request.POST and request.method == 'POST':
        your_cart = Cart.objects.get(user=request.user)
        your_cart.product_list.remove(Amount.objects.get(pk=request.POST.get('remove')))
        messages.add_message(request, messages.INFO,
                             'Product removed from shopping cart')

    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)


def main_view(request):
    product = Product.objects.all()
    query = request.GET.get('query')
    if query:
        product = Product.objects.filter(Q(name__icontains=query)|Q(producer__icontains=query))
    paginator = Paginator(product, 4)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    form_add = AmountForm(request.POST or None)

    if 'add' in request.POST and request.method == 'POST':
        if form_add.is_valid():
            form_add.save(commit=False)
            object_amount = Amount()
            obj_prod = Product.objects.get(name=request.POST.get('add'))
            object_amount.product = obj_prod
            object_amount.amount = form_add.cleaned_data['amount']
            object_amount.save()
            your_cart = Cart.objects.get(user=request.user)
            your_cart.product_list.add(object_amount)
            messages.add_message(request, messages.INFO,
                                 'Product {} added to shopping cart'.format(obj_prod.name))

    form_prod = ProductForm(request.POST or None, request.FILES or None)

    if 'save_prod' in request.POST and request.method == 'POST':
        if form_prod.is_valid():
            form_prod.save()
        return redirect('/list/')

    if 'edit' in request.POST and request.method == 'POST':
        return redirect('/edit/{}/'.format(request.POST.get('edit')))

    if 'delete' in request.POST and request.method == 'POST':
        product = Product.objects.get(name=request.POST.get('delete'))
        if request.POST.get('delete'):
            product.delete()
        messages.add_message(request, messages.INFO,
                             'Object deleted succesfuly')
        return redirect('/list/')

    context = {
        'product': products,
        'form': form_add,
        'form2': form_prod,
    }
    return render(request, 'main_page.html', context)


def edit_view(request,name):

    form = ProductFormEdit(request.POST or None, request.FILES or None, instance=Product.objects.get(name=name))

    if request.method == 'POST' and 'save' in request.POST:
        if form.is_valid():
            form.save()
        return redirect('/list/')
    context = {
        'form': form,
    }
    return render(request, 'edit.html', context)

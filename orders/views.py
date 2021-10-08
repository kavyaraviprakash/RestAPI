from django.urls import reverse
from django.shortcuts import render, redirect
from xhtml2pdf import pisa
import orders.models
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings
from django.template.loader import render_to_string, get_template
from shop.models import *
import os
from django.http import HttpResponse


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
        "order_{}.pdf"'.format(order.id)
    # weasyprint.HTML(string=html).write_pdf(response,
    #                                        stylesheets=[weasyprint.CSS(
    #                                            settings.STATIC_ROOT + 'css/pdf.css')])
    return response


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            user = request.user
            order.user = user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


def order_list(request):
    currest_user=request.user
    orders=Order.objects.filter(user=currest_user.id)
    return render(request, 'orders/order/order_list.html', {'orders':orders})


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/order_details.html',{'order': order})


def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # template=get_template('orders/order/pdf.html')
    template_path='orders/order/pdf.html'
    context={'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Invoice.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=order_list)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

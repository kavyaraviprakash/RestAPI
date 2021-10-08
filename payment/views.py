import braintree
from django.shortcuts import render, redirect, get_object_or_404
import orders.forms
from orders.models import Order
from twilio.rest import Client
import os
from django.template.loader import render_to_string
from io import BytesIO
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from orders.forms import *


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            subject = f'order {order_id}'
            message = f"Your order no {order_id}, with items costing ${order.get_total_cost()}, has been placed " \
                      f"successfully."
            # email_attach('order_{}.pdf'.format(order.id),out.getvalue(),'application/pdf')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [order.email]
            send_mail(subject, message, email_from, recipient_list)
            account_sid = 'AC0ab33b13cd68b454672c784a39ae95f7'
            auth_token = '97fe7e2f4b5bbcb052a892de760eaf71'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body='Hi, Thank you for shopping at e-buy,your order has been placed and we will deliver you asap.',
                from_='+14083530568',
                to='+14022150853'
            )

            print(message.sid)

            # create invoice e-mail
            #             subject = 'Fun for Kids Store - Invoice no. {}'.format(order.id)
            #             message = 'Thank you for shopping at Fun for Kids. Your total bill card to CC is.'
            #             email = EmailMessage(subject,
            #                                  message,
            #                                  'admin@myshop.com',
            #                                  [order.email])
            #             # generate PDF
            # #            html = render_to_string('orders/order/pdf.html', {'order': order})
            # #            out = BytesIO()
            # #            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            # #            weasyprint.HTML(string=html).write_pdf(out,
            # #                                                  stylesheets=stylesheets)
            #             # attach PDF file
            # #            email.attach('order_{}.pdf'.format(order.id),
            # #                         out.getvalue(),
            # #                         'application/pdf')
            #             # send e-mail
            #             email.send()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

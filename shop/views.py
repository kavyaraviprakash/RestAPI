from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Category, Product, User, Currency
from cart.forms import CartAddProductForm
from .forms import *
import requests
import json
import pycountry
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAdminUser
from orders.models import Order


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # initialize currency as Euro
    selected_country = "DE"
    country_form = CountryForm()

    # pull selected country
    if request.method == 'POST':
        selected_country = request.POST['selectedcountry']

    # get appropriate currency
    countryname = pycountry.countries.get(alpha_2=selected_country)
    currency = pycountry.currencies.get(numeric=countryname.numeric)
    try:
        currencycode = currency.alpha_3
    except:
        currencycode = 'EUR'
    else:
        currencycode = currency.alpha_3

    # pull current rate
    r1string = 'https://api.getgeoapi.com/v2/currency/convert?api_key=6e1e62d64cbc5f6cec2a8cae8dbd34cd38953e6a&from=USD&to='
    r2string = currencycode
    r3string = '&format=json'
    apistring = r1string + r2string + r3string
    response = requests.get(apistring)
    exchangerate = response.json()
    extrate = exchangerate['rates']
    exttrate = extrate[currencycode]
    exrate = exttrate['rate']

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'country_form': country_form,
                   'categories': categories,
                   'products': products,
                   'exrate': exrate,
                   'currencycode': currencycode
                   })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   })


# -----------------------------------------------------
def CustomerSignUpView(request):
    model = User
    form_class = CustomerSignUpForm
    form = CustomerSignUpForm
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            is_customer = True
            form.save()
            return redirect('shop:signup_successful')
        else:
            context = {'form': form}
            return render(request, 'registration/signup.html', context)
    else:
        context = {'form': form}
        return render(request, 'registration/signup.html', context)


def signup_successful(request):
    return render(request, 'registration/signup_successful.html', {'shop': signup_successful})


class category_info(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        c1 = Category.objects.all()
        s1 = cSerializer(c1, many=True)
        return Response(s1.data)


class user_info(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        c1 = User.objects.all()
        s1 = uSerializer(c1, many=True)
        return Response(s1.data)


class product_infos(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        c1 = Product.objects.all()
        s1 = pSerializer(c1, many=True)
        return Response(s1.data)


class order_info(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        c1 = Order.objects.all()
        s1 = oSerializer(c1, many=True)
        return Response(s1.data)


# def login(request):
#     return render(request, 'registration/login.html', {'shop': login})

def visitor_new(request):
    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitors = form.save(commit=False)
            visitors.created_date = timezone.now()
            visitors.save()
            return render(request, 'shop/product/feedback_done.html')

    else:
        form = VisitorForm()
        # print("Else")
    return render(request, 'shop/product/contactus.html', {'form': form})


def about(request):
    return render(request, 'shop/product/aboutus.html')

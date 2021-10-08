from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
# from parler.models import TranslatableModel, TranslatedField


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)
    phone = models.CharField(blank=True, max_length=20)


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


class Currency(models.Model):
    selectedcountry = CountryField(blank_label='(select country)')


class Feedback(models.Model):
    Name = models.CharField(max_length=200)
    Comments_Or_Questions = models.CharField(max_length=500)
    Email = models.EmailField(max_length=200)
    Phone_Number = models.CharField(max_length=20, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name


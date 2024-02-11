from .models import *
from django.forms import ModelForm, formset_factory
from django import forms


class CustomerForm(ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=15)
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone', 'gender']




class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1)
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    paymode = forms.ModelChoiceField(queryset=PaymentMode.objects.all())
    tel = forms.CharField(max_length=15)


class AddProductForm(forms.Form):
    productid = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    price = forms.CharField(max_length=255)
    TYPE_CHOICES = [('phone', 'Phone'), ('accessory', 'Accessory')]
    product_type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect)
    brand = forms.CharField()
    quantity = forms.IntegerField(min_value=1)

    # class Meta:
    #     model = Product
    #     fields = ('productid', 'name', 'price', 'product_type', 'brand', 'quantityInStock')
    #     exclude = ('type',)



class SearchCustomerForm(forms.Form):
    #search_query = forms.CharField(max_length=100)
    search_query = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Search for customers'}),
        required=False  # Set required to False to remove the "required" message
    )

class SearchSaleForm(forms.Form):
    #search_query = forms.CharField(max_length=100)
    search_query = forms.IntegerField()
    # search_query = forms.CharField(
    #     widget=forms.IntegerField(
    #         #attrs={'placeholder': 'Search here...'}),
    #     required=False  # Set required to False to remove the "required" message
    # ))
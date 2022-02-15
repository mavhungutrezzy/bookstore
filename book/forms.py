from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class CreateUserForm(UserCreationForm):
    
    class Meta:
        
        model = User
        fields = ['username', 'password',]
        
    
class CreateCustomerForm(ModelForm):
    
    class Meta:
        
        model = Customer
        fields = '__all__'
        exclude = ['user']
        

class CreateBookForm(ModelForm):
    
    class Meta:
        
        model = Book
        fields = '__all__'
        
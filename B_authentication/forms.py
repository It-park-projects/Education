from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from B_authentication.models import *

class CreasteUser(UserCreationForm):
   class Meta(UserCreationForm):
        model = CustumUsers
        fields = ('username','first_name','last_name','midile_name','address','phone','passort_seria','price','total_price_persent','education_main','education_filial','password')

class ChangeUser(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustumUsers
        fields = ('first_name','last_name','midile_name','address','phone','passort_seria','price','total_price_persent','education_main','education_filial','password')
from django import forms
from .models import CustomUser, UserProfile
from orders.models import  Address
Password = forms.CharField()


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone', 'email')

    def init(self, args, *kwargs):
        super(CustomUserForm, self).init(args, *kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone')

    def init(self, args, *kwargs):
        super(CustomUserForm, self).init(args, *kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(error_messages={
                                       'Invalid': ("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city',
                  'state', 'country', 'profile_picture')

    def init(self, args, *kwargs):
        super(CustomUserForm, self).__init__(args, *kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line_1','address_line_2','state','country','city',]
    
    def __init__(self, *args, **kwargs):
      super(AddressForm,self).__init__(*args, **kwargs)  
      for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
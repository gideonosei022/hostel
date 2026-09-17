from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from hostel_app.models import Message, Property, PropertyImage, User


# 1️⃣ Owner Registration Form
class OwnerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, initial='owner', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


# 2️⃣ Owner Login Form
class OwnerLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# 3️⃣ Owner Profile Update Form (Optional but Recommended)
class OwnerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']


# 4️⃣ Create / Update Property Form
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'location',
            'region',
            'price',
            'property_type',
            'description',
            'is_available',
            'contact_email',
            'contact_phone',
        ]


# 5️⃣ Property Image Upload Form
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']


# 6️⃣ Contact Owner Form (Guest Messaging)
class ContactOwnerForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender_name', 'sender_email', 'content']


# 7️⃣ Search & Filter Form (For browsing properties)
class PropertySearchForm(forms.Form):
    location = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, decimal_places=2)
    max_price = forms.DecimalField(required=False, decimal_places=2)
    property_type = forms.ChoiceField(
        required=False,
        choices=(
            ('', 'All Types'),
            ('room', 'Room'),
            ('house', 'Entire House'),
        )
    )
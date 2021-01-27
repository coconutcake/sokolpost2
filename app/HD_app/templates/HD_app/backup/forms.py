# Importy ----------------------------------------------------------

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError 

class ChoiceFieldPracownik(forms.ChoiceField):
    def validate(self, value):
        print(value)
        if User.objects.filter(email=value).exists():
            print("user istnieje!")
            raise ValidationError("Taki użytkownik już istnieje!")
        else:
            print("Nie ma takiego uzytkownika")
            return value




# Formularze -------------------------------------------------------
class Company_Form_old(forms.ModelForm):
    user = forms.ModelChoiceField(\
        queryset=User.objects.filter(is_staff=False),
        label="Użytkownik do podpięcia", 
        help_text="Wybierz uzytkownika do którego chcesz\
            podpiąc firmy w modelu Profile. Użytkownik musi mieć założony profil!",
            required=False)
    care = forms.ModelChoiceField(\
        queryset=User.objects.filter(is_staff=True),
        label="Opiekun do podpięcia", 
        help_text="Wybierz opiekuna do którego chcesz\
            podpiąc daną firmę",
            required=False)
    care_substitute = forms.ModelChoiceField(\
        queryset=User.objects.filter(is_staff=True),
        label="Zastępca opiekuna",required=False)
    is_sent = forms.BooleanField(\
        label="Wyślij formularz zmiany hasła", 
        required=False,
        help_text="Czy wysłać formularz zmiany hasła dla użytkownika firmy?"
        )
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ('thumb',)

    def clean(self):
        data = self.cleaned_data
        pole = 'nip'
        msg = 'wpisany nip ma niepoprawna ilość liczb. Dozwolona liczba musi być 10-cyfrowa'
        if len(str(data[pole])) != 10:
            self.add_error(pole, msg)
            raise forms.ValidationError(msg)
    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(Company_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
class Company_Form(forms.ModelForm):
    user = forms.ModelChoiceField(\
        queryset=User.objects.filter(is_staff=False),
        label="Użytkownik do podpięcia z lokalnej bazy kartoteki", 
        help_text="Wybierz uzytkownika do którego chcesz\
            podpiąc firmy w modelu Profile. Użytkownik musi mieć założony profil!",
            required=False)
    care = forms.ModelChoiceField(\
        queryset=User.objects.filter(is_staff=True),
        label="Opiekun do podpięcia", 
        help_text="Wybierz opiekuna do którego chcesz\
            podpiąc daną firmę",
            required=False)
    care_substitute = forms.ModelChoiceField(\
        queryset=User.objects.filter(is_staff=True),
        label="Zastępca opiekuna",required=False)
    is_sent = forms.BooleanField(\
        label="Wyślij formularz zmiany hasła", 
        required=False,
        help_text="Czy wysłać formularz zmiany hasła dla użytkownika firmy?"
        )
    is_created_new = forms.BooleanField(\
        label="Utwórz użytkownika wybranego", 
        required=False,
        help_text="Czy utworzyć nowego użytkownika z wybranego pracownika firmy?"
        )
    pracownik = ChoiceFieldPracownik(\
        )
    email = forms.CharField(\
        max_length=50, required=False, label="Email"
        )
    city = forms.CharField(\
        max_length=50, required=False, label="Miasto")
    ulica = forms.CharField(\
        max_length=50, required=False, label="Ulica")
    nr_dom = forms.CharField(\
        max_length=50, required=False, label="Nr domu")
    nr_lok = forms.CharField(\
        max_length=50, required=False, label="Nr lokalu")
    is_accepted = forms.BooleanField(\
        label="Automatyczna akceptacja tej firmy", 
        required=False,
        initial=True,
        help_text="Czy firma ma zostać automatycznie aktywna? (Tylko na taką firme można zakladać umowy)"
        )
    class Meta:
        model = Company
        fields = ('nip','name','pracownik','email','city','ulica','nr_dom','nr_lok','care','care_substitute','user','is_created_new','is_sent',)
        exclude = ('thumb',)

    def clean(self):
        data = self.cleaned_data
        pole = 'nip'
        msg = 'wpisany nip ma niepoprawna ilość liczb. Dozwolona liczba musi być 10-cyfrowa'
        error_exist_company = "Firma o podanym nipie juz istnieje!"
        if len(str(data[pole])) != 10:
            self.add_error(pole, msg)
            raise forms.ValidationError(msg)
        if Company.objects.filter(nip=data[pole]).exists():
            print("firma istnieje")
            self.add_error(pole, error_exist_company)
            raise forms.ValidationError(error_exist_company)

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(Company_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
class PakietForm(forms.ModelForm):
    
    class Meta:
        model = Pakiet
        fields = ('name','included_hours', 'abonament','ratestack')
    def clean_abonament(self):
        field = self.cleaned_data['abonament']
        if field == 0 or field is None:
            raise forms.ValidationError("Podana cena abonamentu jest niepoprawna. Poprawna cena musi być większa od 0")
        return field
    def clean_name(self):
        field = self.cleaned_data['name']
        if field == "":
            raise forms.ValidationError("Podaj nazwę pakietu")
        return field    
    def __init__(self,*args,**kwargs):
        super(PakietForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                "shadow-sm form-control"
class OrderTemplateForm(forms.ModelForm):
    
    class Meta:
        model = OrderTemplate
        fields = "__all__"
    
    def __init__(self,*args,**kwargs):
        super(OrderTemplateForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                "shadow-sm form-control"
class RateStackForm(forms.ModelForm):
    
    class Meta:
        model = RateStack
        fields = ("name",)
    def __init__(self,*args,**kwargs):
        super(RateStackForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                "form-control shadow-sm"
class User_Form(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    password_reset = forms.BooleanField(label="Resetowanie hasła", \
        help_text="Czy wysłać zresetowanie hasła do tego użytkownika?", required=False)

    class Meta:
        model = User
        fields = ('username','password1','password2','email','first_name',\
            'last_name','is_active','is_staff')

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(User_Form, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
            
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(User_Form, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False # send confirmation email
        if commit:
            user.save()
        
        return user
class Agreement_Form(forms.ModelForm):
    class Meta:
        model = Agreement2
        fields = '__all__'

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(Agreement_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
class Address_Form(forms.ModelForm):
    name = forms.CharField(label='Nazwa adresowa')
    class Meta:
        model = Address
        fields = '__all__'

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(Address_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
class Profile_Form(forms.ModelForm):
    imie = forms.CharField(label="Imię", max_length=50, required=False)
    nazwisko = forms.CharField(label="Nazwisko", max_length=50, required=False)
    email = forms.CharField(label="Email", max_length=50, required=False)
    class Meta:
        model = Profile
        fields = '__all__'
    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(Profile_Form, self).__init__(*args, **kwargs)
        u = User.objects.filter(username=kwargs['instance'])
        self.fields['user'].widget.attrs['readonly'] = True
        self.fields['idf'].widget = forms.HiddenInput()
        self.fields['tablef'].widget = forms.HiddenInput()
        self.fields['thumb'].widget = forms.HiddenInput()
        self.fields['imie'].initial = u.values_list("first_name",flat=True)[0]
        self.fields['nazwisko'].initial = u.values_list("last_name",flat=True)[0]
        self.fields['email'].initial = u.values_list("email",flat=True)[0]
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
class Order_Form(forms.ModelForm):
    agreement = forms.ModelChoiceField(\
        queryset = Agreement2.objects.filter(end_date__gte=datetime.now(),status__name__icontains="Aktywna"), label="Umowa")
    care = forms.ModelChoiceField(\
        queryset = User.objects.filter(is_staff=True), label="Opiekun IT")
    template = forms.ModelChoiceField(\
        queryset = OrderTemplate.objects.all(),label="Szablon zlecenia")
    field_order = [
        'template',
        'name',
        'description',
        'no',
        'order_status',
        'order_type',
        'implementation_type',
        'agreement',
        'address',
        'care',
        'start_datetime',
        'end_datetime',
        ]
    class Meta:
        model = Order
        fields = '__all__'
    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        print(kwargs)
        print(args)
        self.user = kwargs.pop('care',None)
        self.agreement = kwargs.pop('agreement',None)
        super(Order_Form, self).__init__(*args, **kwargs)

        self.fields['no'].widget.attrs['readonly'] = True
        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['updated_date'].widget = forms.HiddenInput()
        self.fields['attachment'].widget = forms.HiddenInput()
        self.fields['template'].required = False
        self.fields['description'].widget.attrs['rows'] = 16
        #self.fields['template'].choices = [(o.id, str(o).upper()) for o in OrderTemplate.objects.all()]
        # self.fields['care'].choices = [(o.id, str(o).upper()) for o in User.objects.filter(is_staff=True)]
        # self.fields['care'].queryset = User.objects.filter(id=self.user.id)


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
        self.fields['name'].widget.attrs['class'] = "shadow-sm form-control font-weight-bold"
    def get_request_user(self,*args,**kwargs):
        return kwargs.pop('user',None)
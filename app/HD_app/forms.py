# Importy ----------------------------------------------------------

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError 
from django.forms import modelformset_factory
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
    # password_reset = forms.BooleanField(label="Resetowanie hasła", \
    #     help_text="Czy wysłać zresetowanie hasła do tego użytkownika?", required=False)

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
class Document_Form(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(Document_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'

# AddressFormSet = modelformset_factory(Address,exclude=('user',),form=Address_Form)

class MessageCreateForm(forms.ModelForm):
    receipt = forms.ModelMultipleChoiceField(
            queryset=User.objects.all().order_by('-first_name'),
            widget=forms.CheckboxSelectMultiple,label="Wyślij do",
        )
    class Meta:
        model = Message
        fields = "__all__"
    
    def __init__(self,*args,**kwargs):
        super(MessageCreateForm,self).__init__(*args,**kwargs)
        self.fields["name"].widget.attrs['class'] = "form-control shadow-sm"
        self.fields["description"].widget.attrs['class'] = "form-control shadow-sm"
        self.fields["name"].widget.attrs['autocomplete'] = "off"

        self.fields["sender"].widget = forms.HiddenInput()
        self.fields["is_read"].widget = forms.HiddenInput()

class AddressDeleteForm(forms.Form):
    address = forms.ModelMultipleChoiceField(
        queryset=Address2.objects.all().order_by('-name'),
        widget=forms.CheckboxSelectMultiple(
            {
                'class': 'no-bullet-list',
                'style': 'list-style: none;'
            }
         ),label="Adres",
    )
    def __init__(self,*args,**kwargs):
        address = kwargs.pop("address")
        print("Znalezione adresy firmy:")
        print(address)
        super(AddressDeleteForm,self).__init__(*args,**kwargs)
        self.fields["address"].queryset = address
class DocumentDeleteForm(forms.Form):
    document = forms.ModelMultipleChoiceField(
        queryset=Document.objects.all().order_by('-name'),
        widget=forms.CheckboxSelectMultiple(
            {
                'class': 'no-bullet-list',
                'style': 'list-style: none;'
            }
         ),label="Dokument",
    )
    def __init__(self,*args,**kwargs):
        document = kwargs.pop("document")
        print("Znalezione dokumenty")
        print(document)
        super(DocumentDeleteForm,self).__init__(*args,**kwargs)
        self.fields["document"].queryset = document

class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(DocumentCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
            self.fields["name"].widget.attrs['autocomplete'] = "off"
            self.fields["start_date"].widget.attrs['autocomplete'] = "off"
            self.fields["end_date"].widget.attrs['autocomplete'] = "off"
            self.fields["company_sfk"].widget.attrs['readonly'] = True
class AddressCreateForm(forms.ModelForm):

    class Meta:
        model = Address2
        fields = '__all__'

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(AddressCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
            self.fields["name"].widget.attrs['autocomplete'] = "off"
            self.fields["company_sfk"].widget.attrs['readonly'] = True

class RaportSearchForm(forms.ModelForm):
    care = forms.ModelChoiceField(
            queryset=User.objects.all().order_by('-first_name'),
            label="Opiekun IT",
            required=False
        )
    class Meta:
        fields = ["document","start_datetime","end_datetime","care"]
        model = Order2

    def __init__(self,*args,**kwargs):
        super(RaportSearchForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control shadow-sm"
            self.fields["document"].widget.attrs['readonly'] = True
            self.fields['start_datetime'].widget.attrs.update({
                'autocomplete': 'off'
            })
            self.fields['end_datetime'].widget.attrs.update({
                'autocomplete': 'off'
            })
    

    
class OrderCreateForm(forms.ModelForm):
    excluded = [4,6,7,9]

    order_template = forms.ModelChoiceField(label="Wybierz szablon",\
        queryset=OrderTemplate.objects.all(),required=False)
    order_status = forms.ModelChoiceField(label="Status",\
        queryset=OrderStatus.objects.all().exclude(id__in=excluded))
    class Meta:
        model = Order2
        fields = '__all__'

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        try:
            request = kwargs.pop("request")
            me = User.objects.get(pk=request.user.id)
            users = User.objects.filter(pk=request.user.id)
        except:
            pass
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        try:
            self.fields["care"].initial = me
            self.fields["care"].queryset = users
            
        except:
            pass
        self.fields["created_date"].widget = forms.HiddenInput()
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
            self.fields['start_datetime'].widget.attrs['autocomplete'] = "off"
            self.fields['end_datetime'].widget.attrs['autocomplete'] = "off"
class OrderDetailForm(forms.ModelForm):
    excluded = [4,6,7,9]
    order_template = forms.ModelChoiceField(label="Wybierz szablon",\
        queryset=OrderTemplate.objects.all(),required=False)
    order_status = forms.ModelChoiceField(label="Status",\
        queryset=OrderStatus.objects.all().exclude(id__in=excluded))
    class Meta:
        model = Order2
        fields = '__all__'


    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(OrderDetailForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'
            self.fields["created_date"].widget = forms.HiddenInput()
            self.fields['start_datetime'].widget.attrs['autocomplete'] = "off"
            self.fields['end_datetime'].widget.attrs['autocomplete'] = "off"
class OrderSearchModelForm(forms.ModelForm):

    class Meta:
        model = Order2
        fields = "__all__"
        exclude = ("description","created_date","updated_date","care")

    def __init__(self,*args,**kwargs):
        super(OrderSearchModelForm,self).__init__(*args,*kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].help_text = None
            self.fields[field].widget.attrs['class'] = "form-control shadow-sm"

    def clean(self):
        """ Wyrzuca pola z clened_data jeśli są puste lub None """
        cleaned = {}
        print("Przeszukuje pola w poszukiwaniu wartosci None lub ""...")
        for k,v in self.cleaned_data.items():
            if v == None or v == "":
                print(f"{k} - brak wartości")
            else:
                cleaned.update({k:v})
        print(f"Zwracam zmodyfikowane cleaned_data: \n{cleaned}")
        return cleaned

class DocumentDetailForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

    # Dodaj do wszystch pol klasy
    def __init__(self, *args, **kwargs):
        super(DocumentDetailForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = \
                'shadow-sm form-control'


class SubiektCompanyCreateForm(forms.Form):
    Nazwa = forms.CharField(label="Nazwa", max_length=50, required=False)
    Typ = forms.BooleanField(label="Pracownik", required=False)
    NazwaPelna = forms.CharField(label="Pełna nazwa", max_length=120, required=False)
    Nip = forms.CharField(label="Nip", max_length=10, required=False)
    Miejscowosc = forms.CharField(label="Miejscowość", max_length=30, required=False)
    KodPocztowy = forms.CharField(label="Kod pocztowy", max_length=7, required=False)
    Ulica = forms.CharField(label="Ulica", max_length=30, required=False)
    NrDomu = forms.CharField(label="Nr domu", max_length=10, required=False)
    NrLokalu = forms.CharField(label="Nr lokalu", max_length=10, required=False)

    class Meta:
        fields = "__all__"
    def __init__(self,*args,**kwargs):
        super(SubiektCompanyCreateForm,self).__init__(*args,*kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control shadow-sm"
            # self.fields[field].widget.attrs['readonly'] = True
class SubiektCompanySearchForm(forms.Form):
    nazwa = forms.CharField(label="Nazwa", max_length=25, required=False)
    nip = forms.CharField(label="nip", max_length=10, required=False)
    class Meta:
        fields = "__all__"
    def __init__(self,*args,**kwargs):
        super(SubiektCompanySearchForm,self).__init__(*args,*kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control shadow-sm"
class SubiektCompanySearchForm1(forms.Form):
    nip = forms.CharField(label="NIP", max_length=10, required=False,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter numbers Only '}))
    nazwa = forms.CharField(label="Nazwa", max_length=25, required=False)
    class Meta:
        fields = "__all__"
    def __init__(self,*args,**kwargs):
        super(SubiektCompanySearchForm1,self).__init__(*args,*kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control shadow-sm"



class SearchUserForm(forms.Form):
    """ Search Users dla Subiekta """
    nip = forms.IntegerField(label="nip",required=False)
    class Meta:
        fields = "__all__"
    def __init__(self,*args,**kwargs):
        super(SearchUserForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control shadow-sm"
            
    def clean_nip(self,value):
        if len(str(value)) < 10:
            raise ValidationError("Za krótki numer nip")
        return value
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

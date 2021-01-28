# Importy ------------------------------------------------------
from datetime import time
import datetime
from django.db import models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import json
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import \
    User, AbstractUser
from django.db.models.signals import \
    post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta
from django.conf import settings
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.core.files import File
from openpyxl import load_workbook
import os,sys
from fpdf import FPDF
from django.core.mail import send_mail, EmailMessage
from django.utils.html import format_html, mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from HD_app.additionals.validationprintservice import *
from django.db.models import F, Func, Avg, Sum
import numpy as np
# warnings off - Usuwanie warningów przy komunikacji po ssl
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from HD_app.additionals.subiekt import *
subiekt = Subiekt()

from django.db.models.functions import ExtractDay,ExtractHour
# Email backend -------------------------------------------
def get_seconds_from_days(days,hours):
    return ((days*hours)*60)*60
def get_current_month_busdays():
    current_datetime = datetime.datetime.now()
    first_day = current_datetime.replace(day=1,hour=0,minute=0,second=0)
    last_day = current_datetime.replace(day=1,hour=23,minute=59,second=59,month=current_datetime.month+1)-datetime.timedelta(days=1)
    days = np.busday_count(first_day.date(),last_day.date())
    return days
def get_user_data(self):
    return "%s %s [%s]" % (self.first_name, self.last_name, self.email)
def get_current_month_efficiency(self,max_efficiency_hours=8,shift_start=8,shift_end=16):
    current_datetime = datetime.datetime.now()
    orders = Order2.objects.filter(
        care__id=self.pk,
        start_datetime__month=current_datetime.month,
        start_datetime__year=current_datetime.year
        ).annotate(
            time=F('end_datetime')-F('start_datetime')
        ).values(
            "time"
        ).annotate(
            sum=Sum("time")
        ).values(
            "sum"
        )
    busdays = get_current_month_busdays()
    busday_shift_seconds = get_seconds_from_days(busdays,max_efficiency_hours)
    my_time = list(orders)[0]['sum'].total_seconds()
    my_efficiency = my_time*100/busday_shift_seconds
    return "{:.2f}".format(my_efficiency)



def count_orders(self):
    p = Profile.objects.get(user=self.id)
    if Order.objects.filter(care__id=self.id).exists():
        return Order.objects.filter(care__id=self.id).count()
    else:
        return 0
def count_order_values(self):
    p = Profile.objects.get(user=self.id)
    o = Order.objects.filter(care__id=self.id).exists()
    if Order.objects.filter(care__id=self.id).exists():
        pass
    else:
        pass
User.add_to_class("__str__", get_user_data)
User.add_to_class("count_orders", count_orders)
User.add_to_class("get_current_month_efficiency", get_current_month_efficiency)
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

# Template email ------------------------------------------
def email_new_order(instance):
    return """\
    <table>
    <tbody>
    <tr>
    <td><img id="imglogo" class="logo" src="http://mign.pl/img/logogb.jpg" width=150 alt="logo" /></td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    </tr>
    </tbody>
    </table>

    <table>
    <tbody>
        <hr>
        <tr style="height: 23px;">
            <td style="height: 23px;">
    </tr>
    </tbody>
    </table>

    <table>
    <tbody>
    <tr>
    <td>
    <p><b>Witaj %s,</b></p>
    <p>Twoje zgłoszenie na zlecenie nr: <b>%s</b> zostało wysłane. Na bierząco możesz obserwować stan zlecenia w aplikcji webowej Sokół.</p>
    <br><p>Email generowany automatycznie. Prosimy nie odpowiadać</p><br>
    </td>
    </tr>
    </tbody>
    </table>

    <table>
        <hr>
    <tbody>
    <tr>
    <td>
    
    <p><a href="http://hajduk.eu"><span">www.gobit.com.pl/</span></a></p>
    <p><span>Przedsiębiorstwo Importowo-Eksportowe Sprzętu Elektronicznego GOBIT<br />ul. Walczaka 20, 66-400 Gorzów Wlkp., tel. 95 735 05 00, fax 95 735 05 07</span></p>
    <p><span"><strong><img width=50 src="http://mign.pl/img/logogb.jpg"></a></strong></span></p>
    </td>
    </tr>
    </tbody>
    </table>

    <p>&nbsp;</p>
""" % (instance.user.first_name, instance.id)
# Wyszukiwanie modelu obowiązującego ----------------------
def get_uptodate_model(*args,**kwargs):
    """ Przeszukuje model i zwraca wazny """
    model = kwargs.get("model")
    to_compare = kwargs.get("to_compare")
    objs = model.objects.all()
    for obj in objs:
        if obj.start < to_compare < obj.end:
            return obj

# Modele --------------------------------------------------
class DocumentType(models.Model):
    """ Typ umowy """
    name = models.CharField(_("Nazwa typu dokumentu"),max_length=30)
    description = models.TextField(_("Opis typu dokumentu"),max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = _("Typ dokumentu")
        verbose_name_plural = _("Typy dokumentów")

    def __str__(self):
        return f"{self.name}"
    def get_absolute_url(self):
        return reverse("DocumentType_detail",kwargs={"pk":self.pk})
    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
    def get_view_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
class DistanceCalcProfile(models.Model):
    """
    Profil kalkulatora kilometrówki
    """
    name = models.CharField(_("Nazwa profilu"), max_length=100)
    cost = models.FloatField(_("Koszt per km"))

    start = models.DateTimeField(_("Obowiązuje od"), help_text="Obowiązuje dla przeliczeń zleceń",auto_now=False, auto_now_add=False,null=True)
    end = models.DateTimeField(_("Obowiązuje do"), help_text="Obowiązuje dla przeliczeń zleceń",auto_now=False, auto_now_add=False,null=True)

    class Meta:
        verbose_name = _("Profil kosztów kilometrowych")
        verbose_name_plural = _("Profile kosztów kilometrowych")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("DistanceCalculator_detail", kwargs={"pk": self.pk})
    # def __init__(self, *args, **kwargs):
    #     super(DistanceCalcProfile, self).__init__(*args, **kwargs)
    #     self._is_default = self.is_default
class Rate(models.Model):
    """
    Zakres cenowy dla wskazanego zakresu czasu pracy
    """
    name = models.CharField(_("Nazwa"), max_length=50)
    start = models.TimeField(_("Od"), auto_now=False, auto_now_add=False)
    stop = models.TimeField(_("Do"), auto_now=False, auto_now_add=False)
    price = models.FloatField(_("Stawka godzinowa"))
    is_default = models.BooleanField(_("Domyślna stawka rozliczeniowa"),default=False,help_text="Stawka domyślna wg której będą rozliczane godziny w pakiecie")

    class Meta:
        verbose_name = _("Stawka")
        verbose_name_plural = _("Stawki")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Rate_detail", kwargs={"pk": self.pk})

    def __init__(self,*args,**kwargs):
        """
        Przypisanie pola dla signału do porównania pola i ustawienia reszty obiektów na is_default=False
        """
        super(Rate,self).__init__(*args,**kwargs)
        self._is_default = self.is_default
class RateStack(models.Model):
    """
    Zbiór zakresów cenowych
    """
    name = models.CharField(_("Nazwa pakietu godzinowego"), max_length=50)
    rate = models.ManyToManyField(Rate, verbose_name=_("Rate"))

    start = models.DateTimeField(_("Obowiązuje od"), help_text="Obowiązuje dla przeliczeń zleceń",auto_now=False, auto_now_add=False,null=True)
    end = models.DateTimeField(_("Obowiązuje do"), help_text="Obowiązuje dla przeliczeń zleceń",auto_now=False, auto_now_add=False,null=True)
    class Meta:
        verbose_name = _("Zestaw stawek")
        verbose_name_plural = _("Zestawy stawek")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("RateStack_detail", kwargs={"pk": self.pk})
class Pakiet(models.Model):
    """
    Pakiet zbiorów zakresów cenowych
    """
    name = models.CharField(_("Nazwa"), max_length=50)
    ratestack = models.ForeignKey(\
        RateStack, 
        verbose_name=_("Stawki godzinowe"), 
        on_delete=models.CASCADE,
        null=True
        )
    included_hours = models.FloatField(\
        _("Godziny w pakiecie"), 
        help_text="Czas w ramach którego, klient nie pomosi dodatkowych kosztów za wsparcie w ramach umowy",
        default=0.0,
        )
    abonament = models.FloatField(\
        _("Abonament"),
        help_text="Abonament z PLN",
        default=0
        )
    class Meta:
        verbose_name = _("Pakiet")
        verbose_name_plural = _("Pakiety")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Pakiet_detail", kwargs={"pk": self.pk})
class Address2(models.Model):
    """ Adres """
    # Subiekt Symbol (firma)
    company_sfk = models.CharField(_("Firma subiekta"), max_length=100,null=True,blank=True)
    name = models.CharField(max_length=30,help_text="Nazwa adresowa")
    nr_dom = models.CharField(_("Nr domu"), max_length=100,null=True,blank=True)
    nr_lok = models.CharField(_("Nr lokalu"), max_length=100,null=True,blank=True)
    city = models.CharField(_("Miasto"), max_length=100,null=True,blank=True)
    street = models.CharField(_("Ulica"), max_length=100,null=True,blank=True)
    distance = models.IntegerField(_("Km"), help_text="Dystans do klienta w km",blank=True,null=True)
    is_default = models.BooleanField(_("Domyślna"), default=False)
    
    class Meta:
        verbose_name = _("Adres")
        verbose_name_plural = _("Adresy")

    def __str__(self):
        return f"{self.name}, {self.street}, {self.nr_dom}, {self.city}, {self.distance}km"

    def get_absolute_url(self):
        return reverse("Address2_detail", kwargs={"pk": self.pk})   

    def __init__(self, *args, **kwargs):
        super(Address2, self).__init__(*args, **kwargs)
        self._is_default = self.is_default

    def get_addresses(self):
        return self.__class__.objects.filter(company_sfk=self.company_sfk)

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
    def get_view_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
class DocumentStatus(models.Model):
    """
    Stan umowy
    """
    name = \
        models.CharField(\
            _("Nazwa statusu"), 
            max_length=50)
    description = \
        models.TextField(\
            _("Opis"))

    class Meta:
        verbose_name = _("Status umowy")
        verbose_name_plural = _("Statusy umowy")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("DocumentStatus_detail", kwargs={"pk": self.pk})
class Document(models.Model):
    """
    Umowa
    """
    company_sfk = models.CharField(_("Firma subiekta"),help_text=settings.UNIQUE_API_SYMBOL_LABEL,max_length=50,blank=False,null=True)
    name = \
        models.CharField(\
            _("Nazwa"), 
            max_length=50)
    start_date = \
        models.DateField(\
            _("Data zawarcia"), 
            auto_now=False, 
            auto_now_add=False,null=True)
    end_date = \
        models.DateField(\
        _("Data zakończenia"), 
        auto_now=False, 
        auto_now_add=False,null=True)
    document_type = models.ForeignKey(\
        DocumentType,
        verbose_name = _("Typ dokumentu"),
        on_delete = models.SET_NULL,
        blank=False,null=True
        )
    status = \
        models.ForeignKey(\
            DocumentStatus, 
            verbose_name=_("Status dokumentu"), 
            on_delete=models.SET_NULL,
            blank=False, null=True) 
    class Meta:
        verbose_name = _("Dokument")
        verbose_name_plural = _("Dokumenty")
    def __str__(self):
        return "%s - %s" % (self.get_subiekt_company_name(),self.name)
    def get_absolute_url(self):
        return reverse("document_detail", kwargs={"pk": self.pk})

    def get_subiekt_company_name(self):
        endpoint = subiekt.get_absolute_endpoint("kontrahenci")
        data = {"Nip":self.company_sfk}
        try:
            r = requests.post(endpoint,data=json.dumps(data),headers=subiekt.get_header(),verify=False)
            if r.status_code == 200:
                return r.json().get("KontrahenciList")[0]['Nazwa']
        except:
            return "uruchom subiekta!"
    def get_subiekt_company_nip(self):
        endpoint = subiekt.get_absolute_endpoint("kontrahenci")
        data = {"Nip":self.company_sfk}
        try:
            r = requests.post(endpoint,data=json.dumps(data),headers=subiekt.get_header(),verify=False)
            if r.status_code == 200:
                return r.json().get("KontrahenciList")[0]['Nip']
        except:
            return "uruchom subiekta!"
    def get_fields(self):
        """ Wszytskie pola """
        class_name = self.__class__.__name__
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
    def get_view_fields(self):
        """ Pola widoczne na widoku """
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
    def get_pending_orders(self):
        return Order2.objects.filter(document__id=self.id).exclude(order_status=6)
    def get_completed_orders(self):
        return Order2.objects.filter(document__id=self.id).filter(order_status=6)
class ProfileType(models.Model):
    """
    Typ profilu uzytkownika
    """
    name = \
        models.CharField(\
            _("Nazwa"),
            max_length=50)
    description = \
        models.TextField(\
            _("Opis"),
            blank=True,)

    class Meta:
        verbose_name = _("Typ użytkownika")
        verbose_name_plural = _("Typy użytkowników")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(\
            "ProfileType_detail", kwargs={"pk": self.pk})
class ProfileGroup(models.Model):
    """ Grupa Profilowa """
    name = models.CharField(_("Nazwa"), max_length=50)
    description =  models.TextField(_("Opis"),blank=True)

    class Meta:
        verbose_name = _("Grupy użytkowników")
        verbose_name_plural = _("Grupy użytkowników")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ProfileGroup_detail", kwargs={"pk": self.pk})
class UserSettings(models.Model):
    """
    Ustawienia użytkownika
    """
    user = models.OneToOneField(\
        User, 
        verbose_name=_("Użytkownik"), 
        on_delete=models.CASCADE)
    email_notifications = models.BooleanField(\
        _("Powiadomienia email"), 
        default=True)
    alert_notifications = models.BooleanField(\
        _("Powiadomienia o alertach"),default=True)

    class Meta:
        verbose_name = _("Ustawienia użytkownika")
        verbose_name_plural = _("Ustawienia użytkowników")

    def __str__(self):
        return "%s %s - [%s]" % (self.user.first_name, self.user.last_name, self.user.email)

    def get_absolute_url(self):
        return reverse("UserSettings_detail", kwargs={"pk": self.pk})
class Message(models.Model):
    """
    Wiadomości
    """
    sender = models.ForeignKey(\
        User, 
        verbose_name=_("Sender"), 
        related_name="sender",
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    receipt = models.ManyToManyField(User, verbose_name=_("Adresat"))
    name = models.CharField(\
        _("Tytuł"), 
        max_length=50
        )
    description = models.TextField(\
        _("Wiadomość"),
        blank=True
        )
    
    is_read = models.BooleanField(\
        _("Przeczytana"),
        default=False)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Message_detail", kwargs={"pk": self.pk})
class Profile(models.Model):
    """
    Profil użytkownika
    """
    user = \
        models.OneToOneField(\
            User,
            on_delete=models.CASCADE)
    cellphone = \
        models.DecimalField(\
            _("Telefon komórkowy"), 
            max_digits=12, 
            decimal_places=0,
            blank=True, null=True)
    typ = \
        models.ForeignKey(\
            ProfileType,
            verbose_name=_("Typ"),
            on_delete=models.SET_NULL,
            blank=True, null=True)
    group = models.ForeignKey(ProfileGroup, verbose_name=_("Grupa użytkowników"),\
        on_delete=models.CASCADE,blank=True,null=True)
    thumb = \
        models.ImageField(\
            _("Thumb"), 
            upload_to="thumbs/", 
            help_text="Akceptowalne pliki: *jpg, *png",
            height_field=None, 
            width_field=None, 
            max_length=None, 
            default=None,
            blank=True, null=False
            )
    idf = \
        models.DecimalField(\
            _("Klucz obcy"), 
            decimal_places=0,
            max_digits=10,
            blank=True, null=True)
    tablef = \
        models.CharField(_("Tabela obca"), 
        max_length=50,
        blank=True)

    class Meta:
        verbose_name = _("Profil użytkownika")
        verbose_name_plural = _("Profile użytkowników")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse(\
            "Profile_detail", kwargs={"pk": self.pk})
class OrderType(models.Model):
    name = \
        models.CharField(\
            _("Nazwa"), 
            max_length=50, 
            blank=False, null=True)
    description = \
        models.TextField(\
            _("Opis"), 
            blank=True)

    class Meta:
        verbose_name = _("Typ zlecenia")
        verbose_name_plural = _("Typy zleceń")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("OrderType_detail", kwargs={"pk": self.pk})
class ImplementationType(models.Model):
    name = \
        models.CharField(\
            _("Typ realizacji"), 
            max_length=50)
    is_traveled = models.BooleanField(_("Wymaga dojazdu?"),default=False)
    class Meta:
        verbose_name = _("Typ realizacji")
        verbose_name_plural = _("Typy realizacji")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("ImplementationType_detail", kwargs={"pk": self.pk})
class OrderStatus(models.Model):
    name = \
        models.CharField(\
            _("Stan zlecenia"), 
            max_length=50)
    description = \
        models.TextField(\
            _("Opis"),
            blank=True,
            )

    class Meta:
        verbose_name = _("Stan zlecenia")
        verbose_name_plural = _("Stany zleceń")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
class Order2(models.Model):
    """ Zlecenie """
    name = \
        models.CharField(\
            _("Nazwa"), help_text="Krótka nazwa zlecenia",
            max_length=90, blank=False, default="")
    document = \
        models.ForeignKey(\
            Document, 
            verbose_name=_("Dokument"), 
            blank=False,
            on_delete=models.CASCADE)
    address = \
        models.ForeignKey(\
            Address2, 
            verbose_name=_("Adres"),
            help_text="Adres dojazdu. Wypełnij jeśli zlecenie wykonujesz u klienta. Automatycznie ustawiany jest domyślny dla firmy",
            null=True,
            blank=True, 
            on_delete=models.CASCADE
            )
    start_datetime = \
        models.DateTimeField(\
            _("Start"), 
            auto_now=False, 
            auto_now_add=False,
            blank=True,
            null=True
            )
    end_datetime = \
        models.DateTimeField(\
            _("Koniec"), 
            auto_now=False, 
            auto_now_add=False,
            blank=True,
            null=True
            )
    order_status = \
        models.ForeignKey(\
            OrderStatus, 
            verbose_name=_("Stan zlecenia"), 
            on_delete=models.CASCADE, blank=True, null=True)
    order_type = \
        models.ForeignKey(\
            OrderType, 
            verbose_name=_("Typ zlecenia"), 
            on_delete=models.CASCADE, blank=True, null=True)
    implementation_type = \
        models.ForeignKey(\
            ImplementationType, 
            verbose_name=_("Typ realizacji"), 
            on_delete=models.CASCADE, blank=False, null=True)
    care = \
        models.ForeignKey(\
            User, 
            verbose_name=_("Opiekun IT"),
            null=True,
            on_delete=models.CASCADE)
    description = \
        models.TextField(\
            _("Opis"), help_text="Tutaj opisz zlecenie. Możesz używać szablonów do wklejania poniej",
            max_length=999, 
            blank=False, default="")
    created_date = \
        models.DateTimeField(\
            _("Data utworzenia"), 
            auto_now=False, 
            auto_now_add=False,
            blank=True, null=True)
    updated_date = \
            models.DateTimeField(\
            _("Data operacji na rekordzie"), 
            auto_now=False, 
            auto_now_add=False,
            blank=True, null=True) 

    class Meta:
        verbose_name = _("Zlecenie")
        verbose_name_plural = _("Zlecenia")
    def __str__(self):
        return f"{self.name}"
    def get_absolute_url(self):
        return reverse(\
            "order2_detail", kwargs={"pk": self.pk})
    
    # Fukcje obliczeniowe zlecenia
    def resetDate(self,rdate):
        rdate = rdate
        d = datetime.datetime.replace(year=rdate.year,month=rdate.month,day=1,hour=0,minute=0,second=0)
        return d.date()
    def get_object(self):
        obj = Order2.objects.get(pk=self.id)
        return obj
    def are_dates(self):
        """
        Sprawdzanie czy sa wszystkie daty wpisane w pola
        """
        if self.start_datetime and self.end_datetime:
            return True
        else:
            return False
    def get_rates(self):
        try:
            ratestack = get_uptodate_model(model=RateStack,to_compare=self.created_date)
            return ratestack.rate
        except:
            raise ObjectDoesNotExist("Brak obowiązujących stawek Ratestack")



    def get_ratestack(self):
        try:
            ratestack = get_uptodate_model(model=RateStack,to_compare=self.created_date)
            return ratestack
        except:
            raise ObjectDoesNotExist("Brak obowiązujących stawek Ratestack")
    def get_days(self):
        days = self.end_datetime.day-self.start_datetime.day
        return days+1
    def get_costs(self):
        """
        Zwraca koszta wg stawek godzinowych
        """
        koszt = float()
        order_start = self.start_datetime
        order_stop = self.end_datetime
        diff = order_stop-order_start
        for day in range(1):
            diff = timedelta()
            for r in self.get_rates().all():
                print(f"rate: {r}")
                if order_stop.time() > r.stop:
                    hhh = r.stop.hour + 1
                    timee = datetime.time(hhh,0,0)
                    order_stop2 = order_stop.replace(hour=timee.hour,minute=timee.minute,second=timee.second)
                    t = timedelta(hours=order_start.hour,minutes=order_start.minute,seconds=order_start.second)
                    st = timedelta(hours=order_stop2.hour,minutes=order_stop2.minute,seconds=order_stop2.second)
                    u = st - t
                    k = ((u.total_seconds()/60)/60)*r.price
                    diff += u
                    order_start = order_start.replace(hour=timee.hour,minute=timee.minute,second=timee.second)
                    koszt = koszt + k
                elif order_start.time() >= r.start and order_stop.time() <= r.stop:
                    u = order_stop-order_start
                    diff += u
                    kk = ((u.total_seconds()/60)/60)*r.price
                    koszt = koszt + kk
                    break
        return koszt
    def calculate_order(self):
        """ Zwraca koszta zleceń wg godzinówek """
        order = self.get_object()

        if self.are_dates():
            return self.get_costs()
        else:
            return "Brak kosztów"
    def getRateCost(self):
        try:
            ratestack = get_uptodate_model(model=RateStack,to_compare=self.created_date)
            return ratestack.rate.get(is_default=True).price
        except:
            raise ObjectDoesNotExist("Brak obowiązujących stawek Ratestack")
    

    def getDistanceCalcProfileCosts(self):
        try:
            obj = get_uptodate_model(model=DistanceCalcProfile,to_compare=self.created_date)
            return obj.cost
        except:
            raise ObjectDoesNotExist("Brak obowiązujących stawek stawek dystansowych")
    def calculate_timedelta(self):
        td = timedelta()
        diff = self.end_datetime-self.start_datetime
        return diff.total_seconds()
    def calculate_order_with_distance(self):
        """ Kalkulator kosztów dojazdu dla zlecenia """
        distance_cost = self.getDistanceCalcProfileCosts()
        distance_km = self.get_two_way_distance() if self.is_traveled() else 0
        costs = (distance_km)*2*distance_cost
        return float("{:.2f}".format(self.calculate_order()+costs))
    def get_fuel_costs(self):
        distance_costs = self.getDistanceCalcProfileCosts()
        distance_km = self.get_two_way_distance() if self.is_traveled() else 0
        costs = (distance_km)*2*distance_costs
        return float("{:.2f}".format(costs))
    def get_distance(self):
        return float(self.address.distance) if self.is_distance() else self.get_google_km()
    def get_two_way_distance(self):
        two_way_distance = self.get_distance()*2
        return two_way_distance
    def get_google_km(self):
        api_key ='AIzaSyB7W8VWn3SxVUoDFbtyLoDAk7hpLP2LivA'
        origin = 'Gorzow+Poland+Gobit' 
        destination = self.address.city+"+"+self.address.street+"+"+self.address.nr_dom
        url ='https://maps.googleapis.com/maps/api/directions/json?'
        r = requests.get(url+'origin='+origin+'&destination='+destination+'&key='+api_key+"&avoid=tolls|highways")
        routes = r.json().get("routes")[0].get("legs")[0].get("distance").get("value")
        km = round((routes/1000),2)
        return km
    def is_distance(self):
        return True if self.address.distance else False
    def is_traveled(self):
        return True if self.implementation_type.is_traveled else False
    def get_view_fields(self):
        """ Pola widoczne na widoku """
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
class OrderCategory(models.Model):
    name = \
        models.CharField(\
            _("Nazwa"), 
            max_length=50
            )
    description = \
        models.TextField(\
            _("Opis"),
            blank=True)

    class Meta:
        verbose_name = _("Kategoria zlecenia")
        verbose_name_plural = _("Kategorie zleceń")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("OrderCategory_detail", kwargs={"pk": self.pk})
class OrderTemplate(models.Model):
    name = models.CharField(_("Nazwa"), max_length=100)
    description = models.TextField(_("Opis"))
    order_type = models.ForeignKey(OrderType, verbose_name=_("Domyślny typ zlecenia"), default=1, on_delete=models.CASCADE)
    implementation_type = models.ForeignKey(ImplementationType, verbose_name=_("Domyślny typ realizacji zlecenia"), default=1, on_delete=models.CASCADE)
    order_status = models.ForeignKey(OrderStatus, verbose_name=_("Domyślny status zlecenia"), default=3, on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Opis zlecenia")
        verbose_name_plural = _("Opis zleceń")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("OrderTemplate_detail", kwargs={"pk": self.pk})

# Sygnały ---------------------------------------------------
class Signals():
    def __init__(self,*args,**kwargs):
        self.model = kwargs.get("model")
        self.instance = kwargs.get("instance")
    def set_created_date(self):
        self.instance.created_date = datetime.datetime.now()
        self.instance.save()
    def set_updated_date(self):
        self.model.objects.filter(pk=self.instance.id).update(updated_date=datetime.datetime.now())

@receiver(post_save, sender=User)
def createuser_signal(sender, instance, created, **kwargs):
    """
    Tworzy profil uzytkownika, oraz ustawienia przy zakładaniu konta
    """
    printservice = ValidationPrintService("%s: %s" % ("SIGNAL",sys._getframe().f_code.co_name),"SIGNAL")
    printservice.set_signal_kwargs(i=instance,c=created,s=sender)
    print(instance)
    if created:
        printservice.print_green("CREATED?","YES")
        try:
            try:
                Profile.objects.create(user=instance,cellphone=instance.tel)
                printservice.print_green("PROFILE SAVED?","YES")
                printservice.print_green("Tel?","YES")
            except:
                Profile.objects.create(user=instance)
                printservice.print_green("PROFILE SAVED?","YES")
                printservice.print_red("Tel?","NO")
            try:
                UserSettings.objects.create(user=instance)
                printservice.print_green("USERSETTINGS SAVED?","YES")
            except:
                printservice.print_red("USERSETTINGS SAVED?","NO")
            instance.profile.save()
        except:
            pass
    else:
        printservice.print_red("CREATED?","NO")
    instance.profile.save()
@receiver(post_save, sender=Order2)
def order_notification(sender, instance, created, **kwargs):
    printservice = ValidationPrintService("%s: %s" % ("SIGNAL",sys._getframe().f_code.co_name),"SIGNAL")
    printservice.set_signal_kwargs(i=instance,c=created,s=sender)
    s = Signals(model=sender,instance=instance,**kwargs)
    if created:
        printservice.print_green("CREATED?","YES")
        s.set_created_date()
        d = datetime.datetime.now()
        instance.no = "GZ_%s/%s/%s/%s" % (instance.id,d.day,d.month,d.year)
        instance.save()
    printservice.print_green("UPDATED?","YES")
    s.set_updated_date()
@receiver(post_save, sender=Rate)
def rate_sig(sender, instance, created, **kwargs):
    """
    nadpisanie domyslego pola
    """
    if instance.is_default != instance._is_default:
        Rate.objects.all().update(is_default=False)
        Rate.objects.filter(pk=instance.id).update(is_default=instance.is_default)



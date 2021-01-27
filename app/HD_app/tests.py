from django.test import TestCase, Client
import json
import requests
from HD_app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
import datetime
from django.forms.models import model_to_dict
print("\n")

# Testy --------------------------------------------------------
class ProfileTypeTest(TestCase):
    """Test tworzenia nowego typu profilu"""
    def setUp(self):
        ProfileType.objects.create(name='test', description='test')
    def test_profiletype_create(self):
        p = ProfileType.objects.get(name='test', description='test')
        self.assertEqual(p.name, 'test')
        self.assertEqual(p.description, 'test')
        print("[OK] Utworzono rekordy modelu: ProfileType")

class UserTest(TestCase):
    """Test tworzenia nowego Usera"""
    def setUp(self):
        User.objects.create_user(\
            username='test', 
            email='test@test.pl', 
            password='test')
    def test_user_create(self):
        u = User.objects.get(username='test')
        self.assertEqual(u.username, 'test')
        self.assertEqual(u.email, 'test@test.pl')
        print("[OK] Utworzono rekordy modelu: User")

class ProfileTest(TestCase):
    def setUp(self):
        self.phone = '999999999'
        self.rate = 1.4
        self.u = User.objects.create_user(\
            username='testuser', 
            email='test@test.pl', 
            password='testpassword')
        self.t = ProfileType.objects.create(\
            name='test', description='test')

    def test_ProfileTest(self):
        profiletype_create = ProfileType.objects.get(\
            name='test', description='test')
        profile_create = Profile.objects.create(\
            user=self.u, 
            typ=self.t, 
            phone=self.phone, 
            )
        profile_get = Profile.objects.get(\
            user=self.u, 
            typ=self.t, 
            phone=self.phone, 
            )
        self.assertEqual(profile_create, profile_get)
        print("[OK] Utworzono rekordy modelu: Profile")

class CustomerTest(TestCase):
    def setUp(self):
        self.customer = Customer2.objects.create(name='test', street='test')

    def test_customer(self):
        q = Customer2.objects.get(name=self.customer.name, street=self.customer.street)
        self.assertEqual(self.customer, q)
        print("[OK] Utworzono rekordy modelu: Customer")

class OrderTest(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(\
            username='testcustomer', 
            email='test@test.pl', 
            password='testcustom123')
        self.user = User.objects.create_user(\
            username='testuser', 
            email='test@test.pl', 
            password='testuse123')
        self.order_status = OrderStatus.objects.create(\
            name="status1",
            description="opis statusu")
        self.order_type = OrderType.objects.create(\
            name="typ1",
            description="opis typu")
        self.implementation_type = ImplementationType.objects.create(\
            name="simpleimplementation")
        self.order = Order.objects.create(\
            user=self.user, 
            care=self.customer, 
            title='testtitle', 
            description='testdescription',
            komunikat="zrobione",
            order_status=self.order_status,
            order_type=self.order_type,
            implementation_type=self.implementation_type,
            start_datetime=datetime.datetime.now(),
            end_datetime=datetime.datetime.now())
    def test_order(self):
        q = Order.objects.get(\
            user=self.user, 
            care=self.customer, 
            title='testtitle', 
            description='testdescription')
        self.assertEqual(self.order, q)
        print("[OK] Utworzono rekordy modelu: Order2")

class Agreement2Test(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(\
            username='testuser123',
            email='test@op.pl',
            password='testasd123')
        self.care = User.objects.create_user(\
            username='caretestuser123',
            email='caretest@op.pl',
            password='caretestasd123')
        self.agreement = Agreement2.objects.create(\
            name='testagreement',
            customer=self.customer,
            care=self.care,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            pakiet="podstawowy",
            subscription=23.6,
            hours=23.5,
            rate=100,
            )
        
    def test_order(self):
        q = Agreement2.objects.get(\
            name='testagreement',
            customer=self.customer,
            care=self.care)
        self.assertEqual(self.agreement, q)
        print("[OK] Utworzono rekordy modelu: Agreement2")




# Testy API ----------------------------------------------------

CREATE_USER_URL = reverse('createuser')
CREATE_ORDERTYPE_URL = reverse('order_type_api-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    def setUp(self):
        """Tworzenie nowego superadmina do testow z tokenem i kluczy obcych dla nastepnych testów"""

        self.superusername = 'admintestapi'
        self.superuserpassword = 'test123asd123api'
        self.superuseremail = 'admin@api.com'
        self.superuser = User.objects.create_superuser(self.superusername, self.superuseremail, self.superuserpassword)
        self.token, created = Token.objects.get_or_create(user=self.superuser)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

                # foreign key setup
        
        # Payloady kluczy obcych
        self.care_payload = {
            'username':'testusercare', 
            'email':'testcare@test.pl', 
            'password':'testpasswordcare'
        }
        self.care_payload_2 = {
            'username':'testuse', 
            'email':'testre@test.pl', 
            'password':'testswordcare'
        }
        self.customer_payload = {
            'username': 'testusercustomer', 
            'email': 'testcustomer@test.pl', 
            'password': 'testpasswordcustomer'
        }
        self.customer_payload_2 = {
            'username': 'testusercustomer2s', 
            'email': 'tetomer@test.pl', 
            'password': 'twordcusmer'
        }
        self.agreement_status_payload = {
            'name': 'statusonline',
            'description': 'statusonline'
        }
        self.agreement_status_payload_2 = {
            'name': 'stat',
            'description': 'statuline'
        }
        self.order_status_payload = {
            'name': 'statustaki',
            'description': 'opis taki'
        }
        self.order_status_payload_2 = {
            'name': 'statustaki2',
            'description': 'opistaki2'
        }
        self.order_type_payload = {
            'name': 'nazwatypu',
            'description': 'opistypu'
        }
        self.order_type_payload_2 = {
            'name': 'nazwatypu2',
            'description': 'opistypu2'
        }
        self.implementation_type_payload = {
            'name': 'typimplementacji'
        }
        self.implementation_type_payload_2 = {
            'name': 'typimplementacji2'
        }

        # Utworzenie kluczy obcych
        self.care = User.objects.create(**self.care_payload)
        self.care_2 = User.objects.create(**self.care_payload_2)
        self.customer = User.objects.create(**self.customer_payload)
        self.customer_2 = User.objects.create(**self.customer_payload_2)
        self.agreement_status = AgreementStatus.objects.create(**self.agreement_status_payload)
        self.agreement_status_2 = AgreementStatus.objects.create(**self.agreement_status_payload_2)
        self.order_status = OrderStatus.objects.create(**self.order_status_payload)
        self.order_status_2 = OrderStatus.objects.create(**self.order_status_payload_2)
        self.order_type = OrderType.objects.create(**self.order_type_payload)
        self.order_type_2 = OrderType.objects.create(**self.order_type_payload_2)
        self.implementation_type = ImplementationType.objects.create(**self.implementation_type_payload)
        self.implementation_type_2 = ImplementationType.objects.create(**self.implementation_type_payload_2)

    def test_if_admintest_exists(self):
        """Sprawdzenie czy istnieje konto testowe admina"""
        print("\n--- API ---")
        self.assertEqual(self.superuser.username, self.superusername)
        self.assertEqual(self.superuser.email, self.superuseremail)
        if self.superuser.username == self.superusername and self.superuser.email == self.superuseremail:
            print("[OK][API] - Konto admina do testow API zostało sprawdzone")
        print("--- API:end ---")
    def test_api_create_with_token(self):
        """Sprawdzenie zapisu nowego uzytkownika za pomoca tokenu admina"""
        print("\n--- API ---")
        
        test_user_payload = {
            "username": "testusername",
            "password": "teststetst",
            "email": "testing@test.pl"
        }
        
        # Logowanie
        login = self.client.login(username='admin', password='asdasd123')
        if self.client.login:
            print("[OK][API] - Zalogowano prawidłowo na konto admina")
        else:
            print("[-][API] - Nie udalo się zalogować na konto admina")

        # POST
        res = self.client.post(CREATE_USER_URL, test_user_payload)
        print("[OK][API] - Wysłano paczke JSON do API")

        # Created?
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print("[OK][API] - utworzono nowe konto za pomocą tokena")

        # GET object
        user = User.objects.get(username=test_user_payload['username'])
        print("[OK][API] - Prawidlowo wybrano usera testowego używając login")

        # Assert
        self.assertEqual(user.username, test_user_payload['username'])
        print("[OK][API] - Prawidłowo sprawdzono usera testowego pod kątem loginu")
        print("--- API:end ---") 
    def test_if_care_exists(self):
        """ Testuje czy obiekt 'care' zostal prawidłowo utworzony w konstruktorze dla następnych testów jednostkowych """
        self.care_get = User.objects.get(**self.care_payload)
        self.care_get_2 = User.objects.get(**self.care_payload_2)
        self.assertEqual(self.care, self.care_get)
        self.assertEqual(self.care_2, self.care_get_2)
        print("[OK][FOREIGN] - Care")
    def test_if_customer_exists(self):
        """ Testuje czy obiekt 'customer' zostal prawidłowo utworzony w konstruktorze dla następnych testów jednostkowych """
        self.customer_get = User.objects.get(**self.customer_payload)
        self.customer_get_2 = User.objects.get(**self.customer_payload_2)
        self.assertEqual(self.customer, self.customer_get)
        self.assertEqual(self.customer_2, self.customer_get_2)
        print("[OK][FOREIGN] - Customer")
    def test_if_agreementsstatus_exists(self):
        """ Testuje czy obiekt 'AgreementStatus' zostal prawidłowo utworzony w konstruktorze dla następnych testów jednostkowych """
        self.agreement_status_get = AgreementStatus.objects.get(**self.agreement_status_payload)
        self.agreement_status_get_2 = AgreementStatus.objects.get(**self.agreement_status_payload_2)
        self.assertEqual(self.agreement_status, self.agreement_status_get)
        self.assertEqual(self.agreement_status_2, self.agreement_status_get_2)
        print("[OK][FOREIGN] - Agreementstatus")
    def test_if_orderstatus_exist(self):
        """ Testuje czy obiekt 'OrderStatus' zostal prawidłowo utworzony w konstruktorze dla następnych testów jednostkowych """
        self.order_status_get = OrderStatus.objects.get(**self.order_status_payload)
        self.order_status_get_2 = OrderStatus.objects.get(**self.order_status_payload_2)
        self.assertEqual(self.order_status, self.order_status_get)
        self.assertEqual(self.order_status_2, self.order_status_get_2)
        print("[OK][FOREIGN] - OrderStatus")
    def test_if_ordertype_exist(self):
        """ Testuje czy obiekt 'OrderStatus' zostal prawidłowo utworzony w konstruktorze dla następnych testów jednostkowych """
        self.order_type_get = OrderType.objects.get(**self.order_type_payload)
        self.order_type_get_2 = OrderType.objects.get(**self.order_type_payload_2)
        self.assertEqual(self.order_type, self.order_type_get)
        self.assertEqual(self.order_type_2, self.order_type_get_2)
        print("[OK][FOREIGN] - OrderType")
    def test_if_implementationtype_exist(self):
        """ Testuje czy obiekt 'ImplementationType' zostal prawidłowo utworzony w konstruktorze dla następnych testów jednostkowych """
        self.implementation_type_get = ImplementationType.objects.get(**self.implementation_type_payload)
        self.implementation_type_get_2 = ImplementationType.objects.get(**self.implementation_type_payload_2)
        self.assertEqual(self.implementation_type, self.implementation_type_get)
        self.assertEqual(self.implementation_type_2, self.implementation_type_get_2)
        print("[OK][FOREIGN] - ImplementationType")

    def test_api_agreement2(self):
        """API: GET/POST/PUT/DELETE na modelu: Agreement2"""    

        model = Agreement2
        API_LIST_URL = "agreement_api-list"
        API_REVERSE_URL = "agreement_api-detail"

        create_payload = {
            "name": "testagreement",
            "customer": self.customer.id,
            "care": self.care.id,
            "start_date": datetime.date(2019, 4, 13),
            "end_date": datetime.date.today(),
            "pakiet": "podstawowy",
            "subscription": 32.5,
            "hours": 22.5,
            "status": self.agreement_status.id,
            "rate": 120.5
        }

        put_payload = {
            "name": "testagreement2",
            "customer": self.customer_2.id,
            "care": self.care_2.id,
            "start_date": datetime.date(2018, 2, 11),
            "end_date": datetime.date(2019, 7, 10),
            "pakiet": "rozszezony",
            "subscription": 322.5,
            "hours": 143,
            "status": self.agreement_status_2.id,
            "rate": 120
        }
    # Fukcje ---------
     # LOGOWANIE 
        print("\n--- API: %s ---" % model)
        login = self.client.login(\
            username='admin', 
            password='asdasd123')
        if self.client.login:
            print("[OK][API] - Zalogowano prawidłowo na konto admina")
        else:
            print("[-][API] - Nie udalo się zalogować na konto admina")
     # POST
        res = self.client.post(reverse(API_LIST_URL), create_payload)
        print("[OK][API-POST] - Wysłano paczke JSON do API -> Model: %s" % str(model))
        # Sprawdzenie Created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print("[OK][API-POST] - utworzono %s" % model)
     # GET
        # Get list
        obj = self.client.get(reverse(API_LIST_URL))
        print("[OK][API-GET-ALL] - Prawidlowo wybrano liste model: %s" % str(model))
        # Get object
        obj = model.objects.get(**create_payload)
        print("[OK][API-GET] - Prawidlowo wybrano model: %s" % str(model))
     # PUT
        print(reverse(API_REVERSE_URL, kwargs={'pk': obj.pk}))
        put = self.client.put(
            reverse(\
                API_REVERSE_URL, 
                kwargs={'pk': obj.pk}),
            data=json.dumps(put_payload, indent=4, sort_keys=True, default=str),
            content_type='application/json'
        )
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        print("[OK][API-PUT] - Zmieniono rekord")
        # Get object po put
        obj = model.objects.get(**put_payload)
        print("[OK][API-PUT>GET] - Prawidlowo wybrano model: %s po PUT" % str(model))
        # Konwersja modelu do słownika i porównanie
        obj_dict = model_to_dict(\
            obj, 
            fields=[field.name for field in obj._meta.fields], 
            exclude=["id"]
            )
        # Assert object
        self.assertEqual(obj_dict, put_payload)
        print("[OK][API-PUT>GET] - Prawidłowo sprawdzono model: %s po PUT" % str(model))  
     # DELETE
        delete = self.client.delete(\
            reverse(API_REVERSE_URL, 
            kwargs={'pk': obj.pk})
            )
        # Assert object
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        print("[OK][API-DELETE] - Usunięto model: %s" % model)
        print("--- API.end: %s ---" % model)
    
    def test_api_order(self):
        """API: GET/POST/PUT/DELETE na modelu: Order"""    

        model = Order
        API_LIST_URL = "order_api-list"
        API_REVERSE_URL = "order_api-detail"

        create_payload = {
            "title": "tytul3",
            "description": "Opis123",
            "komunikat": "",
            "start_datetime": datetime.datetime.combine(datetime.date(2020,1,2), datetime.time(14,4,3)).strftime('%Y-%m-%d %H:%M:%S'),
            "end_datetime": datetime.datetime.combine(datetime.date(2020,1,2), datetime.time(14,4,3)).strftime('%Y-%m-%d %H:%M:%S'),
            "user": self.superuser.id,
            "care": self.care.id,
            "order_status": self.order_status.id,
            "order_type": self.order_type.id,
            "implementation_type": self.implementation_type.id
        }

        put_payload = {
            "title": "tytul5",
            "description": "Opis567",
            "komunikat": "Komunikat developera",
            "user": self.superuser.id,
            "care": self.care_2.id,
            "order_status": self.order_status_2.id,
            "order_type": self.order_type_2.id,
            "implementation_type": self.implementation_type_2.id
        }
    # Fukcje ---------
     # LOGOWANIE 
        print("\n--- API: %s ---" % model)
        login = self.client.login(\
            username='admin', 
            password='asdasd123')
        if self.client.login:
            print("[OK][API] - Zalogowano prawidłowo na konto admina")
        else:
            print("[-][API] - Nie udalo się zalogować na konto admina")
     # POST
        res = self.client.post(reverse(API_LIST_URL), create_payload)
        print("[OK][API-POST] - Wysłano paczke JSON do API -> Model: %s" % str(model))
        # Sprawdzenie Created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print("[OK][API-POST] - utworzono %s" % model)
     # GET
        # Get list
        obj = self.client.get(reverse(API_LIST_URL))
        print("[OK][API-GET-ALL] - Prawidlowo wybrano liste model: %s" % str(model))
        # Get object
        obj = model.objects.get(**create_payload)
        print("[OK][API-GET] - Prawidlowo wybrano model: %s" % str(model))
     # PUT
        print(reverse(API_REVERSE_URL, kwargs={'pk': obj.pk}))
        put = self.client.put(
            reverse(\
                API_REVERSE_URL, 
                kwargs={'pk': obj.pk}),
            data=json.dumps(put_payload, indent=4, sort_keys=True, default=str),
            content_type='application/json'
        )
        print(put.data)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        print("[OK][API-PUT] - Zmieniono rekord")
        # Get object po put
        obj = model.objects.get(**put_payload)
        print("[OK][API-PUT>GET] - Prawidlowo wybrano model: %s po PUT" % str(model))
     # DELETE
        delete = self.client.delete(\
            reverse(API_REVERSE_URL, 
            kwargs={'pk': obj.pk})
            )
        # Assert object
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        print("[OK][API-DELETE] - Usunięto model: %s" % model)
        print("--- API.end: %s ---" % model)

    def test_api_agreementstatus(self):
        """API: GET/POST/PUT/DELETE na modelu: AgreementsStatus"""    

        model = AgreementStatus
        API_LIST_URL = "agreement_status_api-list"
        API_REVERSE_URL = "agreement_status_api-detail"

        create_payload = {
            "name": "testname",
            "description": "testname",
        }
        put_payload = {
            'name': 'putpayload',
            'description': 'putpayload',
        }
    # Fukcje ---------
     # LOGOWANIE 
        print("\n--- API: %s ---" % model)
        login = self.client.login(\
            username='admin', 
            password='asdasd123')
        if self.client.login:
            print("[OK][API] - Zalogowano prawidłowo na konto admina")
        else:
            print("[-][API] - Nie udalo się zalogować na konto admina")
     # POST
        res = self.client.post(reverse(API_LIST_URL), create_payload)
        print("[OK][API-POST] - Wysłano paczke JSON do API -> Model: %s" % str(model))
        # Sprawdzenie Created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print("[OK][API-POST] - utworzono %s" % model)
     # GET
        # Get list
        obj = self.client.get(reverse(API_LIST_URL))
        print("[OK][API-GET-ALL] - Prawidlowo wybrano liste model: %s" % str(model))
        # Get object
        obj = model.objects.get(**create_payload)
        print("[OK][API-GET] - Prawidlowo wybrano model: %s" % str(model))
     # PUT
        put = self.client.put(
            reverse(\
                API_REVERSE_URL, 
                kwargs={'pk': obj.pk}),
            data=json.dumps(put_payload),
            content_type='application/json'
        )
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        print("[OK][API-PUT] - Zmieniono rekord")
        # Get object po put
        obj = model.objects.get(**put_payload)
        print("[OK][API-PUT>GET] - Prawidlowo wybrano model: %s po PUT" % str(model))
        # Konwersja modelu do słownika i porównanie
        # obj_dict = model_to_dict(\
        #     obj, 
        #     fields=[field.name for field in obj._meta.fields], 
        #     exclude=["id"]
        #     )
        # # Assert object
        # self.assertEqual(obj_dict, put_payload)
        # print("[OK][API-PUT>GET] - Prawidłowo sprawdzono model: %s po PUT" % str(model))  
     # DELETE
        delete = self.client.delete(\
            reverse(API_REVERSE_URL, 
            kwargs={'pk': obj.pk})
            )
        # Assert object
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        print("[OK][API-DELETE] - Usunięto model: %s" % model)
        print("--- API.end: %s ---" % model)
    
    def test_api_ordertype(self):
        """API: GET/POST/PUT/DELETE na modelu: OrderType"""    

        model = OrderType
        API_LIST_URL = "order_type_api-list"
        API_REVERSE_URL = "order_type_api-detail"

        create_payload = {
            "name": "testname",
            "description": "testname",
        }
        put_payload = {
            'name': 'putpayload',
            'description': 'putpayload',
        }
    # Fukcje ---------
     # LOGOWANIE 
        print("\n--- API: %s ---" % model)
        login = self.client.login(\
            username='admin', 
            password='asdasd123')
        if self.client.login:
            print("[OK][API] - Zalogowano prawidłowo na konto admina")
        else:
            print("[-][API] - Nie udalo się zalogować na konto admina")
     # POST
        res = self.client.post(reverse(API_LIST_URL), create_payload)
        print("[OK][API-POST] - Wysłano paczke JSON do API -> Model: %s" % str(model))
        # Sprawdzenie Created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print("[OK][API-POST] - utworzono %s" % model)
     # GET
        # Get list
        obj = self.client.get(reverse(API_LIST_URL))
        print("[OK][API-GET-ALL] - Prawidlowo wybrano liste model: %s" % str(model))
        # Get object
        obj = model.objects.get(**create_payload)
        print("[OK][API-GET] - Prawidlowo wybrano model: %s" % str(model))
     # PUT
        put = self.client.put(
            reverse(\
                API_REVERSE_URL, 
                kwargs={'pk': obj.pk}),
            data=json.dumps(put_payload),
            content_type='application/json'
        )
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        print("[OK][API-PUT] - Zmieniono rekord")
        # Get object po put
        obj = model.objects.get(**put_payload)
        print("[OK][API-PUT>GET] - Prawidlowo wybrano model: %s po PUT" % str(model))
        # Konwersja modelu do słownika i porównanie
        # obj_dict = model_to_dict(\
        #     obj, 
        #     fields=[field.name for field in obj._meta.fields], 
        #     exclude=["id"]
        #     )
        # # Assert object
        # self.assertEqual(obj_dict, put_payload)
        # print("[OK][API-PUT>GET] - Prawidłowo sprawdzono model: %s po PUT" % str(model))  
     # DELETE
        delete = self.client.delete(\
            reverse(API_REVERSE_URL, 
            kwargs={'pk': obj.pk})
            )
        # Assert object
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        print("[OK][API-DELETE] - Usunięto model: %s" % model)
        print("--- API.end: %s ---" % model)
    
    def test_api_implementationtype(self):
        """API: GET/POST/PUT/DELETE na modelu: Implementationtype"""    

        model = ImplementationType
        API_LIST_URL = "implementation_type_api-list"
        API_REVERSE_URL = "implementation_type_api-detail"

        create_payload = {
            "name": "testname",
        }
        put_payload = {
            'name': 'putpayload',
        }
    # Fukcje ---------
     # LOGOWANIE 
        print("\n--- API: %s ---" % model)
        login = self.client.login(\
            username='admin', 
            password='asdasd123')
        if self.client.login:
            print("[OK][API] - Zalogowano prawidłowo na konto admina")
        else:
            print("[-][API] - Nie udalo się zalogować na konto admina")
     # POST
        res = self.client.post(reverse(API_LIST_URL), create_payload)
        print("[OK][API-POST] - Wysłano paczke JSON do API -> Model: %s" % str(model))
        # Sprawdzenie Created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print("[OK][API-POST] - utworzono %s" % model)
     # GET
        # Get list
        obj = self.client.get(reverse(API_LIST_URL))
        print("[OK][API-GET-ALL] - Prawidlowo wybrano liste model: %s" % str(model))
        # Get object
        obj = model.objects.get(**create_payload)
        print("[OK][API-GET] - Prawidlowo wybrano model: %s" % str(model))
     # PUT
        put = self.client.put(
            reverse(\
                API_REVERSE_URL, 
                kwargs={'pk': obj.pk}),
            data=json.dumps(put_payload),
            content_type='application/json'
        )
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        print("[OK][API-PUT] - Zmieniono rekord")
        # Get object po put
        obj = model.objects.get(**put_payload)
        print("[OK][API-PUT>GET] - Prawidlowo wybrano model: %s po PUT" % str(model))
        # Konwersja modelu do słownika i porównanie
        # obj_dict = model_to_dict(\
        #     obj, 
        #     fields=[field.name for field in obj._meta.fields], 
        #     exclude=["id"]
        #     )
        # # Assert object
        # self.assertEqual(obj_dict, put_payload)
        # print("[OK][API-PUT>GET] - Prawidłowo sprawdzono model: %s po PUT" % str(model))  
     # DELETE
        delete = self.client.delete(\
            reverse(API_REVERSE_URL, 
            kwargs={'pk': obj.pk})
            )
        # Assert object
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        print("[OK][API-DELETE] - Usunięto model: %s" % model)
        print("--- API.end: %s ---" % model)
    
    def test_api_orderstatus(self):
        """API: GET/POST/PUT/DELETE na modelu: OrderStatus"""     
        
        model = OrderStatus
        API_LIST_URL = "order_status_api-list"
        API_REVERSE_URL = "order_status_api-detail"

        # PAYLOADS
        create_payload = {
            "name": "testname",
            "description": "test2name",
        }
        put_payload = {
            'name': 'putpayload',
            'description': 'putpayload223',
        }
    # Funkcje ---------
     # LOGOWANIE 
        print("\n--- API: %s ---" % model)
        login = self.client.login(\
            username='admin', 
            password='asdasd123')
        if self.client.login:
            print("[OK][API] - Zalogowano prawidłowo na konto admina")
        else:
            print("[-][API] - Nie udalo się zalogować na konto admina")
     # POST
        res = self.client.post(reverse(API_LIST_URL), create_payload)
        print("[OK][API-POST] - Wysłano paczke JSON do API -> Model: %s" % str(model))
        # Sprawdzenie Created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print("[OK][API-POST] - utworzono %s" % model)
     # GET
        # Get list
        obj = self.client.get(reverse(API_LIST_URL))
        print("[OK][API-GET-ALL] - Prawidlowo wybrano liste model: %s" % str(model))
        # Get object
        obj = model.objects.get(**create_payload)
        print("[OK][API-GET] - Prawidlowo wybrano model: %s" % str(model))
     # PUT
        put = self.client.put(
            reverse(\
                API_REVERSE_URL, 
                kwargs={'pk': obj.pk}),
            data=json.dumps(put_payload),
            content_type='application/json'
        )
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        print("[OK][API-PUT] - Zmieniono rekord")
        # Get object po put
        obj = model.objects.get(**put_payload)
        print("[OK][API-PUT>GET] - Prawidlowo wybrano model: %s po PUT" % str(model))
        # Konwersja modelu do słownika i porównanie
        # obj_dict = model_to_dict(\
        #     obj, 
        #     fields=[field.name for field in obj._meta.fields], 
        #     exclude=["id"]
        #     )
        # # Assert object
        # self.assertEqual(obj_dict, put_payload)
        # print("[OK][API-PUT>GET] - Prawidłowo sprawdzono model: %s po PUT" % str(model))  
     # DELETE
        delete = self.client.delete(\
            reverse(API_REVERSE_URL, 
            kwargs={'pk': obj.pk})
            )
        # Assert object
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        print("[OK][API-DELETE] - Usunięto model: %s" % model)
        print("--- API.end: %s ---" % model)
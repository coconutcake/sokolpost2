from django.urls import path,include, re_path
from django.conf.urls import url
from . import views
from .views import *
from django.contrib import admin
from django.views.generic.base import TemplateView 
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.views.static import serve 
from HD_app.settings import SIMULATION_MODE
from django.contrib.auth import views as auth_views
# Ruter API ---------------------------------------------------------
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'profiletypes', views.ProfileTypeViewSet)
router.register(r'message', views.MessagesListView, 'message_api')
router.register(r'message', views.MessagesListView)
router.register(r'order', views.OrderListView, 'order_api')
router.register(r'order', views.OrderListView)
router.register(r'order_status', views.OrderStatusListView, 'order_status_api')
router.register(r'order_status', views.OrderStatusListView)
router.register(r'order_type', views.OrderTypeListView, 'order_type_api')
router.register(r'order_type', views.OrderTypeListView)
router.register(r'implementation_type', views.ImplementationTypeListView, 'implementation_type_api')
router.register(r'implementation_type', views.ImplementationTypeListView)
router.register(r'pakiet', views.PakietListView, 'pakiet_api')
router.register(r'document', views.DocumentListView)
router.register(r'document_status', views.DocumentStatusListView, 'document_status_api')
router.register(r'distancecalcprofile', views.DistanceCalcProfileListView)
router.register(r'distancecalcprofile', views.DistanceCalcProfileListView, 'distancecalcprofile_api')
router.register(r'address', views.AddressListView)
router.register(r'address', views.AddressListView, 'address_api')
router.register(r'rate', views.RateListView)
router.register(r'ratestack', views.RateStackListView)
router.register(r'ratestack', views.RateStackListView, 'ratestack_api')
router.register(r'document_status', views.DocumentStatusListView)
router.register(r'profile', views.ProfileListView, 'profile_api')
router.register(r'profile', views.ProfileListView)
router.register(r'usersettings', views.UserSettingsView)
router.register(r'usersettings', views.UserSettingsView, 'usersettings_api')

from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView,
)



urlpatterns = [
# API
    path('api/', include(router.urls,)),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('api/create/user/', views.CreateUserView.as_view(),name='createuser'),
    path('api/token/', views.CreateTokenView.as_view(),name='token'),
# Konta
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    url('^', include('django.contrib.auth.urls')), 
# Redirecty 
    url(r'^api/$', RedirectView.as_view(url='/'), name='api-router'),
    url(r'^admin/$', RedirectView.as_view(url='/'), name='admin-page'),  
# Zmiana hasła
    url(r'^pwdchange/$', views.change_password, name='change_password'),
    url(r'^masspwdchange/$', views.MassPasswordChange.as_view(), name='User_reset_ajax'),
    path('<int:user_pk>/pwdreset/', views.MyPasswordResetView.as_view(), name='my_password_reset'),
# Dashboard
    path('', views.home, name='home'),
    url(r'dashboard/', views.DashboardView.as_view(), name='DashboardView'),

# Obiekty subiekta -----------------------------------------------
    # Firmy
    url(r'^company_add/$', views.SubiektCompanyCreateView.as_view(),\
    name='SubiektCompany_add'),
    url(r'^company_detail/$', views.SubiektCompanyDetailView.as_view(),\
    name='SubiektCompany_detail'),


# Obiekty django -------------------------------------------------
    # Użytkownicy
    url(r'^user_add/$', views.UserCreateView.as_view(),\
        name='User_add'),
    url(r'^user_detail/(?P<pk>\d+)/$', views.UserDetailView.as_view(),\
        name='User_detail'),
    url(r'^user_delete/(?P<pk>\d+)/delete/$',views.UserDeleteView.as_view(),\
        name='User_delete'),
    url(r'^user_delete_ajax/$',views.UserDeleteAjax.as_view(),\
        name='User_delete_ajax'),

    # Umowy i raporty
    url(r'^raport/$', views.DocumentRaportView.as_view(),\
    name='Raport'),
    url(r'^raport_search/$', views.RaportSearchAjax.as_view(),\
        name='Raport_search_ajax'),

    # Umowy 
    url(r'^document_add/$', views.DocumentCreateView.as_view(),\
        name='Document_add'),
    url(r'^document_detail/(?P<pk>\d+)/$', views.DocumentDetailView.as_view(),\
        name='Document_detail'),
    url(r'^document_delete_ajax/$',views.DocumentDeleteAjax.as_view(),\
        name='Document_delete_ajax'),

    # Wiadomości
    url(r'^message_add/$', views.MessageCreateView.as_view(),\
        name='Message_add'),
    url(r'^message_detail/$', views.MessageDetailView.as_view(),\
        name='Message_detail'),
    url(r'^message_delete/$', views.MessageDeleteAjax.as_view(),\
        name='Message_delete_ajax'),
    
    # Adresy
    url(r'^address_add/$', views.AddressCreateView.as_view(),\
        name='Address_add'),
    url(r'^address_delete_ajax/$',views.AddressDeleteAjax.as_view(),\
        name='Address_delete_ajax'),

    # Zlecenia
    url(r'^order_add/$', views.OrderCreateView.as_view(),\
        name='Order_add'),
    url(r'^order_detail/(?P<pk>\d+)/$', views.OrderDetailView.as_view(),\
        name='Order_detail'),
    url(r'^order_delete/$', views.OrderDeleteAjax.as_view(),\
        name='Order_delete_ajax'),
    url(r'^order_delete/$', views.OrderDeleteAjax.as_view(),\
        name='Order_delete_ajax'),
    url(r'^order_delete2/$', views.OrderDeleteAjax2.as_view(),\
        name='Order_delete_ajax2'),
    url(r'^order_account/$', views.OrderAccountAjax.as_view(),\
        name='Order_account_ajax'),

#Umowy 

    # url(r'^agreement_detail/(?P<pk>\d+)/$',views.AgreementViewDetails.as_view(),\
    #     name='Agreement_detail'),
    # url(r'^agreement_delete/(?P<pk>\d+)/delete/$', views.AgreementViewDelete.as_view(),\
    #     name='Agreement_delete'),
### Pakiet
    # url(r'pakiet_add/$',views.PakietView.as_view(),\
    #     name="Pakiet_add"),
### OrderTemplate
    # url(r'ordertemplate_add/$',views.OrderTemplateView.as_view(),\
    #     name="OrderTemplate_add"),
### Zlecenia 
    # url(r'^order_add/$', views.OrderView.as_view(),\
    #     name='Order_add'),
    # url(r'^order_detail/(?P<pk>\d+)/$', views.OrderViewDetails.as_view(), \
    #     name='Order_detail'),
    # url(r'^order_delete/(?P<pk>\d+)/delete/$', views.OrderViewDelete.as_view(),\
    #     name='Order_delete'),
### Profil
    # url(r'^profile_detail/(?P<pk>\d+)/$', views.ProfileViewDetails.as_view(), \
    #     name='Profile_detail'),
### JSON
    url(r'^JSON_load_cares/$', views.JSON_load_cares,\
        name='JSON_load_cares'),
    url(r'^JSON_load_addresses/$', views.JSON_load_addresses,\
        name='JSON_load_addresses'),
    url(r'^JSON_rozlicz_zlecenie/$', views.JSON_rozlicz_zlecenie,\
        name='JSON_rozlicz_zlecenie'),
    url(r'^JSON_sumuj_zlecenia/$', views.JSON_sumuj_zlecenia,\
        name='JSON_sumuj_zlecenia'),  
    url(r'^JSON_load_order_template/$', views.JSON_load_order_template,\
        name='JSON_load_order_template'),  
### Fltry 
    # url(r'^orderfilter/$', views.Raport1View.as_view(),\
    #     name='Raport_Order_1'),
    # url(r'^orderagrfilter/$', views.Raport2View.as_view(),\
    #     name='Raport_Agreement_1'),
### Raporty
    # url(r'^orderfilter_raport/$', views.GenerateRaport.as_view(),\
    # name='Generate_raport'),
### Rozliczanie zleceń
    # url(r'^account_orders/$', views.AccountOrders.as_view(),\
    # name='AccountOrders'),
### Filtry
    # path('orderfilter_/', views.Raport1View_filteredByTime.as_view(), name="Raport_1_filteredByTime"),
    # path('orderagrfilter_/', views.OrderAgreement1View_filteredByTime.as_view(), name="Raport_1_order_agreement_filteredByTime"),
    # path('raport_agree_1_filteredbytime/', views.Agreement1View_filteredByTime.as_view(), name="Raport_agree_1_filteredByTime"),



### SubiektAPI
    url(r'^subiektapi/$', views.SubiektAPI.as_view(),\
    name='SubiektAPI'),
    url(r'^subiektapi/$', views.SubiektAPI.as_view(),\
    name='SubiektAPI'),
    url(r'^subiektstatus/$', views.SubiektStatus.as_view(),\
    name='SubiektStatus'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serwowanie static -----------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    urlpatterns += re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


from django.views.decorators.csrf import csrf_exempt

if SIMULATION_MODE:
    urlpatterns.append(url(r'^simulation/kontrahenci', csrf_exempt(views.SimulationKontrahenci.as_view()), name='SimulationKontrahenci'))
    
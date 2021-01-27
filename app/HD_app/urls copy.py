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

from django.contrib.auth import views as auth_views
# Ruter API ---------------------------------------------------------
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'profiletypes', views.ProfileTypeViewSet)
router.register(r'customer', views.CustomerListView, 'customer_api')
router.register(r'customer', views.CustomerListView)
router.register(r'message', views.MessagesListView, 'message_api')
router.register(r'message', views.MessagesListView)
router.register(r'order', views.OrderListView, 'order_api')
router.register(r'order', views.OrderListView)
router.register(r'serviceorder', views.ServiceOrderView)
router.register(r'serviceorder', views.ServiceOrderView, 'serviceorder_api')
router.register(r'order_status', views.OrderStatusListView, 'order_status_api')
router.register(r'order_status', views.OrderStatusListView)
router.register(r'order_type', views.OrderTypeListView, 'order_type_api')
router.register(r'order_type', views.OrderTypeListView)
router.register(r'implementation_type', views.ImplementationTypeListView, 'implementation_type_api')
router.register(r'implementation_type', views.ImplementationTypeListView)
router.register(r'pakiet', views.PakietListView, 'pakiet_api')
router.register(r'agreement', views.AgreementListView)
router.register(r'agreement_status', views.AgreementStatusListView, 'agreement_status_api')
router.register(r'distancecalcprofile', views.DistanceCalcProfileListView)
router.register(r'distancecalcprofile', views.DistanceCalcProfileListView, 'distancecalcprofile_api')
router.register(r'address', views.AddressListView)
router.register(r'address', views.AddressListView, 'address_api')
router.register(r'rate', views.RateListView)
router.register(r'ratestack', views.RateStackListView)
router.register(r'ratestack', views.RateStackListView, 'ratestack_api')
router.register(r'agreement_status', views.AgreementStatusListView)
router.register(r'profile', views.ProfileListView, 'profile_api')
router.register(r'profile', views.ProfileListView)
router.register(r'company', views.CompanyListView, 'company_api')
router.register(r'company', views.CompanyListView)
router.register(r'usersettings', views.UserSettingsView)
router.register(r'usersettings', views.UserSettingsView, 'usersettings_api')
router.register(r'news', views.NewsView)
router.register(r'news', views.NewsView, 'news_api')
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView,
)

urlpatterns = [

#Administracja ---------------------------------------------------
    path('api/', include(router.urls,)),
    path('api-auth/', include('rest_framework.urls', \
        namespace='rest_framework')),
    path('api/create/user/', views.CreateUserView.as_view(), \
        name='createuser'),
    path('api/token/', views.CreateTokenView.as_view(), \
        name='token'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    url('^', include('django.contrib.auth.urls')), 
#Do zrobienia strony ---------------------------------------------
    path('mystats/',views.mystats, name='mystats'),
#Redirecty -------------------------------------------------------
    url(r'^api/$', RedirectView.as_view(url='/'), name='api-router'),
    url(r'^admin/$', RedirectView.as_view(url='/'), name='admin-page'),
#Zmiana hasła
    url(r'^pwdchange/$', views.change_password, name='change_password'),
    url(r'^masspwdchange/$', views.MassPasswordChange.as_view(), name='User_reset_ajax'),
    path('<int:user_pk>/pwdreset/', views.MyPasswordResetView.as_view(), name='my_password_reset'),
    #path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="HD_app/password_reset_form.html",success_url='Company_add'), name='password_reset_confirm'),
    #path('done/', PasswordResetCompleteView.as_view(success_url=reverse_lazy('Company_add')), name='password_reset_complete'),
    #path('password_reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#Dashboard
    path('', views.home, name='home'),
    url(r'dashboard/', views.DashboardView.as_view(),\
        name='DashboardView'),
#Klienci
    url(r'^company_add/$', views.CompanyView.as_view(),\
        name='Company_add'),
    url(r'^company_detail/(?P<pk>\d+)/$', views.CompanyViewDetails.as_view(), \
        name='Company_detail'),
    url(r'^company_delete/(?P<pk>\d+)/delete/$',views.CompanyViewDelete.as_view(),\
        name='Company_delete'),
url(r'^company_delete_ajax/$',views.CompanyDeleteAjax.as_view(),\
        name='Company_delete_ajax'),
#Klienci old
    url(r'^company_add_old/$', views.CompanyView_old.as_view(),\
        name='Company_add_old'),
    url(r'^company_detail_old/(?P<pk>\d+)/$', views.CompanyViewDetails_old.as_view(), \
        name='Company_detail_old'),
    url(r'^company_delete_old/(?P<pk>\d+)/delete/$',views.CompanyViewDelete_old.as_view(),\
        name='Company_delete_old'),
    
#Użytkownicy
    url(r'^user_add/$', views.UserView.as_view(),\
        name='User_add'),
    url(r'^user_detail/(?P<pk>\d+)/$', views.UserViewDetails.as_view(), \
        name='User_detail'),
    url(r'^user_delete/(?P<pk>\d+)/delete/$',views.UserViewDelete.as_view(),\
        name='User_delete'),
    url(r'^user_delete_ajax/$',views.UserDeleteAjax.as_view(),\
        name='User_delete_ajax'),
#Adresy
    url(r'^address_add/$', views.AddressView.as_view(),\
        name='Address_add'),
    url(r'^address_detail/(?P<pk>\d+)/$',views.AddressViewDetails.as_view(),\
        name='Address_detail'),
    url(r'^address_delete/(?P<pk>\d+)/delete/$', views.AddressViewDelete.as_view(),\
        name='Address_delete'),
#Umowy 
    url(r'^agreement_add/$', views.AgreementView.as_view(),\
        name='Agreement_add'),
    url(r'^agreement_detail/(?P<pk>\d+)/$',views.AgreementViewDetails.as_view(),\
        name='Agreement_detail'),
    url(r'^agreement_delete/(?P<pk>\d+)/delete/$', views.AgreementViewDelete.as_view(),\
        name='Agreement_delete'),
### Pakiet
    url(r'pakiet_add/$',views.PakietView.as_view(),\
        name="Pakiet_add"),
### OrderTemplate
    url(r'ordertemplate_add/$',views.OrderTemplateView.as_view(),\
        name="OrderTemplate_add"),
### Zlecenia 
    url(r'^order_add/$', views.OrderView.as_view(),\
        name='Order_add'),
    url(r'^order_detail/(?P<pk>\d+)/$', views.OrderViewDetails.as_view(), \
        name='Order_detail'),
    url(r'^order_delete/(?P<pk>\d+)/delete/$', views.OrderViewDelete.as_view(),\
        name='Order_delete'),
### Profil
    url(r'^profile_detail/(?P<pk>\d+)/$', views.ProfileViewDetails.as_view(), \
        name='Profile_detail'),
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
    url(r'^orderfilter/$', views.Raport1View.as_view(),\
        name='Raport_Order_1'),
    url(r'^orderagrfilter/$', views.Raport2View.as_view(),\
        name='Raport_Agreement_1'),
### Raporty
    url(r'^orderfilter_raport/$', views.GenerateRaport.as_view(),\
    name='Generate_raport'),
### Rozliczanie zleceń
    url(r'^account_orders/$', views.AccountOrders.as_view(),\
    name='AccountOrders'),
### Filtry
    path('orderfilter_/', views.Raport1View_filteredByTime.as_view(), name="Raport_1_filteredByTime"),
    path('orderagrfilter_/', views.OrderAgreement1View_filteredByTime.as_view(), name="Raport_1_order_agreement_filteredByTime"),
    path('raport_agree_1_filteredbytime/', views.Agreement1View_filteredByTime.as_view(), name="Raport_agree_1_filteredByTime"),
# Msg
    url(r'^msg/$', views.MessageCreateView.as_view(),\
    name='MessageCreateView'),
    url(r'^msg/detail/$', views.MessageDetailView.as_view(),\
    name='MessageDetailView'),
    url(r'^msg/delete/$', views.MessageDeleteAjax.as_view(),\
    name='MessageDeleteAjax'),


### SubiektAPI
    url(r'^subiektapi/$', views.SubiektAPI.as_view(),\
    name='SubiektAPI'),
    url(r'^subiektapi/$', views.SubiektAPI.as_view(),\
    name='SubiektAPI'),
    url(r'^subiektstatus/$', views.SubiektStatus.as_view(),\
    name='SubiektStatus'),


### SubiektAPI firma    
    url(r'^subiektapi/firma/$', views.SubiektAPICompanyCreateView.as_view(),\
    name='SubiektAPICompanyCreateView'),
    # url(r'^subiektapi/list/firma/$', views.SubiektAPICompanyListView.as_view(),\
    # name='SubiektAPICompanyListView'),
    url(r'^subiektapi/detail/firma/$', views.SubiektAPICompanyDetailView.as_view(),\
    name='SubiektAPICompanyDetailView'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serwowanie static -----------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    urlpatterns += re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
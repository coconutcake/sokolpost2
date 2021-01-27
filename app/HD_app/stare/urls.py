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
router.register(r'agreement', views.AgreementListView, 'agreement_api')
router.register(r'agreement', views.AgreementListView)
router.register(r'agreement_status', views.AgreementStatusListView, 'agreement_status_api')
router.register(r'agreement_status', views.AgreementStatusListView)
router.register(r'profile', views.ProfileListView, 'profile_api')
router.register(r'profile', views.ProfileListView)
router.register(r'company', views.CompanyListView, 'company_api')
router.register(r'company', views.CompanyListView)
router.register(r'usersettings', views.UserSettingsView)
router.register(r'usersettings', views.UserSettingsView, 'usersettings_api')
router.register(r'news', views.NewsView)
router.register(r'news', views.NewsView, 'news_api')



urlpatterns = [

# Administracja ---------------------------------------------------
    path('api/', include(router.urls,)),
    path('api-auth/', include('rest_framework.urls', \
        namespace='rest_framework')),
    path('api/create/user/', views.CreateUserView.as_view(), \
        name='createuser'),
    path('api/token/', views.CreateTokenView.as_view(), \
        name='token'),
    path('admin/', admin.site.urls),
    path('sys_info/', views.sys_info, name='sys_info'),
    path('accounts/', include('django.contrib.auth.urls')),
    
# Do zrobienia strony ---------------------------------------------
    # path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('register2/', views.register2, name='register2'),
    path('register3/', views.register3, name='register3'),

# Quaries ---------------------------------------------------------
    path('orders_length/', views.orders_length, name='orders_length'),
    path('counters/', views.counters, name='counters'),

# Searche ---------------------------------------------------------
    path('search_orders/', views.SearchOrdersView.as_view(), name="search_orders"),

# Zlecenia IT -----------------------------------------------------
    url(r'^myorders1/$', views.Order1.as_view(), name='orders1'),
    url(r'^myorders1/(?P<pk>\d+)/$', views.OrderDetails.as_view(), \
        name='order_detail'),
    url(r'^myorders1/(?P<pk>\d+)/delete/$', views.OrderDelete.as_view(), \
        name='order_delete'),
    url(r'^myorders1_not_completed/$', views.Order1_not_completed.as_view(), name='orders1_not_completed'),
    url(r'^myorders1_completed/$', views.Order1_completed.as_view(), name='orders1_completed'),

# Zlecenia uzytkownika --------------------------------------------
    url(r'^myorders2/$', views.Order2.as_view(), name='orders2'),
    url(r'^myorders2/(?P<pk>\d+)/$', views.Order2Details.as_view(), name='order_detail2'),
    url(r'^myorders2/(?P<pk>\d+)/delete/$', views.Order2Delete.as_view(), \
        name='order_delete2'),

    url(r'^ord/$',views.OrdView.as_view(),name='ord'),


# Zlecenia serwisowe ----------------------------------------------
    url(r'^myserviceorders1/$', views.ServiceOrder1.as_view(), name='service_orders1'),
    url(r'^myserviceorders1/(?P<pk>\d+)/$', views.ServiceOrderDetails.as_view(), name='serviceorder_detail'),
    url(r'^myserviceorders1/(?P<pk>\d+)/delete/$', views.ServiceOrderDelete.as_view(), \
        name='serviceorder_delete'),

# Umowy -----------------------------------------------------------
    url(r'^agreements/$', views.Agreement.as_view(), name='agreements'),
    url(r'^agreements/(?P<pk>\d+)/$', views.AgreementEdit.as_view(), name='agreement_detail'),
    url(r'^agreements/(?P<pk>\d+)/delete/$', views.AgreementDelete.as_view(), \
        name='agreement_delete'),

# Wiadomości ------------------------------------------------------
    url(r'^messages/$', views.Messages.as_view(), name='messages'),
    url(r'^messages/(?P<pk>\d+)/delete/$', views.MessageDelete.as_view(), \
        name='message_delete'),

# Firmy -----------------------------------------------------------
    # url(r'^companies/$', views.CompanyView.as_view(), name='companies'),
    # url(r'^companies/(?P<pk>\d+)/$', views.CompanyEditView.as_view(), name='Company_detail'),


    url(r'^stats/$', views.Stats.as_view(), name='stats'),
    path('readms/', views.readms, name='readms'),

# Stare strony ----------------------------------------------------
    path('ordertypes/', views.OrderTypeView.as_view(), \
        name='ordertypes'),
    path('ordertypes/<int:pk>', views.OrderTypeView.as_view(), \
        name='ordertypes'),

    path('orders/', views.OrderView.as_view(), \
        name='orders'),
    path('myorders/', views.OrdersView.as_view(), \
        name='myorders'),



    path('implementations/', views.ImplementationTypeView.as_view(), \
        name='implementations'),
    path('implementations/<int:pk>', views.ImplementationTypeView.as_view(), \
        name='implementations'),


    path('entry/', views.entry, name='entry'),

    path('mystats/',views.mystats, name='mystats'),
    path('', views.basehome, name='home'),
    # path('customers/<int:pk>', views.CustomerView.as_view(), \
    #     name='customer'),

# Wejscia
    path('getharwareinfo/', views.gethardwareinfo, name='gethardwareinfo'),

# Redirecty -------------------------------------------------------
    url(r'^api/$', RedirectView.as_view(url='/'), name='api-router'),
    url(r'^admin/$', RedirectView.as_view(url='/'), name='admin-page'),


# -----------------------------------------------------------------
# Stara sowa ------------------------------------------------------
# -----------------------------------------------------------------

# Klienci 
    url(r'^company_add/$', views.CompanyView.as_view(),name='Company_add'),
    url(r'^company_detail/(?P<pk>\d+)/$', views.CompanyViewDetails.as_view(), \
        name='Company_detail'),
    url(r'^company_delete/(?P<pk>\d+)/delete/$', \
        views.CompanyViewDelete.as_view(),name='Company_delete'),

# Użytkownicy
    url(r'^user_add/$', views.UserView.as_view(),name='User_add'),
    url(r'^user_detail/(?P<pk>\d+)/$', views.UserViewDetails.as_view(), \
        name='User_detail'),
    url(r'^user_delete/(?P<pk>\d+)/delete/$', \
        views.UserViewDelete.as_view(),name='User_delete'),

# Umowy
    url(r'^agreement_add/$', views.AgreementView.as_view(),name='Agreement_add'),
    url(r'^agreement_detail/(?P<pk>\d+)/$', views.AgreementViewDetails.as_view(), \
        name='Agreement_detail'),
    url(r'^agreement_delete/(?P<pk>\d+)/delete/$', \
        views.AgreementViewDelete.as_view(),name='Agreement_delete'),



# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Serwowanie static -----------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    urlpatterns += re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
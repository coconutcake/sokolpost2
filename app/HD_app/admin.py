from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.site_header = "Sokół"
admin.site.site_title = "Administracja Sokół"
admin.site.index_title = "Witaj w panelu administracyjnym Sokół"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):



    list_display = ['user','user_firstname','user_lastname','typ','id', 'idf', 'thumb']
    readonly_fields = ('user', 'idf', 'tablef', 'user_id', 'user_firstname', 'user_lastname', 'user_email', 'user_email2', 'custom_field',)
    inlines = []
    list_filter = ('typ',)
    search_fields = ['user__email','user__first_name', 'user__last_name']

    def user_id(self,obj):
        return format_html('<p style="color: red; font-weight:bold;">{}</p>', obj.user.id)
        # return obj.user.id
    def user_firstname(self,obj):
        return obj.user.first_name
    def user_lastname(self,obj):
        return obj.user.last_name
    def user_email(self,obj):
        return obj.user.email
    def user_email2(self,obj):
        return obj.user.email


    def custom_field(self, obj):
        return format_html('<a href={}>URL</a>', obj.url)

    fieldsets = (
        ("Uzytkownik powiązany", {
            # 'classes': ('wide', 'extrapretty'),
            "description": format_html("<p style='padding: 1rem;color: red; background: #EBEBEB;'><i>Ten uzytkownik znajduje sie w tablicy <b>auth.user</b> a jego dane mogą być zmienione tylko z poziomu tabeli nadrzednej. Mowych użytkowników należy dodawać również z poziomu <b>Użytkownicy</b> gdyż tylko w ten sposób dane zostaną skopiowane do <b>Profile użytkowników</b> do tabeli <b>hd_app_profile</b></i></p>"),
            "fields": (
                'user_id',
                'tablef',
                'idf',
                'user',
                'typ',
                'group',
            ),
        }),

        ("Dodatkowe", {
            'classes': ('collapse',),
            "fields": (
                'user_firstname',
                'user_lastname',
                'user_email',
                'thumb',
                'cellphone',
            ),
        }),

        ("Inne", {
            "description": "Te informacje znajdują sie w tabeli hd_app.profile",
            
            "fields": (

                
            ),
        }),
        
    )
@admin.register(ProfileType)
class ProfileType(admin.ModelAdmin):
    def id_name(self, obj):
        return "id:%s | %s" % (obj.id, obj.name)

    list_display = ['name', 'description', 'id']
@admin.register(OrderType)
class OrderType(admin.ModelAdmin):
    list_display = ['name', 'description', 'id']
@admin.register(Order2)
class Order2(admin.ModelAdmin):

    list_display = [\
        'name',
        'created_date', 
        'order_type',
        'order_status',
        'id']
    list_filter = (\
        'created_date', 
        'document',
        'order_type',
        'order_status',
        )
    search_fields = (\
        'document',
        )
@admin.register(ImplementationType)
class ImplementationType(admin.ModelAdmin):
    list_display = ['name', 'id']
@admin.register(OrderStatus)
class OrderStatus(admin.ModelAdmin):
    list_display = ['name', 'id']
@admin.register(Document)
class Document(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields=('company_sfk', )
@admin.register(Pakiet)
class Pakiet(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(Rate)
class Rate(admin.ModelAdmin):
    list_display = ('name','start','stop','price','is_default')
    ordering = ('-is_default',)
@admin.register(RateStack)
class RateStack(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(UserSettings)
class UserSettings(admin.ModelAdmin):
    list_display = ['user', 'email_notifications']
    search_fields = (\
    'user',
    )
    list_filter = (\
        'email_notifications', 
    )
@admin.register(OrderTemplate)
class OrderTemplate(admin.ModelAdmin):
    list_display = ['name', 'description',]
@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ['name', 'description','id']
@admin.register(DistanceCalcProfile)
class DistanceCalcProfile(admin.ModelAdmin):
    list_display = ['name', 'cost']
@admin.register(ProfileGroup)
class ProfileGroup(admin.ModelAdmin):
    list_display = ['name']
@admin.register(Address2)
class Address2(admin.ModelAdmin):
    list_display = ['id','name', 'company_sfk', 'distance', 'city', 'is_default']
@admin.register(OrderCategory)
class OrderCategory(admin.ModelAdmin):
    list_display = ['name', 'id']
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name','id']

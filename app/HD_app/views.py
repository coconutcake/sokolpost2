# Imports -------------------------------------------------
from .imports import *
from django.db.models import CharField,DurationField,DateTimeField, ExpressionWrapper, F
import functools 
# Klasy pomocnicze Subiekta API ---------------------------
class SubiektFormOperations():
    """ Klasa operacji na ciele formularza ajax """
    def __init__(self,*args,**kwargs):
        pass

    def get_form_data(self,request,*args,**kwargs):
        """ Wybiera dane z przesłanego formularza z 'data' """
        for key,value in json.loads(request.POST.get('data', ''))[0].items():
            if key == kwargs.get("form"):
                print(print("{0} - Formularz: {1}".format(get_current_datetime(),key)))
                data = json.loads(request.POST.get('data', ''))
                l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
                q = QueryDict(l)
                return q 

    def is_form_in_data(self,request,*args,**kwargs):
        """ Sprawdza czy są dane w formularzu pod kluczem 'data' """
        for key,value in json.loads(request.POST.get('data', ''))[0].items():
            if key == kwargs.get("formid"):
                return True

    def get_subiekt_data(self,request,*args,**kwargs):
        """ Wysyła dane formularza do subiekta i zwraca odebrane dane """
        form = kwargs['form']
        endpoint = kwargs['endpoint']
        cleaned_data = form.cleaned_data
        print("{0} - Endpoint do wysyłki: {1}".format(get_current_datetime(),endpoint))
        print("{0} - Wysyłam paczke na endpoint subiekta...:\n{1}".format(get_current_datetime(),cleaned_data))
        r = requests.post(endpoint,data=json.dumps(cleaned_data),headers=subiekt.get_header(),verify=False)
        print("{0} - Odebrano:\n{1}".format(get_current_datetime(),r.json()))
        return r

    def get_subiekt_object(self,request, *args, **kwargs):
        """ Wysyla dane otrzymane przez ajax do subiekta i zwraca odebrane dane """
        endpoint = kwargs['endpoint']
        data = self.get_ajax_data(request,*args,**kwargs)
        print(f"{get_current_datetime()} - Wysyłam do {endpoint}\n{data}")
        obj = requests.post(endpoint,data=json.dumps(data),headers=subiekt.get_header(),verify=False)
        print(f"{get_current_datetime()} - Odebrano: \n{obj.json()}")

        # Musi byc 1 obiekt 
        # q = QueryDict(obj)
        return obj.json().get("KontrahenciList")

    def get_ajax_data(self,request,*args,**kwargs):
        """ Zwraca 'data' z ajax """
        return json.loads(request.GET.get("data",""))
    def replace_ajax_form_fields(self,fields_replacement_matrix,form_data):  
        """ Zamienia wskazane pola formularza wg matrycy """   
        changed = {}
        print(dict(form_data))
        for k,v in dict(form_data).items():
            if k in fields_replacement_matrix.keys():
                value = fields_replacement_matrix[k]
                obj = {value:v}
                changed.update(obj)
        print(f"Zamieniono pola wg matrycy: {fields_replacement_matrix}")
        print(changed)
        return changed
            


    def is_data(self,request,*args,**kwargs):
        """ Sprawdza czy jest klucz 'data' w paczce ajax """
        if json.loads(request.GET.get("data",None)):
            return True
        else:
            return False
class SubiektStatus(View):
    """ Widok do odpytywania statusu subiekta """
    def get(self,request,*args,**kwargs):
        context = {}
        if subiekt.is_up():
            context['status'] = status.HTTP_200_OK
            return JsonResponse(context)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            return JsonResponse(context)

@method_decorator(staff_member_required,name='dispatch')
class DashboardView(LoginRequiredMixin,View):
    """ Dashboard """
    template_name = "HD_app/subiekt/dashboard/dashboard.html"
    model_order = Order2


    def get(self,request,*args,**kwargs):
        self.request = request
        return render(request, self.template_name, self.get_context(request,*args,**kwargs))

    def get_context(self,request,*args,**kwargs):
        context = {
            "inbox":Message.objects.filter(receipt=request.user),
            "sent": Message.objects.filter(sender=request.user),
            "get_current_month_days":self.get_current_month_days(),
            "get_my_current_month_orders_counter":self.get_my_current_month_orders_counter(),
            "get_my_current_month_orders_counter_completed":self.get_my_current_month_orders_counter_completed(),
            "get_my_current_month_orders_counter_notcompleted":self.get_my_current_month_orders_counter_notcompleted(),
            "get_my_current_month_orders_counter_status_all":self.get_my_current_month_orders_counter_status_all(),
            "get_month_orders_statuses":self.get_month_orders_statuses(),
            "get_month_orders_types":self.get_month_orders_types(),
            "get_not_completed_orders":self.get_not_completed_orders(),
            "get_completed_orders":self.get_completed_orders(),
            "get_my_current_month_orders_counter_in_progress":self.get_my_current_month_orders_counter_in_progress(),
            "get_my_current_month_orders_counter_spent":self.get_my_current_month_orders_counter_spent(),
            "get_my_current_month_orders_counter_costs":self.get_my_current_month_orders_counter_costs(),
            "get_orders_sum_costs":self.get_orders_sum_costs(),
            "get_orders_sum_travel_costs":self.get_orders_sum_travel_costs(),
            "get_orders_sum_costs_with_travel": self.get_orders_sum_costs_with_travel(),
            "get_orders_counter": self.get_orders_counter(),
            "get_orders_two_way_distance": self.get_orders_two_way_distance(),
            "get_orders_sum_time":self.get_orders_sum_time(),
            "user":User.objects.get(pk=request.user.pk),
            "get_month_companies_spent":self.get_month_companies_spent(),
            "get_month_companies_costs":self.get_month_companies_costs()
            
        }
        return context 

    def get_objects(self):
        """ Zwraca obiekty modelu """
        return self.model_order.objects.filter(care=self.request.user)

    
    def get_current_month_days(self):
        """ Zwraca liste dni bierzacego miesiaca """
        current = datetime.datetime.now()
        month = Calendar().itermonthdates(current.year,current.month)
        days = [day.day for day in month if day.month == current.month]
        return days

    def get_my_current_month_orders_counter(self):
        """ Zwraca liste zlecen per dzien beirzacego miesiaca """
        current = datetime.datetime.now()
        
        # Queryset
        qs = self.get_objects().filter(
            created_date__month = current.month,
            created_date__year = current.year
        ).annotate(
            day=ExtractDay('created_date'),
        ).values(
            'day'
        ).annotate(
            n=Count('pk')
        ).order_by('day')
        
        complete_list = []
        for day in self.get_current_month_days():
            for x in list(qs):
                if day == x['day']:
                    complete_list.append(x['n'])
                else:
                    complete_list.append(0)
        return complete_list
    def get_my_current_month_orders_counter_completed(self):
        """ Zwraca liste zlecen zakonczonych per dzien beirzacego miesiaca """
        current = datetime.datetime.now()
        
        # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
            order_status__id=6
        ).annotate(
            day=ExtractDay('start_datetime'),
        ).values(
            'day'
        ).annotate(
            n=Count('pk')
        ).order_by('day')
        

        li = []
        for day in self.get_current_month_days():
            flag = False
            value = ""
            for x in list(qs):
                if x['day'] == day:
                    value = x['n']
                    flag = True
            if flag:
                li.append(value)
            else:
                li.append(0)

        return li
    def get_my_current_month_orders_counter_notcompleted(self):
        """ Zwraca liste zlecen oczekujacych na rozliczenie per dzien beirzacego miesiaca """
        current = datetime.datetime.now()
        
        # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
            order_status__id=5
        ).annotate(
            day=ExtractDay('start_datetime'),
        ).values(
            'day'
        ).annotate(
            n=Count('pk')
        ).order_by('day')
        
        complete_list = []

        li = []
        for day in self.get_current_month_days():
            flag = False
            value = ""
            for x in list(qs):
                if x['day'] == day:
                    value = x['n']
                    flag = True
            if flag:
                li.append(value)
            else:
                li.append(0)
        return li
    def get_my_current_month_orders_counter_in_progress(self):
        """ Zwraca liste zlecen niezakonczonych per dzien beirzacego miesiaca """
        current = datetime.datetime.now()
        
        # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
            order_status__id=3
        ).annotate(
            day=ExtractDay('start_datetime'),
        ).values(
            'day'
        ).annotate(
            n=Count('pk')
        ).order_by('day')
        
        complete_list = []

        li = []
        for day in self.get_current_month_days():
            flag = False
            value = ""
            for x in list(qs):
                if x['day'] == day:
                    value = x['n']
                    flag = True
            if flag:
                li.append(value)
            else:
                li.append(0)
        return li
    def get_my_current_month_orders_counter_spent(self):
        """ Zwraca liste czasów zlecen per dzien beirzacego miesiaca """
        current = datetime.datetime.now()
        
        # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
        ).annotate(
            day=ExtractDay('start_datetime'),
            timeuntil=F('end_datetime')-F('start_datetime')
        ).values(
            'day',
            'timeuntil'
        ).annotate(
            n=Count('pk'),
            t=Sum('timeuntil')
        ).order_by('day')

        
        complete_list = []


        li = []
        for day in self.get_current_month_days():
            flag = False
            value = ""
            for x in list(qs):
                if x['day'] == day:
                    value = "{:.2f}".format(float(x['t'].total_seconds()/60)/60)
                    flag = True
            if flag:
                li.append(value)
            else:
                li.append(0)
        return li
    def get_my_current_month_orders_counter_costs(self):
        """ Zwraca liste czasów zlecen per dzien beirzacego miesiaca """
        current = datetime.datetime.now()
        
        # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
        ).annotate(
            day=ExtractDay('start_datetime'),
            month=ExtractMonth('start_datetime__month'),
            year=ExtractYear('start_datetime__year')
        ).values(
            'day',
            'month',
            'year'
        ).annotate(
            n=Count('pk'),
        ).order_by('day')

        

        for each in list(qs):
            day = each['day']
            month = each['month']
            year = each['year']
            qss = self.get_objects().filter(start_datetime__day=day,start_datetime__month=month,start_datetime__year=year)
            koszta = 0
            for q in qss:
                print(q.calculate_order_with_distance())
                koszta += q.calculate_order_with_distance()
            each['koszta'] = koszta
            
            print(qs)

        complete_list = []


        li = []
        for day in self.get_current_month_days():
            flag = False
            value = ""
            for x in list(qs):
                if x['day'] == day:
                    value = x['koszta']
                    flag = True
            if flag:
                li.append(value)
            else:
                li.append(0)
        print(li)
        return li
    def get_my_current_month_orders_counter_status_all(self):
        current = datetime.datetime.now()
         # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year
        ).annotate(
            nieukończone=Count('pk', exclude=Q(order_status__id=6)),
            ukończone=Count('pk', filter=Q(order_status__id=6))
        ).values("nieukończone","ukończone")

        try:
            return qs[0]
        except:
            pass
    def get_month_orders_statuses(self):
        """ Zbiera dane o zleceniach do licznika """
        current = datetime.datetime.now()
         # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
        ).annotate(
            completed=Count('pk',filter=Q(order_status__id=6)),
            notcompleted=Count('pk',filter=~Q(order_status__id=6))
        ).values(
            "completed",
            "notcompleted",
        ).aggregate(
            rozliczone=Sum("completed"),
            nierozliczone=Sum("notcompleted")
            )
        return qs
    def get_month_orders_types(self):
        """ Zbiera dane o zleceniach do licznika """
        current = datetime.datetime.now()
         # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
        ).annotate(
            traveled=Count('pk',filter=Q(implementation_type__is_traveled=True)),
            remoted=Count('pk',filter=~Q(implementation_type__is_traveled=True))
        ).values(
            "traveled",
            "remoted"
        ).aggregate(
            wizyty=Sum("traveled"),
            zdalnie=Sum("remoted")
            )
        

        return qs
    def get_not_completed_orders(self):
        return self.get_objects().exclude(order_status__id=6)
    def get_completed_orders(self):
        return self.get_objects().filter(order_status__id=6)
    def get_month_companies_spent(self):
        """ Zbiera dane czaasowe firm ze zleceniami """
        current = datetime.datetime.now()
         # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
        ).annotate(
            duration=ExpressionWrapper(F('end_datetime')-F('start_datetime'),output_field=DurationField(default=int(timedelta().total_seconds()))),
        ).order_by(
            "document__company_sfk"
        )


        li = []
        for x in qs:
            obj= {}
            obj['nip'] = x.document.company_sfk
            obj['firma'] = x.get_subiekt_company_name()
            obj['czas'] = float(x.duration.total_seconds()/60)/60
            li.append(obj)

        aggregated_list = self.get_aggregated_list(lista=li,key="firma",value="czas")
        print(aggregated_list)

        return aggregated_list
    def get_month_companies_costs(self):
        """ Zbiera dane z kosztów per firma """
        current = datetime.datetime.now()
         # Queryset
        qs = self.get_objects().filter(
            start_datetime__month = current.month,
            start_datetime__year = current.year,
        ).order_by(
            "document__company_sfk"
        )
        companies_costs = self.get_companies_costs(orders=qs)
        return companies_costs


    def get_aggregated_list(self,lista,key,value):
        """ Agreguje dane listy slowników wg key """
        import itertools as it
        keyfunc = lambda x: x[key]
        groups = it.groupby(sorted(lista, key=keyfunc), keyfunc)
        return [{key:k, value:sum(x[value] for x in g)} for k, g in groups]

    def get_companies_costs(self,orders):
        lista = []
        for each in orders:
            costs = {
                "firma":each.get_subiekt_company_name(),
                "koszta":each.calculate_order_with_distance()
                }
            lista.append(costs)

        aggregated_list = self.get_aggregated_list(lista=lista,key="firma",value="koszta")
        return aggregated_list




    def get_orders_sum_costs(self):
        """ Zwraca sume kosztów wszytskich zleceń instancji"""
        return sum([c.calculate_order() for c in self.get_objects()])
    def get_orders_sum_travel_costs(self):
        """ Zwraca sume kosztów z dojazdem wszytskich zleceń instancji"""
        return sum([c.get_fuel_costs() for c in self.get_objects()])
    def get_orders_sum_costs_with_travel(self):
        """ Zwraca sume kiletrów instancji zleceń """
        return sum([c.calculate_order_with_distance() for c in self.get_objects()])
    def get_orders_counter(self):
        """ Zwraca sume zleceń instacji """
        return len(self.get_objects())
    def get_orders_two_way_distance(self):
        """ Zwraca sume kilometrową zleceń instancji """
        return sum([c.get_two_way_distance() for c in self.get_objects()])
    def get_orders_sum_time(self):
        """ Zwraca sume czasu zleceń instancji """
        return "{:.1f}".format(sum([(c.calculate_timedelta()/60)/60 for c in self.get_objects()]))
    

def home(request):
    """ Przekierowanie na dashboard """
    return HttpResponseRedirect("dashboard")


# Widoki obiektów --------------------------------------
@method_decorator(staff_member_required, name='dispatch')
class MessageCreateView(LoginRequiredMixin,View):
    """ Widok dodawania nowego obiektu 'Message' """
    template_create_form = "HD_app/subiekt/messages/message_add_form.html"

    # forms
    create_form = MessageCreateForm

    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def get_context_data(self,**kwargs):
        context = {
            "create_form": self.create_form,
        }
        return context

    def get(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data()
        if request.is_ajax():
            if request.method == "GET":
                return render(request,self.template_create_form,{"create_form":self.create_form})
        return render(request,self.template_create_form,{"create_form":self.create_form})
       
    def post(self, request, pk=None, *args, **kwargs):
        if self.sf.is_form_in_data(request,formid="message-add-form"):
            create_form = self.create_form(self.sf.get_form_data(request,form="message-add-form"))
            if create_form.is_valid():
                form = create_form.save(commit=False)
                form.sender = request.user
                form.save()
                create_form.save_m2m()
                if request.is_ajax():
                    return JsonResponse({"status":status.HTTP_200_OK,"Message":"Zapisano"})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"Message":"Błąd"})
            else:
                print(f"Błąd: {create_form.errors} \n")
                if request.is_ajax():
                    return render(request,self.template_create_form,context={"create_form":create_form})
@method_decorator(staff_member_required, name='dispatch')
class MessageDetailView(LoginRequiredMixin,View):
    """ Widok instancji obiektu 'Message' """
    model = Message
    template_name = 'HD_app/subiekt/messages/message_detail.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            msg = self.get_msg(request,*args,**kwargs)
            self.make_msg_read(msg)
            return render(request,self.template_name,{"msg": msg})

    def make_msg_read(self,msg):
        if msg.is_read == False:
            msg.is_read = True
            msg.save()
        
    def get_msg(self,request,*args,**kwargs):
        pk = int(request.GET.get("pk",None))
        msg = self.model.objects.get(pk=pk)
        return msg
@method_decorator(staff_member_required, name='dispatch')
class MessageDeleteAjax(LoginRequiredMixin,View):
    """ Widok usuwania 'Message' """
    model = Message
    def get_objects(self,*args,**kwargs):
        ids = json.loads(self.request.body).get("pk")
        objs = self.model.objects.filter(id__in=ids)
        return objs
    
    def delete_objects(self,*args,**kwargs):
        return self.get_objects().delete()

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.delete_objects()
            return JsonResponse({"status":"OK"})


@method_decorator(staff_member_required, name='dispatch')
class UserCreateView(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = User_Form
    model = User
    template_name = 'HD_app/user_add.html'
    template_form = 'HD_app/subiekt/user/user_add_form.html'

    def get(self, request, pk=None, *args, **kwargs):
        context = {
            "user_form": self.form_class(),
            "users": self.model.objects.all(),
            "profiles": Profile.objects.all()
            }
        if request.is_ajax():
            if request.method == "GET":
                return render(request,self.template_form,{"user_form":self.form_class})
        return render(request, self.template_name, context)   
    def form_valid(self, form):
        # form.instance.created_by = self.request.user
        return super().form_valid(form)
    def is_data(self,request,*args,**kwargs):
        for x,y in request.POST.items():
            if x == 'data':
                return True
            else:
                return False
    def add_users(self,request,*args,**kwargs):
        for x,y in request.POST.items():
            if x == 'add_users':
                return True
            else:
                return False
    def create_users_and_profiles(self,request):
        lista = self.get_user_list(request)
        for user in lista:
            idf = user['idf']
            user.pop("idf")
            user['username'] = user['email']
            u,created = User.objects.get_or_create(**user)
            print(u.id)
            p = Profile.objects.get(user=u)
            p.idf=idf
            p.save()
    def get_user_list(self,request,*args,**kwargs):
        return json.loads(request.POST.get('add_users', ''))
    def is_form_in_data(self,request,*args,**kwargs):
        for key,value in json.loads(request.POST.get('data', ''))[0].items():
            if key == kwargs.get("formid"):
                return True       
    def get_data_users_list(self,request,*args,**kwargs):
        lista = []
        data = json.loads(request.body)['data']
        for user in data:
            u = user
            u["password"] = "2fwfewef"
            u["username"] = user["email"]
            lista.append(u)
        return lista
    def get_form_data(self, request, *args,**kwargs):
        for key,value in json.loads(request.POST.get('data', ''))[0].items():
            if key == kwargs.get("form"):
                print(print("{0} - Formularz: {1}".format(get_current_datetime(),key)))
                data = json.loads(request.POST.get('data', ''))
                l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
                q = QueryDict(l)
                print(print("{0} - Przekonwertowano: {1}".format(get_current_datetime(),q)))
                return q
    def post(self, request, pk=None, *args, **kwargs):
        if self.is_data(request):
            if self.is_form_in_data(request,formid="user_add_form"):
                user_form = self.form_class(self.get_form_data(request,form="user_add_form"))
                if user_form.is_valid():
                    user_form.save()
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_200_OK})
                else:
                    return render(request,self.template_form,context={"user_form":user_form})
        if self.add_users(request):
            self.create_users_and_profiles(request)
            if request.is_ajax():
                return JsonResponse({"status":status.HTTP_200_OK})
            
        return JsonResponse({"status":status.HTTP_400_BAD_REQUEST})
@method_decorator(staff_member_required, name='dispatch')
class UserDetailView(LoginRequiredMixin,UpdateView):
    model = User
    profile = Profile
    form_class = User_Form
    template_name = 'HD_app/user_detail.html'
    template_form = 'HD_app/forms/user_detail_form.html'
    template_name_suffix = '_detail'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.method == "GET":
                obj = self.get_object() 
                form = self.form_class(instance=obj)
                return render(request,self.template_form,{"form":form})
        return super(UserViewDetails, self).get(\
            request, *args, **kwargs)
        
   
    def post(self, request, *args, **kwargs):
        # self.template_name = self.template_form
        obj = self.get_object()
        form = self.form_class(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({"status":"OK"})
        return render(request,self.template_form,{"form":form})
    
        # self.object = self.get_object()
        # super(UserViewDetails, self).post(\
        #     request, *args, **kwargs)
        
    def get_success_url(self, **kwargs):         
        return reverse_lazy("User_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
    
    def get_profile(self,*args,**kwargs):
        profile = get_object_or_404(self.profile, user__id=self.kwargs['pk'])
        return profile
@method_decorator(staff_member_required, name='dispatch')
class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = User
    form_class = User_Form
    template_name = 'HD_app/user_delete.html'
    template_form = 'HD_app/forms/user_delete_form.html'
    success_url = reverse_lazy('User_add')
    template_name_suffix = '_delete'
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status":"OK"})
        
    def get_object(self,*args,**kwargs):
        return get_object_or_404(self.model,pk=self.kwargs['pk'])
@method_decorator(staff_member_required, name='dispatch')
class UserDeleteAjax(View):
    model = User
    def get_objects(self,*args,**kwargs):
        ids = json.loads(self.request.body).get("pk")
        objs = self.model.objects.filter(id__in=ids)
        return objs
    
    def delete_objects(self,*args,**kwargs):
        return self.get_objects().delete()

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.delete_objects()
            return JsonResponse({"status":"OK"})


@method_decorator(staff_member_required, name='dispatch')
class DocumentCreateView(LoginRequiredMixin,View):
    """ Widok dodawania nowego obiektu 'Document' """
    template_create_form = "HD_app/subiekt/document/document_add_form.html"

    # forms
    create_form = DocumentCreateForm

    # endpoint odpytania subiekta o obiekt
    endpoint_company_get = subiekt.get_absolute_endpoint("kontrahenci")

    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def get_context_data(self,**kwargs):
        context = {
            "create_form": self.create_form,
        }
        return context

    def get(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data()
        if request.is_ajax():
            if request.method == "GET":
                if self.sf.is_data(request,*args,**kwargs):
                    if subiekt.is_up():
                        obj = self.sf.get_subiekt_object(request,endpoint=self.endpoint_company_get,*args,**kwargs)
                        form = self.create_form(data={"company_sfk":obj[0]['Symbol']})

                        return render(request,self.template_create_form,{"create_form":form})
        return render(request,self.template_create_form,{"create_form":self.create_form})
       
    def post(self, request, pk=None, *args, **kwargs):
        print(request.POST)
        if self.sf.is_form_in_data(request,formid="document-add-form"):
            create_form = self.create_form(self.sf.get_form_data(request,form="document-add-form"))

            if create_form.is_valid():
                create_form.save()
                if request.is_ajax():
                    return JsonResponse({"status":status.HTTP_200_OK,"Message":"Zapisano"})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"Message":"Błąd"})
            else:
                print(f"Błąd: {create_form.errors} \n")
                if request.is_ajax():
                    return render(request,self.template_create_form,context={"create_form":create_form})
@method_decorator(staff_member_required, name='dispatch')
class DocumentDeleteAjax(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    
    model = Document
    form_name = "document-delete-form"

    # Matryca zmiany nazw pól
    fields_replacement_matrix = {
        "document":"pk"
    }

    
    def get_objects(self,request,*args,**kwargs):
        form_data = self.sf.get_form_data(request,form=self.form_name)
        fields = self.sf.replace_ajax_form_fields(fields_replacement_matrix=self.fields_replacement_matrix,form_data=form_data)
        objs = self.model.objects.filter(pk__in=fields.get("pk"))
        print("Znaleziono obiekty:")
        print(objs)
        return objs
    

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.get_objects(request,*args,**kwargs).delete()
            return JsonResponse({"status":"OK"})

@method_decorator(staff_member_required, name='dispatch')
class AddressCreateView(LoginRequiredMixin,View):
    """ Widok dodawania nowego obiektu 'Address' """
    template_create_form = "HD_app/subiekt/address/address_add_form.html"

    # forms
    create_form = AddressCreateForm

    # endpoints
    endpoint_company_get = subiekt.get_absolute_endpoint("kontrahenci")

    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def get_context_data(self,**kwargs):
        context = {
            "create_form": self.create_form,
        }
        return context

    def get(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data()
        if request.is_ajax():
            if self.sf.is_data(request,*args,**kwargs):
                if subiekt.is_up():
                    obj = self.sf.get_subiekt_object(request,endpoint=self.endpoint_company_get,*args,**kwargs)
                    form = self.create_form(data={"company_sfk":obj[0]['Symbol']})
                    return render(request,self.template_create_form,{"create_form":form})
        return render(request,self.template_create_form,{"create_form":self.create_form})

    def post(self, request, pk=None, *args, **kwargs):
        if self.sf.is_form_in_data(request,formid="address-add-form"):
            create_form = self.create_form(self.sf.get_form_data(request,form="address-add-form"))
            if create_form.is_valid():
                create_form.save()
                if request.is_ajax():
                    return JsonResponse({"status":status.HTTP_200_OK,"Message":"Zapisano"})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"Message":"Błąd"})
            else:
                print(f"Błąd: {create_form.errors} \n")
                if request.is_ajax():
                    return render(request,self.template_create_form,context={"create_form":create_form})
@method_decorator(staff_member_required, name='dispatch')
class AddressDeleteAjax(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    
    model = Address2
    form_name = "address-delete-form"

    # Matryca zmiany nazw pól
    fields_replacement_matrix = {
        "address":"pk"
    }

    
    def get_objects(self,request,*args,**kwargs):
        form_data = self.sf.get_form_data(request,form=self.form_name)
        fields = self.sf.replace_ajax_form_fields(fields_replacement_matrix=self.fields_replacement_matrix,form_data=form_data)
        objs = self.model.objects.filter(pk__in=fields.get("pk"))
        print("Znaleziono obiekty:")
        print(objs)
        return objs
    

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.get_objects(request,*args,**kwargs).delete()
            return JsonResponse({"status":"OK"})
@method_decorator(staff_member_required, name='dispatch')
class OrderDeleteAjax2(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    
    model = Order2
    form_name = "pending-orders-delete-form"

    # Matryca zmiany nazw pól
    fields_replacement_matrix = {
        "pending_order":"pk"
    }

    
    def get_objects(self,request,*args,**kwargs):
        form_data = self.sf.get_form_data(request,form=self.form_name)
        fields = self.sf.replace_ajax_form_fields(fields_replacement_matrix=self.fields_replacement_matrix,form_data=form_data)
        objs = self.model.objects.filter(pk__in=fields.get("pk"))
        print("Znaleziono obiekty:")
        print(objs)
        return objs
    

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.get_objects(request,*args,**kwargs).delete()
            return JsonResponse({"status":"OK"})


order_modal_sections = {
        "tabs":[
            {
                "icon":"<i class='fas fa-align-left'></i>",
                "tab_name":"Podstawowe",
                "tab_id":"podstawowe",
                "active":True,
                "fields":[
                    "order_template",
                    "name",
                    "document",
                    "description",
                    "created_date"
                    ],
            },
            {
                "icon":"<i class='fas fa-plus-square'></i>",
                "tab_name":"Dodatkowe",
                "tab_id":"dodatkowe",
                "active":False,
                "fields":[
                    "order_status",
                    "implementation_type",
                    "care",
                    "start_datetime",
                    "end_datetime"
                    ],
            },
            {
                "icon":"<i class='fas fa-dollar-sign'></i>",
                "tab_name":"Dojazd i koszta",
                "tab_id":"koszta",
                "active":False,
                "fields":[
                    "address",
                    ],
            }
            ],
        "headers":[
            {
                "name":"create",
                "icon":"<i class='fas fa-clipboard-list'></i>",
                "text":"Nowe zlecenie"
            },
            {
                "name":"detail",
                "icon":"<i class='fas fa-clipboard-list'></i>",
                "text":"Edycja zlecenia"
            },
        ],
            
        }
@method_decorator(staff_member_required, name='dispatch')
class OrderCreateView(LoginRequiredMixin,View):
    """ Widok dodawania nowego obiektu 'Order' """
    template_form = "HD_app/subiekt/order/order_add.html"
    template_create_form = "HD_app/subiekt/order/order_add_form.html"
    template_search_form = "HD_app/subiekt/order/order_search_form.html"
    template_search_list = "HD_app/subiekt/order/order_list.html"
    model = Order2

    # forms
    create_form = OrderCreateForm
    search_form = OrderSearchModelForm

    # endpoints
    endpoint_company_get = subiekt.get_absolute_endpoint("kontrahenci")
    search_endpoint = subiekt.get_absolute_endpoint("kontrahenci")

    # search parameters
    parameters = {
        "name":"__icontains",
        "start_datetime":"__gte",
        "end_datetime":"__lte"
        }

    # Podział sekcji okna modalnego
    modal_sections = order_modal_sections

    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def get_context_data(self,request,*args,**kwargs):

        context = {
            "create_form": self.create_form(request=request),
            "modal_sections":self.modal_sections,
            "search_form":self.search_form,
            "orders": self.model.objects.filter(\
                care=request.user,
                start_datetime__date__gte=datetime.date.today().replace(day=1),
                end_datetime__lte=datetime.datetime.today().replace(hour=23,minute=59,second=59)
                ),
        }
        return context
    
    def search_obj(self,*args,**kwargs):
        main_search_param = kwargs.get("main_search_param")
        exclude_param_for = kwargs.get("exclude_param_for")
        d = kwargs.get("cleaned_data")
        res = {str(key)+main_search_param: val for key, val in d.items()}
        print(f"Przeszukuje po polach {res} z parametrem szukania: {main_search_param}")
        obj = self.model.objects.filter(**res)
        print(f"Znalezione obiekty: {obj}")
        return obj

    def search_objs(self,*args,**kwargs):
        parameters = kwargs.get("parameters","")
        cleaned_data = kwargs.get("cleaned_data","")
        processed_data = {}
        for k,v in cleaned_data.items():
            if k in parameters.keys():
                d = {k+parameters[k]:v}
                processed_data.update(d)
            else:
                de = {k:v}
                processed_data.update(de)
        print(f"Przeszukuje obiekt: {self.model} ,po polach: {processed_data}")
        objs = self.model.objects.filter(**processed_data)
        print(f"Zwracam znalezione obiekty: {objs}")
        return objs
        
    def get(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(request,*args,**kwargs)
        if request.is_ajax():
            return render(request,self.template_create_form,context)
        return render(request,self.template_form,context)

    def post(self, request, pk=None, *args, **kwargs):

    # search
        if self.sf.is_form_in_data(request,formid="order-search-form"):
            search_form = self.search_form(self.sf.get_form_data(request,form="order-search-form"))
            if search_form.is_valid():
                if request.is_ajax():
                    search_form.cleaned_data['care'] = request.user
                    #objs = self.search_obj(main_search_param="__icontains",cleaned_data=search_form.cleaned_data)
                    objs = self.search_objs(parameters=self.parameters,cleaned_data=search_form.cleaned_data)
                    return render(request,self.template_search_list,context={"data":objs})  
            else:
                print(search_form.errors)
                return render(request,self.template_search_form,context={"search_form":search_form})   

    # add
        if self.sf.is_form_in_data(request,formid="order-add-form"):
            create_form = self.create_form(self.sf.get_form_data(request,form="order-add-form"))
            if create_form.is_valid():
                create_form.save()
                if request.is_ajax():
                    return JsonResponse({"status":status.HTTP_200_OK,"Message":"Zapisano"})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"Message":"Błąd"})
            else:
                print(f"Błąd: {create_form.errors} \n")
                if request.is_ajax():
                    return render(request,self.template_create_form,context={"create_form":create_form,"modal_sections":self.modal_sections})
@method_decorator(staff_member_required, name='dispatch')
class OrderDetailView(LoginRequiredMixin,UpdateView):
    """ Widok instacji 'Order' """
    model = Order2
    form_class = OrderDetailForm
    template_name = 'HD_app/subiekt/order/order_detail.html'
    template_form = 'HD_app/subiekt/order/order_detail_form.html'
    
    # Podział sekcji okna modalnego
    modal_sections = order_modal_sections

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.method == "GET":
                obj = self.get_object() 
                form = self.form_class(instance=obj)
                return render(request,self.template_form,{"form":form,"modal_sections":self.modal_sections})
        return super(OrderDetailView, self).get(\
            request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.form_class(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({"status":"OK"})
        return render(request,self.template_form,{"form":form,"modal_sections":self.modal_sections})
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy("Order_add")

    def get_object(self, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_object_ajax(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=request.GET.get("pk"))
        return obj
@method_decorator(staff_member_required, name='dispatch')
class OrderDeleteAjax(LoginRequiredMixin,View):
    """ Widok usuwania 'Order' """
    model = Order2
    def get_objects(self,*args,**kwargs):
        ids = json.loads(self.request.body).get("pk")
        objs = self.model.objects.filter(id__in=ids)
        return objs
    
    def delete_objects(self,*args,**kwargs):
        return self.get_objects().delete()

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.delete_objects()
            return JsonResponse({"status":"OK"})
@method_decorator(staff_member_required, name='dispatch')
class OrderAccountAjax(LoginRequiredMixin,View):
    """ Widok Rozliczania 'Order' """
    model = Order2
    def get_objects(self,*args,**kwargs):
        ids = json.loads(self.request.body).get("pk")
        objs = self.model.objects.filter(id__in=ids)
        return objs
    
    def account_objects(self,*args,**kwargs):
        obj = self.get_objects()
        print("Rozliczam wybrane zlecenia...")
        print(obj)
        obj.update(order_type__id=6)
        return obj


    def account(self, request, *args, **kwargs):
        if request.is_ajax():
            self.account_objects()
            return JsonResponse({"status":"OK"})


raport_modal_sections = {
        "tabs":[
            {
                "icon":"<i class='fas fa-align-left'></i>",
                "tab_name":"Dane dokumentu",
                "tab_id":"podstawowe",
                "active":True,
                "fields":[
                    "name",
                    "company_sfk",
                    "start_date",
                    "end_date",
                    ],
            },
            {
                "icon":"<i class='fas fa-hourglass-half text-danger'></i>",
                "tab_name":"Nierozliczone",
                "tab_id":"pending",
                "active":False,
                "fields":[
                    
                    ],
            },
            {
                "icon":"<i class='fas fa-check text-success'></i>",
                "tab_name":"Rozliczone",
                "tab_id":"closed",
                "active":False,
                "fields":[
                    
                    ],
            },
            {
                "icon":"<i class='fas fa-plus-square'></i>",
                "tab_name":"Generuj raport",
                "tab_id":"raport",
                "active":False,
                "fields":[
                    
                    ],
            }
            ],
        "headers":[
            {
                "name":"create",
                "icon":"<i class='fas fa-clipboard-list'></i>",
                "text":"Nowy dokument"
            },
            {
                "name":"detail",
                "icon":"<i class='fas fa-clipboard-list'></i>",
                "text":"Informacje o dokumencie"
            },
        ],
            
        }
@method_decorator(staff_member_required, name='dispatch')
class DocumentRaportView(LoginRequiredMixin,View):
    """  """
    template_name = 'HD_app/subiekt/raport/raport_add.html'
    template_create_form = "HD_app/subiekt/document/document_add_form.html"
    # template_search_form = "HD_app/subiekt/raport/raport_search_form.html"
    # template_search_list = "HD_app/subiekt/raport/raport_list.html"

    forms
    create_form = SubiektCompanyCreateForm
    search_form = SubiektCompanySearchForm1
    # search_form = RaportSearchForm

    # endpoints
    create_endpoint = subiekt.get_absolute_endpoint("firmy")
    search_endpoint = subiekt.get_absolute_endpoint("kontrahenci")

    # Meta fields
    meta_fields = Document._meta.fields

    model_order = Order2

    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def get_context_data(self,**kwargs):

        context = {
            # "create_form": self.create_form,
            # "search_form":self.search_form,
            "documents":Document.objects.all(),
            "get_pending_orders": self.get_pending_orders()
                    }
        return context

 

    def get_pending_orders(self):
        self.model_order.objects.exclude(order_status=6)
    def get_pending_orders(self):
        self.model_order.objects.exclude(order_status=6)

    def get(self, request, pk=None, *args, **kwargs):
        
        context = self.get_context_data()
        if request.is_ajax():
            if request.method == "GET":
                return render(request,self.template_create_form,{"form":self.create_form})
        return render(request, self.template_name, context)
                
    def post(self, request, pk=None, *args, **kwargs):

 
        if self.sf.is_form_in_data(request,formid="company-search-form"):
            search_form = self.search_form(self.sf.get_form_data(request,form="company-search-form"))
            if search_form.is_valid():
                if subiekt.is_up():
                    subiekt_data = self.sf.get_subiekt_data(request,endpoint=self.search_endpoint,form=search_form)
                    if request.is_ajax():
                        return render(request,self.template_search_list,context={"data":[subiekt_data.json()]})  
                        # return JsonResponse({"status":subiekt_data.status_code,"Message":subiekt_data.json().get("Message")})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND})    
            else:   
                return render(request,self.template_search_form,context={"search_form":search_form})   
        

        if self.sf.is_form_in_data(request,formid="company-add-form"):
            create_form = self.create_form(self.sf.get_form_data(request,form="company-add-form"))
            if create_form.is_valid():
                if subiekt.is_up():
                    subiekt_data = self.sf.get_subiekt_data(request,endpoint=self.create_endpoint,form=create_form)
                    if request.is_ajax():
                        #return render(request,self.template_search_list,context={"data":[subiekt_data.json()]})  
                        return JsonResponse({"status":subiekt_data.status_code,"Message":subiekt_data.json().get("Message")})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND})    
            else:   
                return render(request,self.template_create_form,context={"create_form":create_form})   
@method_decorator(staff_member_required, name='dispatch')
class DocumentDetailView(LoginRequiredMixin,UpdateView):
    """ Widok instacji 'Order' """
    model = Document
    form_class = DocumentDetailForm
    template_form = 'HD_app/subiekt/document/document_detail_form.html'

    # forms
    search_form = RaportSearchForm

    # Podział sekcji okna modalnego
    modal_sections = raport_modal_sections

    # Modele
    model_order = Order2

    def get_context_data(self,request,**kwargs):
        obj = self.get_object()

        context = {
            "modal_sections":self.modal_sections,
            "document":obj,
            "pending_orders":self.get_pending_orders(),
            "completed_orders":self.get_completed_orders()
            }
        return context
    def get_pending_orders(self):
        return self.model_order.objects.filter(document=self.get_object()).exclude(order_status=6)
    def get_completed_orders(self):
        return self.model_order.objects.filter(document=self.get_object()).filter(order_status=6)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.method == "GET":
                obj = self.get_object() 
                form = self.form_class(instance=obj)
                search_form = self.search_form(data={"document":obj})
                context = self.get_context_data(request,**kwargs)
                context["form"] = form
                context["search_form"] = search_form
                return render(request,self.template_form,context)
        return super(DocumentDetailView, self).get(\
            request, *args, **kwargs)  
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.form_class(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({"status":"OK"})
        return render(request,self.template_form,{"form":form,"modal_sections":self.modal_sections}) 
    def get_success_url(self, **kwargs):         
        return reverse_lazy("Document_add")
    def get_object(self, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj
    def get_object_ajax(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=request.GET.get("pk"))
        return obj
@method_decorator(staff_member_required, name='dispatch')
class RaportSearchAjax(LoginRequiredMixin,View):
    template_name = 'HD_app/subiekt/raport/raport_filtered.html'

    # forms
    search_form = RaportSearchForm

    # model
    model = Order2

    # search parameters
    parameters = {
        "name":"__icontains",
        "start_datetime":"__gte",
        "end_datetime":"__lte"
        }
    def get_orders_sum_costs(self):
        """ Zwraca sume kosztów wszytskich zleceń instancji"""
        return sum([c.calculate_order() for c in self.orders[0]])
    def get_orders_sum_travel_costs(self):
        """ Zwraca sume kosztów z dojazdem wszytskich zleceń instancji"""
        return sum([c.get_fuel_costs() for c in self.orders[0]])
    def get_orders_sum_costs_with_travel(self):
        """ Zwraca sume kiletrów instancji zleceń """
        return sum([c.calculate_order_with_distance() for c in self.orders[0]])
    def get_orders_counter(self):
        """ Zwraca sume zleceń instacji """
        return len(self.orders[0])
    def get_orders_two_way_distance(self):
        """ Zwraca sume kilometrową zleceń instancji """
        return sum([c.get_two_way_distance() for c in self.orders[0]])
    def get_orders_sum_time(self):
        """ Zwraca sume czasu zleceń instancji """
        return sum([(c.calculate_timedelta()/60)/60 for c in self.orders[0]])
    def get_orders_fuel_stacks(self):
        """ Zwraca stawki kilometrowe wg którrych została zrobiona kalkulacja """
        all_fuel_stacks = [o.getDistanceCalcProfileCosts() for o in self.orders[0]]
        fuel_stacks = []
        [fuel_stacks.append(o) for o in all_fuel_stacks if o not in fuel_stacks]
        return fuel_stacks
    def get_ajax_data(self,request):
        """ Zwraca dane z ajax w postaci self.payload """
        self.payload = json.loads(json.dumps(request.GET))
    def get_range_in_days(self):
        """ Zwraca różnice dat zakresu raportu """
        start = datetime.datetime.strptime(self.payload.get("start_datetime"), '%Y-%m-%d %H:%M')
        end = datetime.datetime.strptime(self.payload.get("end_datetime"), '%Y-%m-%d %H:%M')
        diff = end-start
        return diff.days
    def search_obj(self,*args,**kwargs):
        main_search_param = kwargs.get("main_search_param")
        exclude_param_for = kwargs.get("exclude_param_for")
        d = kwargs.get("cleaned_data")
        res = {str(key)+main_search_param: val for key, val in d.items()}
        print(f"Przeszukuje po polach {res} z parametrem szukania: {main_search_param}")
        obj = self.model.objects.filter(**res)
        print(f"Znalezione obiekty: {obj}")
        return obj
    def search_objs(self,*args,**kwargs):
        parameters = kwargs.get("parameters","")
        cleaned_data = kwargs.get("cleaned_data","")
        processed_data = {}
        for k,v in cleaned_data.items():
            if k in parameters.keys():
                d = {k+parameters[k]:v}
                processed_data.update(d)
            else:
                de = {k:v}
                processed_data.update(de)
        print(f"Przeszukuje obiekt: {self.model} ,po polach: {processed_data}")
        objs = self.model.objects.filter(**processed_data)
        print(f"Zwracam znalezione obiekty: {objs}")
        return objs
    def search_specified_objs(self,model,*args,**kwargs):
        parameters = kwargs.get("parameters","")
        cleaned_data = kwargs.get("cleaned_data","")
        processed_data = {}

        for k,v in cleaned_data.items():
            if k in parameters.keys():
                d = {k+parameters[k]:v}
                processed_data.update(d)
            else:
                de = {k:v}
                processed_data.update(de)

        # Czyszczenie kluczy bez pól ze slownika
        processed_data_cleaned = processed_data.copy()
        for k,v in processed_data.items():
            if processed_data[k] == "":
                del processed_data_cleaned[k]
                
        print(f"Przeszukuje obiekt: {model} ,po polach: {processed_data_cleaned}")
        objs = model.objects.filter(**processed_data_cleaned)
        pks = objs.values_list("pk")
        print(f"Zwracam znalezione obiekty: {objs}")
    
        # payload = {"pks":pks,"objs":objs}
        # return payload
        return objs
    def get_values_of(self,instance,field):
        return list(instance[0].values_list(field,flat=True))
    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    def get_context_data(self,request,**kwargs):
        self.get_ajax_data(request)
       
        # przefiltrowane orders[0] bo zwracana jest tupla
        self.orders = self.search_specified_objs(parameters=self.parameters,model=Order2,cleaned_data=self.payload),
        self.documents = Document.objects.filter(id__in=self.get_values_of(self.orders,"document"))

        context = {
            "orders": self.orders[0],
            "documents": self.documents,
            "date_range":{
                "start_date":self.payload.get("start_datetime"),
                "end_date":self.payload.get("end_datetime"),
                "get_range_in_days":self.get_range_in_days(),
                },
            "datetime_now":datetime.datetime.now(),
            "get_orders_sum_costs": self.get_orders_sum_costs(),
            "get_orders_sum_travel_costs": self.get_orders_sum_travel_costs(),
            "get_orders_sum_costs_with_travel":self.get_orders_sum_costs_with_travel(),
            "get_orders_counter":self.get_orders_counter(),
            "get_orders_two_way_distance":self.get_orders_two_way_distance(),
            "get_orders_sum_time":self.get_orders_sum_time(),
            "get_orders_fuel_stacks":self.get_orders_fuel_stacks(),
        }
        return context
    def get(self, request, pk=None, *args, **kwargs):    
        return render(request, self.template_name, self.get_context_data(request,*args,**kwargs))
   

# Widoki obiektów subiekta ------------------------------
company_modal_sections = {
        "tabs":[
            {
                "icon":"<i class='fas fa-align-left'></i>",
                "tab_name":"Podstawowe",
                "tab_id":"podstawowe",
                "active":True,
                "fields":[
                    "Nazwa",
                    "NazwaPelna",
                    "Nip",
                    "Typ"
                    ],
            },
            {
                "icon":"<i class='fas fa-plus-square'></i>",
                "tab_name":"Adres w subiekcie",
                "tab_id":"adres",
                "active":False,
                "fields":[
                    "Ulica",
                    "NrDomu",
                    "NrLokalu",
                    "Miejscowosc",
                    "KodPocztowy"
                    ],
            },
            {
                "icon":"<i class='fas fa-plus-square'></i>",
                "tab_name":"Adresy",
                "tab_id":"adresy",
                "active":False,
                "fields":[

                    ],
            },
            {
                "icon":"<i class='fas fa-plus-square'></i>",
                "tab_name":"Dokumenty",
                "tab_id":"dokumenty",
                "active":False,
                "fields":[

                    ],
            },
            ],
        "headers":[
            {
                "name":"create",
                "icon":"<i class='fas fa-clipboard-list'></i>",
                "text":"Nowa firma"
            },
            {
                "name":"detail",
                "icon":"<i class='fas fa-clipboard-list'></i>",
                "text":"Podgląd firmy"
            },
        ],
            
        }
@method_decorator(staff_member_required, name='dispatch')
class SubiektCompanyCreateView(LoginRequiredMixin,View):

    """ Dodawanie i listowanie Firm po searchu """
    template_name = 'HD_app/subiekt/company/company_add.html'
    template_create_form = "HD_app/subiekt/company/company_add_form.html"
    template_search_form = "HD_app/subiekt/company/company_search_form.html"
    template_search_list = "HD_app/subiekt/company/company_list.html"

    # forms
    create_form = SubiektCompanyCreateForm
    search_form = SubiektCompanySearchForm1

    # endpoints
    create_endpoint = subiekt.get_absolute_endpoint("firmy")
    search_endpoint = subiekt.get_absolute_endpoint("kontrahenci")

    # Podział sekcji okna modalnego
    modal_sections = company_modal_sections

    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def get_context_data(self,**kwargs):
        context = {
            "create_form": self.create_form,
            "search_form":self.search_form,
            "modal_sections":self.modal_sections,
            "documents":Document.objects.all()
        }
        return context

    def get(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data()
        if request.is_ajax():
            if request.method == "GET":
                return render(request,self.template_create_form,{"form":self.create_form})
        return render(request, self.template_name, context)
                
    def post(self, request, pk=None, *args, **kwargs):

    # search form
        if self.sf.is_form_in_data(request,formid="company-search-form"):
            search_form = self.search_form(self.sf.get_form_data(request,form="company-search-form"))
            if search_form.is_valid():
                if subiekt.is_up():
                    subiekt_data = self.sf.get_subiekt_data(request,endpoint=self.search_endpoint,form=search_form)
                    if request.is_ajax():
                        return render(request,self.template_search_list,context={"data":[subiekt_data.json()]})  
                        # return JsonResponse({"status":subiekt_data.status_code,"Message":subiekt_data.json().get("Message")})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND})    
            else:   
                return render(request,self.template_search_form,context={"search_form":search_form})   
        
    # create form 
        if self.sf.is_form_in_data(request,formid="company-add-form"):
            create_form = self.create_form(self.sf.get_form_data(request,form="company-add-form"))
            if create_form.is_valid():
                if subiekt.is_up():
                    subiekt_data = self.sf.get_subiekt_data(request,endpoint=self.create_endpoint,form=create_form)
                    if request.is_ajax():
                        #return render(request,self.template_search_list,context={"data":[subiekt_data.json()]})  
                        return JsonResponse({"status":subiekt_data.status_code,"Message":subiekt_data.json().get("Message")})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND})    
            else:   
                return render(request,self.template_create_form,context={"create_form":create_form})   
@method_decorator(staff_member_required, name='dispatch')
class SubiektCompanyDetailView(LoginRequiredMixin,View):
    """ Wyswietlanie instancji obiektu firmy z subiekta i nadpisywanie jego danych """
    template_name = "HD_app/subiekt/company/company_detail_form.html"
    endpoint = subiekt.get_absolute_endpoint("kontrahenci")

    # Formularz trzeba tak stworzyc aby pola odpowiadały odebranym polom z subiekta ,
    # czyli stworzyc pola Id,Nazwa itd. Poza tym widok musi zwracac instancje jednego obiektu
    # która zostanie zrenderowana na ten formularz
    form_class = SubiektCompanyCreateForm
    address_delete_form = AddressDeleteForm
    document_delete_form = DocumentDeleteForm
    # Podział sekcji okna modalnego
    modal_sections = company_modal_sections

    def __init__(self):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
 
    def get_context(self,request,*args,**kwargs):
        context = {
            "addresses":self.get_addresses(request,*args,**kwargs),
            "documents":self.get_documents(request,*args,**kwargs),
            "address_delete_form":self.address_delete_form(address=self.get_addresses(request,*args,**kwargs)),
            "document_delete_form":self.document_delete_form(document=self.get_documents(request,*args,**kwargs)),
            "modal_sections":self.modal_sections,
            
        }
        return context

    def get_addresses(self,request,*args,**kwargs):
        data = self.sf.get_ajax_data(request,*args,**kwargs)

        addr = Address2.objects.filter(company_sfk=data.get("Nip"))
        return addr
    
    def get_documents(self,request,*args,**kwargs):
        data = self.sf.get_ajax_data(request,*args,**kwargs)
        doc = Document.objects.filter(company_sfk=data.get("Nip"))
        return doc
    
    

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.method == "GET":
                if self.sf.is_data(request,*args,**kwargs):
                    if subiekt.is_up():
                        obj = self.sf.get_subiekt_object(request,endpoint=self.endpoint,*args,**kwargs)
                        form = self.form_class(obj[0])
                        context = self.get_context(request,*args,**kwargs)
                        context['form'] = form
                        return render(request,self.template_name,context)

        return super(SubiektCompanyDetailView, self).get(\
            request, *args, **kwargs)

    























def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'HD_app/change_password.html', {
        'form': form
    })
class MyPasswordResetView(PasswordResetView):
    subject_template_name = 'HD_app/password_reset_subject.txt'
    email_template_name = 'HD_app/password_reset_email.html'
    success_url=reverse_lazy('User_add')

    def get_form_kwargs(self):
        user = get_object_or_404(User, pk=self.kwargs.get('user_pk'))
        return {'data': {'email': user.email}}

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
class MassPasswordChange(LoginRequiredMixin,View):
    model = User
    def get_objects(self,*args,**kwargs):
        ids = json.loads(self.request.body).get("pk")
        objs = self.model.objects.filter(id__in=ids)
        return objs
    
    def send_and_get_statuses(self,*args,**kwargs):
        statuses = []
        c = Client()
        for x in self.get_objects():
            res = c.get(reverse("my_password_reset",kwargs={"user_pk":x.pk}))
            statuses.append({"pk":res.status_code})
            print(res.status_code)
        return statuses

    def post(self,request,*args,**kwargs):
        statuses = self.send_and_get_statuses()
        return JsonResponse({"statuses": statuses})

@method_decorator(staff_member_required, name='dispatch')        
class OrderTemplateView(View):
    fields = '__all__'
    form_class = OrderTemplateForm
    model = OrderTemplate
    template_name = 'HD_app/ordertemplate_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        context = {
            "form":self.form_class,
            }
        return render(request,self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                 return JsonResponse({"status":"OK"})
            else:
                return redirect(reverse("OrderTemplate_add"))
        else:
            if request.is_ajax():
                return JsonResponse({"errors":form.errors.as_json()})
            else:
                return render(request, self.template_name, {"form":form})

@staff_member_required
def JSON_load_cares(request):
    """
    Ściąga opiekuna dla podanej firmy. Wykorzystane z Ajaxem do pobierania domyslnego opiekuna firmy po wybraniu pola
    """
    document = request.GET.get('document',None)
    try:
        a = Document.objects.get(pk=document)
        #u = User.objects.get(pk=a.company.care.id)
        u = User.objects.get(pk=request.user.id)
        mo = model_to_dict(u, fields="id")
    except:
        mo = {}
    return JsonResponse(mo, content_type='application/json')
@staff_member_required
def JSON_load_order_template(request):
    """
    Ściąga szablony opisy zlecen
    """
    template_id = request.POST.get('t',None)
    try:
        t = OrderTemplate.objects.get(pk=template_id)
        context = {
            "description": t.description,
            "name": t.name,
            "order_status":t.order_status.id,
            "implementation_type":t.implementation_type.id,
            "order_type":t.order_type.id
        }
    except:
        context = {}
    return JsonResponse(context, content_type='application/json')
@staff_member_required
def JSON_load_addresses(request):
    """
    Ściąga adresy firmy przy zapytaniu o umowe w widoku dodawania zlecenia. Wykorzystane z Ajaxem.
    """
    document_pk = request.GET.get('document_pk',None)
    document = Document.objects.get(pk=document_pk)
    addresses = Address2.objects.filter(company_sfk=document.company_sfk)
    lista = []
    for a in addresses:
        adr = model_to_dict(a,fields=["id","name","city","distance"])
        lista.append(adr)
    return JsonResponse({"list":lista}, content_type='application/json')

        # return JsonResponse({},content_type='application/json')
@staff_member_required
def JSON_rozlicz_zlecenie(request):
    from django.core.serializers.json import DjangoJSONEncoder
    order = request.GET.get('order',None)
    o = Order2.objects.get(pk=order)
    s = OrderStatus.objects.get(name="Zrealizowane - rozliczone")
    o.order_status = s
    o.save()
    mo = model_to_dict(o,fields="id,name,order_status,updated_date")
    return JsonResponse(mo, content_type='application/json')
@staff_member_required
def JSON_sumuj_zlecenia(request):
    """
    Sumuj zlecenia danej umowy
    """
    a = request.GET.get('a',None)
    u = request.GET.get('u',None)
    s = request.GET.get('s',None)
    e = request.GET.get('e',None)
    

    start = datetime.now()
    end = datetime.now()
    try:
        start = datetime.strptime(s, "%Y-%m-%d").date()
        end = datetime.strptime(e, "%Y-%m-%d").date()
    except:
        print("Brak dni. listuje z bieżącego miesiąca...")
        start = datetime.today().replace(day=1,hour=0,minute=0,second=0)
        end = datetime.today().replace(month=start.month+1,day=1,hour=0,minute=0,second=0)
        print("od: %s, do: %s" % (start,end))
    
    o = Order2.objects.all().filter(document__id=a).filter(start_datetime__gte=start, end_datetime__lte=end)
    
    ou = Order2.objects.all().filter(document__id=a, care__id=u).filter(start_datetime__gte=start, end_datetime__lte=end)
    suma = sum([x.calculate_order() for x in o])
    suma_u = sum([x.calculate_order() for x in ou])
    suma_t = sum([x.calculate_timedelta() for x in o])
    suma_th = sum([(x.calculate_timedelta()/60)/60 for x in o])
    suma_ud = float("{:.2f}".format(sum([x.calculate_order_with_distance() for x in ou])))
    rate = [x.getRateCost() for x in o][0]
    print(suma_ud)
    worker = User.objects.get(pk=u)
    print(worker.id)

    return JsonResponse({"a":int(a),"rate":rate,"suma":suma,"suma_u": suma_u, "suma_ud":suma_ud,"suma_t":suma_t,"suma_th":suma_th,"worker":worker.id}, content_type='application/json')



@method_decorator(staff_member_required, name='dispatch')
class SubiektAPI(LoginRequiredMixin,View):

    """ Listowanie subiekta dla buttona 'subiekt-button' (prosty serializer) """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def post(self, request, pk=None, *args, **kwargs):
        return self.send_post_to_subiekt(request,pk=None, *args, **kwargs)

    def get_post_data(self,request,exception=None):
        """ Zwraca odebrany json bez klucza 'exception' """
        data = {}
        for key, value in request.POST.items():
            if exception:
                if key != exception:
                    data[key] = value
            else:
                data[key] = value
        print("{0} - Paczka przygotowana: {1}".format(get_current_datetime(),data))
        return json.loads(json.dumps(data))

    def get_post_datas(self,request,exceptions=None):
        """ Zwraca odebrany json bez klucza 'exception' """
        data = {}
        for key, value in request.POST.items():
            if key in exceptions:
                pass
            else:
                data[key] = value
        print("{0} - Paczka przygotowana: {1}".format(get_current_datetime(),data))
        return json.loads(json.dumps(data))

    def get_template_(self,request,*args,**kwargs):
        """ Zwraca sciezke do template z POST """
        template = request.POST.get('template','')
        print("{0} - Ścieżka do template: {1}".format(get_current_datetime(),template))
        return template

    def get_endpoint_name_(self,request,*args,**kwargs):
        endpoint = request.POST.get('endpoint','')
        print("{0} - Nazwa endpointa: {1}".format(get_current_datetime(),endpoint))
        return endpoint

    def get_endpoint(self,request,*args,**kwargs):
        endpoint = self.get_params(request).get("endpoint","")
        print("{0} - Nazwa endpointa: {1}".format(get_current_datetime(),endpoint))
        return subiekt.get_absolute_endpoint(endpoint)

    def get_json_data(self,request,*args,**kwargs):
        js = json.loads(request.body)
        return js

    def get_fields(self,request,*args,**kwargs):
        fields = self.get_json_data(request).get("fields","")
        print("{0} - Przygotowano paczke z polami: {1}".format(get_current_datetime(),fields))
        return fields

    def get_params(self,request,*args,**kwargs):
        js = self.get_json_data(request)
        return js.get("parameters","")

    def get_template(self,request,*args,**kwargs):
        params = self.get_params(request)
        return params.get("template","")

    def get_subiekt_data(self,request,*args,**kwargs):
        endpoint = self.get_endpoint(request)
        fields = self.get_fields(request)
        r = requests.post(endpoint,data=json.dumps(fields),headers=subiekt.get_header(),verify=False)
        print("{0} - Odebrano:\n{1}".format(get_current_datetime(),r.json()))
        return r

    def get_context_data(self,request,*args,**kwargs):
        context = {}
        context["data"] = self.get_subiekt_data.json()
        return context

    def convert_to_querydict(self,*args,**kwargs):
        from django.http import QueryDict
        ordinary_dict = kwargs['dict']
        query_dict = QueryDict('', mutable=True)
        query_dict.update(ordinary_dict)
        print("{0} - Przekonwerowano słownik na QueryDict: {1}".format(get_current_datetime(),query_dict))
        return query_dict

    def get_form_data(self, request, *args,**kwargs):
        data = json.loads(self.get_fields())
        l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
        q = QueryDict(l)
        print("FORM: {0}\nFORMDATA: {1}".format(kwargs.get("form"),q))
        return q

    def send_post_to_subiekt(self,request,pk=None, *args, **kwargs):
        template = self.get_template(request)
        context = {}
        if subiekt.is_up():
            r = self.get_subiekt_data(request)
            context["data"] = [r.json()]
            return render(request,template,context=context)
            # return JsonResponse({"status": r.status_code,"data": r.json()})
        else:
            print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
            return render(request,template,context=context)
            # return JsonResponse({"status":"failed"})


# TOKEN --------------------------------------------------
class IsSuperUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
class CreateTokenView(ObtainAuthToken):

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_staff': user.is_staff
        })

    def get(self, request, *args, **kwargs):
        queryset = Token.objects.get(user=request.user)
        # qs_json = serializers.serialize('json', queryset)
        return Response({"token": str(queryset)})
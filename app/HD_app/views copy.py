from .imports import *

# WIDOKI ----------------------------------------------------
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
class CompanyView(LoginRequiredMixin,View):
    """ Widok firmy """
    fields = '__all__'
    form_class = Company_Form
    form_address = Address_Form
    model = Company
    template_name = 'HD_app/company_add.html'
    template_form = 'HD_app/forms/company_add_form.html'

    
    def get_context_data(self,**kwargs):
        context = {
            "form": self.form_class,
            "form_address": self.form_address,
            "companies": self.model.objects.all(),
            # "sub_cfg": subiekt.return_json(),
            # "subiekt_status": subiekt.is_subiekt_up()
        }
        return context
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy("Company_add")
    
    def get_object(self,*args,**kwargs):
        return get_object_or_404(self.model,pk=self.kwargs['pk'])
    
    def get(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data()
        if request.is_ajax():
            if request.method == "GET":
                return render(request,self.template_form,{"form":self.form_class,"form_address":self.form_address})
        return render(request, self.template_name, context)
    
    def get_form_data(self, request, *args,**kwargs):
        data = json.loads(request.POST.get('data', ''))
        l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
        q = QueryDict(l)
        print("FORM: {0}\nFORMDATA: {1}".format(kwargs.get("form"),q))
        return q
              
    def post(self, request, pk=None, *args, **kwargs):
        
        company_form = self.form_class(self.get_form_data(request,form="company_add_form"))
        address_form = self.form_address(self.get_form_data(request,form="address_add_form"))

        if company_form.is_valid() and address_form.is_valid():
            company_form.save()
            f = address_form.save(commit=False)
            f.company = company_form.instance
            f.save()
            return JsonResponse({"status":"OK"})
                     
        return render(request,self.template_form,{"form":company_form,"form_address":address_form})
@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDetails(LoginRequiredMixin,UpdateView):
    """ Widok edycji firmy """
    model = Company
    model_address = Address
    form_class = Company_Form
    address_form_class = Address_Form
    address_formset = AddressFormSet
    template_form = 'HD_app/forms/company_detail_form.html'
    template_name_suffix = '_detail'
    
    def get_form_data(self, request, *args,**kwargs):
        data = json.loads(request.POST.get('data', ''))
        l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
        q = QueryDict(l)
        print("FORM: {0}\nFORMDATA: {1}".format(kwargs.get("form"),q))
        return q

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.method == "GET":
                form = self.form_class(instance=self.get_object())
                address_form = self.address_form_class(instance=self.get_default_address())
                return render(request,self.template_form,{"form":form,"form_address":address_form,"rest_addresses":self.get_rest_addresses()})
        return super(CompanyViewDetails, self).get(\
            request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj_address = get_object_or_404(self.model_address,company=obj,is_default=True)
        company_form = self.form_class(self.get_form_data(request,form="company_detail_form"),instance=obj)
        address_form = self.address_form_class(self.get_form_data(request,form="address_detail_form"),instance=obj_address)

        if company_form.is_valid() and address_form.is_valid():
            company_form.save()
            f = address_form.save(commit=False)
            f.company = company_form.instance
            f.save()
            return JsonResponse({"status":"OK"})
                     
        return render(request,self.template_form,{"form":company_form,"form_address":address_form})
            
    def get_success_url(self, **kwargs):         
        return reverse_lazy("Company_add")
    
    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order

    def get_default_address(self,*args,**kwargs):
        return get_object_or_404(self.model_address,company=self.get_object(),is_default=True)

    def get_rest_addresses(self,*args,**kwargs):
        return self.model_address.objects.filter(company=self.get_object(),is_default=False)

@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDelete(LoginRequiredMixin,DeleteView):
    """ Widok usuwania firmy """
    model = Company
    form_class = Company_Form
    success_url = reverse_lazy('Company_add')
    template_name_suffix = '_delete'

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status":"OK"})
        
    def get_object(self,*args,**kwargs):
        return get_object_or_404(self.model,pk=self.kwargs['pk'])

@method_decorator(staff_member_required, name='dispatch')
class CompanyDeleteAjax(LoginRequiredMixin,View):
    model = Company
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

# Company old
@method_decorator(staff_member_required, name='dispatch')
class CompanyView_old(LoginRequiredMixin,View):
    """ Widok firmy """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Company_Form_old
    model = Company
    template_name = 'HD_app/company_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # Context
        context = {
            "form": self.form_class,
            "companies": self.model.objects.all()
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # Return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Odbieranie parametrów POST
        try:
            user = self.request.POST.get('user') if 'user' in request.POST else None
            self.printservice.print_green("field['user']","RECEIVED") if user else self.printservice.print_red("field['user']","NODATA")
        except:
            self.printservice.print_red("field['user']","FAILED")
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            m = form.save(commit=False)
            m.save()
            if user:
                try:
                    u = User.objects.get(pk=user)
                    self.printservice.print_green("User","FOUND")
                except:
                    self.printservice.print_red("User","NOTFOUND")
                try:
                    p = get_object_or_404(Profile,user=u)
                    self.printservice.print_green("Profile","FOUND")
                except:
                    self.printservice.print_red("Profile","NOTFOUND")
                try:
                    p.company = m
                    p.save()
                    self.printservice.print_green("Profile","SAVED")
                except:
                    self.printservice.print_red("Profile","NOTSAVED")
            else:
                self.printservice.print_blue("User","SKIPPED")

            if form.cleaned_data['is_sent']:
                self.printservice.print_green("Password change?","YES")
                redirect_to = reverse("my_password_reset",kwargs={"user_pk":user})
                self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
                self.printservice.print_green("Wyrzucam widok",redirect_to)
                return redirect(redirect_to)
            else:
                self.printservice.print_red("Password change?","NO")

            redirect_to = reverse('Company_add')
            self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
            self.printservice.print_green("Wyrzucam widok",redirect_to)
            return redirect(redirect_to)
        else:
            self.printservice.print_red("Pola formularza","INVALID")
            print(form.errors)
            return render(request, self.template_name, {'form': form})      
@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDetails_old(LoginRequiredMixin,UpdateView):
    """ Widok edycji firmy """
    model = Company
    form_class = Company_Form_old
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CompanyViewDetails, self).get(\
            request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CompanyViewDetails, self).post(\
            request, *args, **kwargs)
    def get_success_url(self, **kwargs):         
        return reverse_lazy("Company_add")
    def get_object(self, *args, **kwargs):
        order = get_object_or_404(Company, pk=self.kwargs['pk'])
        return order
@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDelete_old(LoginRequiredMixin,DeleteView):
    """ Widok usuwania firmy """
    model = Company
    form_class = Company_Form_old
    success_url = reverse_lazy('Company_add')
    template_name_suffix = '_delete'

class Multiforms():
    def __init__(self,*args,**kwargs):
        pass
    def add(self,forms,*args,**kwargs):
        self.forms = forms
        print(self.forms)

    def set_request(self,request):
        self.request = request

    def is_form_in_data(self,*args,**kwargs):
        for key,value in json.loads(self.request.POST.get('data', ''))[0].items():
            if key == kwargs.get("formid"):
                return True

    def saved(self,*args,**kwargs):
        for z in self.forms:
            for key,val in z.items():
                if self.is_form_in_data(formid=kwargs.get("formid","")):
                    form_class = key.get("form_class")
                    form = self.get_form_data(form=form_class)
                    if form.is_valid():
                        form.save()
                        return True
                    else:
                        return False
                        
    def get_form_data(self, request, *args,**kwargs):
        for key,value in json.loads(self.request.POST.get('data', ''))[0].items():
            if key == kwargs.get("form"):
                print(print("{0} - Formularz: {1}".format(get_current_datetime(),key)))
                data = json.loads(request.POST.get('data', ''))
                l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
                q = QueryDict(l)
                print(print("{0} - Przekonwertowano: {1}".format(get_current_datetime(),q)))
                return q           

# Adresy
@method_decorator(staff_member_required, name='dispatch')
class AddressView(LoginRequiredMixin,View):
    """ Widok edycji firmy """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Address_Form_
    model = Address
    template_name = 'HD_app/address_add.html'
    template_form = 'HD_app/forms/address_add_form.html'
    
    def get_form_data(self, request, *args,**kwargs):
        data = json.loads(request.POST.get('data', ''))
        l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
        q = QueryDict(l)
        print("FORM: {0}\nFORMDATA: {1}".format(kwargs.get("form"),q))
        return q

    def get_context_data(self,**kwargs):
        context = {
            "form": self.form_class,
            "addresses": self.model.objects.all(),
        }
        return context


    def get(self, request, pk=None, *args, **kwargs):
        if request.is_ajax():
            print("AJAX")
            if request.method == "GET":
                return render(request,self.template_form,{"form":self.form_class})
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, pk=None, *args, **kwargs):
        form = self.form_class(self.get_form_data(request,form="address_add_form"))
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({"status":"OK"})
        else:
            print(form.errors)
        return render(request,self.template_form,{"form":form})

@method_decorator(staff_member_required, name='dispatch')
class AddressViewDetails(LoginRequiredMixin,UpdateView):
    model = Address
    form_class = Address_Form
    template_name = 'HD_app/address_detail.html'
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AddressViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AddressViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("Address_add")

    def get_object(self, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj
@method_decorator(staff_member_required, name='dispatch')
class AddressViewDelete(LoginRequiredMixin,DeleteView):
    model = Address
    form_class = Address_Form
    template_name = 'HD_app/address_delete.html'
    success_url = reverse_lazy('Address_add')
    template_name_suffix = '_delete'

# Użytkownicy
@method_decorator(staff_member_required, name='dispatch')
class UserView(LoginRequiredMixin,View):
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




        # form = self.form_class(request.POST)

        # if self.is_data(request):
        #     self.create_users_and_profiles(self.get_data_users_list(request))
        #     return JsonResponse({"status":"OK"})
            

        # if form.is_valid():
        #     form.save()
        #     if request.is_ajax():
        #         return JsonResponse({"status":"OK"})
        # return render(request,self.template_form,{"form":form})


        # form = self.form_class(request.POST)
        # tel = request.POST.get('tel')
        # if form.is_valid():
        #     self.printservice.print_green("Pola formularza","VALID")
        #     f=form.save(commit=False)
        #     f.tel = tel
        #     f.save()
           
        #     if form.cleaned_data['password_reset']:
        #         redirect_to = reverse("my_password_reset",kwargs={"user_pk":m.id})
        #         return redirect(redirect_to)
        #     else:
        #         self.printservice.print_red("Password change?","NO")

        #     redirect_to = reverse('User_add')
        #     self.printservice.print_green("Wyrzucam widok",redirect_to)

        #     return redirect(redirect_to)
        # else: 
        #     print(form.is_valid())
        #     print(form.errors)
        #     return render(request, self.template_name, {'form': form}) 


@method_decorator(staff_member_required, name='dispatch')
class UserViewDetails(LoginRequiredMixin,UpdateView):
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
class UserViewDelete(LoginRequiredMixin,DeleteView):
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
# Dodatkowe Ajax
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
# Profil
@method_decorator(staff_member_required, name='dispatch')
class ProfileViewDetails(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = Profile_Form
    user_form = User_Form
    template_name = 'HD_app/profile_detail.html'
    template_name_suffix = '_detail'
    context_object_name = 'imie'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfileViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        rq = request.POST
        u = self.get_user_object()
        u.first_name = rq.get('imie')
        u.last_name = rq.get('nazwisko')
        u.email = rq.get('email')
        u.save()
        return super(ProfileViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("User_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
    def get_user_object(self, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(pk=profile.user.pk)
        return user

# Umowy
@method_decorator(staff_member_required, name='dispatch')
class AgreementView(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Agreement_Form
    form_class_pakiet = PakietForm
    model = Agreement2
    template_name = 'HD_app/agreement_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
        context = {
            "form": self.form_class,
            "form_pakiet": self.form_class_pakiet,
            "agreements": self.model.objects.all()
        }
        return render(request, self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            form.save()
            # return JsonResponse({"status": "OK"})
    # Return
        redirect_to = reverse('Agreement_add')
        self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
        self.printservice.print_green("Wyrzucam widok",redirect_to)
        return redirect(redirect_to)
        # return render(request, self.template_name, {'form': self.form_class})        
@method_decorator(staff_member_required, name='dispatch')
class AgreementViewDetails(LoginRequiredMixin,UpdateView):
    model = Agreement2
    form_class = Agreement_Form
    template_name = 'HD_app/agreement_detail.html'
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AgreementViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AgreementViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("Agreement_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
@method_decorator(staff_member_required, name='dispatch')
class AgreementViewDelete(LoginRequiredMixin,DeleteView):
    model = Agreement2
    form_class = Agreement_Form
    template_name = 'HD_app/agreement_delete.html'
    success_url = reverse_lazy('Agreement_add')
    template_name_suffix = '_delete'

# Zlecenia
@method_decorator(staff_member_required, name='dispatch')
class OrderView(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Order_Form
    form_class_template = OrderTemplateForm
    model = Order
    template_name = 'HD_app/order_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
        self.user = self.request.user
    # Context
        context = {
            "form": self.form_class(),
            "form_ordertemplate": self.form_class_template,
            "orders": self.model.objects.all()
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # Return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            form.save()
        else:
            self.printservice.print_red("Pola formularza","INVALID")
            print(form.errors)
            return render(request, self.template_name, {'form': form})
    # Return
        redirect_to = reverse('Order_add')
        self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
        self.printservice.print_green("Wyrzucam widok",redirect_to)
        return redirect(redirect_to)
@method_decorator(staff_member_required, name='dispatch')
class OrderViewDetails(LoginRequiredMixin,UpdateView):
    model = Order
    form_class = Order_Form
    template_name = 'HD_app/order_detail.html'
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OrderViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OrderViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("Order_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
@method_decorator(staff_member_required, name='dispatch')
class OrderViewDelete(LoginRequiredMixin,DeleteView):
    model = Order
    form_class = Order_Form
    template_name = 'HD_app/order_delete.html'
    success_url = reverse_lazy('Order_add')
    template_name_suffix = '_delete'

@method_decorator(staff_member_required, name='dispatch')
class PakietView(View):
    fields = '__all__'
    form_class = PakietForm
    model = Pakiet
    template_name = 'HD_app/pakiet_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        context = {
            "form":self.form_class,
            }
        return render(request,self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            if request.is_ajax():
                 return JsonResponse({"status":"OK"})
            else:
                return redirect(reverse("Pakiet_add"))
        else:
            if request.is_ajax():
                return JsonResponse({"errors":form.errors.as_json()})
            else:
                return render(request, self.template_name, {"form":form,"form_ratestack":form_ratestack})
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
    agreement = request.GET.get('agreement',None)
    try:
        a = Agreement2.objects.get(pk=agreement)
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
    a = request.GET.get('a',None)
    try:
        ag = Agreement2.objects.get(pk=a)
        ad = Address.objects.filter(company__id=ag.company.id)
        data = ad.values_list("id", flat=True).order_by("id")
        return JsonResponse({"id":list(data)}, content_type='application/json')
    except:
        return JsonResponse({},content_type='application/json')
@staff_member_required
def JSON_rozlicz_zlecenie(request):
    from django.core.serializers.json import DjangoJSONEncoder
    order = request.GET.get('order',None)
    o = Order.objects.get(pk=order)
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
    
    o = Order.objects.all().filter(agreement__id=a).filter(start_datetime__gte=start, end_datetime__lte=end)
    
    ou = Order.objects.all().filter(agreement__id=a, care__id=u).filter(start_datetime__gte=start, end_datetime__lte=end)
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



#######################################################
#######################################################
#######################################################
# Nowe
#######################################################
#######################################################
#######################################################


# Klasy Subiekt API ------------------------------------
class SubiektFormOperations():
    """ Klasa operacji na ciele formularza ajax """
    def __init__(self,*args,**kwargs):
        pass

    def get_form_data(self,request,*args,**kwargs):
        """ Wybiera dane z przesłanego formularza """
        for key,value in json.loads(request.POST.get('data', ''))[0].items():
            if key == kwargs.get("form"):
                print(print("{0} - Formularz: {1}".format(get_current_datetime(),key)))
                data = json.loads(request.POST.get('data', ''))
                l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
                q = QueryDict(l)
                return q 

    def is_form_in_data(self,request,*args,**kwargs):
        """ Sprawdza czy są dane w formularzu """
        for key,value in json.loads(request.POST.get('data', ''))[0].items():
            if key == kwargs.get("formid"):
                return True

    def get_subiekt_data(self,request,*args,**kwargs):
        """ Wysyła dane do subiekta i zwraca odebrane dane """
        form = kwargs['form']
        endpoint = kwargs['endpoint']
        cleaned_data = form.cleaned_data
        print("{0} - Endpoint do wysyłki: {1}".format(get_current_datetime(),endpoint))
        print("{0} - Wysyłam paczke na endpoint subiekta...:\n{1}".format(get_current_datetime(),cleaned_data))
        r = requests.post(endpoint,data=json.dumps(cleaned_data),headers=subiekt.get_header(),verify=False)
        print("{0} - Odebrano:\n{1}".format(get_current_datetime(),r.json()))
        return r
class SubiektStatus(View):
    """ Status subiekta """
    def get(self,request,*args,**kwargs):
        context = {}
        if subiekt.is_up():
            context['status'] = status.HTTP_200_OK
            return JsonResponse(context)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            return JsonResponse(context)

# Widoki -----------------------------------------------
@method_decorator(staff_member_required,name='dispatch')
class DashboardView(LoginRequiredMixin,View):
    
    """ Dashboard """
    template_name = "HD_app/subiekt/dashboard/dashboard.html"

    def get(self,request,*args,**kwargs):
        return render(request, self.template_name, self.get_context(request,*args,**kwargs))

    def get_context(self,request,*args,**kwargs):
        context = {
            "inbox":Message.objects.filter(receipt=request.user),
            "sent": Message.objects.filter(sender=request.user),
        }
        return context    
def home(request):
    """ Przekierowanie na dashboard """
    return HttpResponseRedirect("dashboard")

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

# @method_decorator(staff_member_required, name='dispatch')
# class SubiektAPICompanyListView(LoginRequiredMixin,View):

#     """ Listowanie firm dla formularzy, """
#     template_list = "HD_app/subiekt/company/company_list.html"
#     endpoint = subiekt.get_absolute_endpoint("firmy")
#     search_form = SubiektCompanySearchForm

#     def __init__(self,*args,**kwargs):

#         self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

#     def get_fields(self,request,*args,**kwargs):
#         fields = self.get_json_data(request).get("fields","")
#         print("{0} - Przygotowano paczke z polami: {1}".format(get_current_datetime(),fields))
#         return fields

#     def get_json_data(self,request,*args,**kwargs):
#         js = json.loads(request.body)
#         return js

#     def get_fields(self,request,*args,**kwargs):
#         fields = self.get_json_data(request).get("fields","")
#         print("{0} - Przygotowano paczke z polami: {1}".format(get_current_datetime(),fields))
#         return fields

#     def get_params(self,request,*args,**kwargs):
#         js = self.get_json_data(request)
#         return js.get("parameters","")
    
#     def get_form_data(self, request, *args,**kwargs):
#         data = json.loads(request.POST.get('data', ''))
#         l = [v for x in data for c,v in x.items() if c == kwargs.get("form")][0]
#         q = QueryDict(l)
#         return q  

#     def get_subiekt_data(self,request,*args,**kwargs):
#         fields = self.get_fields(request)
#         r = requests.post(self.endpoint,data=json.dumps(fields),headers=subiekt.get_header(),verify=False)
#         print("{0} - Odebrano:\n{1}".format(get_current_datetime(),r.json()))
#         return r

#     def post(self, request, pk=None, *args, **kwargs):
#         search_form = self.search_form(self.get_form_data(request,form="company_search_form"))
#         context = {}
#         if subiekt.is_up():
#             subiekt_data = self.get_subiekt_data(request)
#             context["data"] = [subiekt_data.json()]
#             return render(request,self.template_list,context=context)
#         else:
#             print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
#             return render(request,self.template_list,context=context)
# @method_decorator(staff_member_required, name='dispatch')
class SubiektAPICompanyCreateView(LoginRequiredMixin,View):

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

    def __init__(self,*args,**kwargs):
        self.sf = SubiektFormOperations()
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")


    def get_context_data(self,**kwargs):
        context = {
            "create_form": self.create_form,
            "search_form":self.search_form
        }
        return context

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


@method_decorator(staff_member_required, name='dispatch')
class SubiektAPICompanyDetailView(LoginRequiredMixin,View):
    """ Wyswietlanie instancji obiektu firmy z subiekta i nadpisywanie jego danych """
    template_name = "HD_app/subiekt/company/company_detail_form.html"
    endpoint = subiekt.get_absolute_endpoint("kontrahenci")


    # Formularz trzeba tak stworzyc aby pola odpowiadały odebranym polom z subiekta ,
    # czyli stworzyc pola Id,Nazwa itd. Poza tym widok musi zwracac instancje jednego obiektu
    # która zostanie zrenderowana na ten formularz
    form_class = SubiektCompanyCreateForm

    def __init__(self):
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")

    def get_subiekt_object(self,request, *args, **kwargs):
        """ Zwraca obiekt Querydict subiekta """
        # data = {self.keyid_send:self.get_subiekt_id(request,*args,**kwargs)}
        data = self.get_ajax_data(request,*args,**kwargs)
        print(f"{get_current_datetime()} - Wysyłam do {self.endpoint}\n{data}")
        obj = requests.post(self.endpoint,data=json.dumps(data),headers=subiekt.get_header(),verify=False)
        print(f"{get_current_datetime()} - Odebrano: \n{obj.json()}")

        # Musi byc 1 obiekt 
        # q = QueryDict(obj)
        return obj.json().get("KontrahenciList")[0]


    def get_ajax_data(self,request,*args,**kwargs):
        """ Zwraca data """
        return json.loads(request.GET.get("data",""))

    def is_data(self,request,*args,**kwargs):
        """ Sprawdza czy jest data w paczce ajax """
        if json.loads(request.GET.get("data",None)):
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.method == "GET":
                if self.is_data(request,*args,**kwargs):
                    if subiekt.is_up():
                        obj = self.get_subiekt_object(request,*args,**kwargs)

                        form = self.form_class(obj)
                        return render(request,self.template_name,{"form":form})

        return super(UserViewDetails, self).get(\
            request, *args, **kwargs)

@method_decorator(staff_member_required, name='dispatch')
class MessageCreateView(LoginRequiredMixin,View):
    """ Dodawanie nowej wiadomości """
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
        # return render(request, self.template_name, context)
        return render(request,self.template_create_form,{"create_form":self.create_form})

            
    def post(self, request, pk=None, *args, **kwargs):
        if self.sf.is_form_in_data(request,formid="message-add-form"):
            create_form = self.create_form(self.sf.get_form_data(request,form="message-add-form"))
            if create_form.is_valid():
                form = create_form.save(commit=False)
                form.sender = request.user
                form.save()
                create_form.save_m2m()
                print(create_form)
                if request.is_ajax():
                    return JsonResponse({"status":status.HTTP_200_OK,"Message":"Zapisano"})
                else:
                    print(print("{0} - Błąd: Subiekt offline!".format(get_current_datetime())))
                    if request.is_ajax():
                        return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"Message":"Błąd"})
            else:
                print(f"Błąd: {create_form.errors} \n")
                if request.is_ajax():
                    # return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"Message":"Błąd pól formularza","content":self.get(request,*args,**kwargs)})   
                    return render(request,self.template_create_form,context={"create_form":create_form})
@method_decorator(staff_member_required, name='dispatch')
class MessageInboxListView(LoginRequiredMixin,View):
    
    model = Message
    template_name = ""

    def get(self,request,*args,**kwargs):
        """ GET """
        return self.inbox(request,*args,**kwargs)



    def post(self,request,*args,**kwargs):
        """ POST """
        pk = self.request.POST.get("read",None)
        self.make_read(pk,request,*args,**kwargs) if pk else None



    def inbox(self,request,*args,**kwargs):
        """ INBOX """
        if request.is_ajax():
            return render(request, self.template_name, self.get_context_data(request,*args,**kwargs))



    def make_read(self,pk,request,*args,**kwargs):
        """ Updatowanie is_read() """
        if request.is_ajax():
            msg = self.model.objects.filter(pk=pk)
            msg.is_read = True
            msg.save()



    def get_context_data(self,request,*args,**kwargs):
        """ CONTEXT """
        context = {
            "inbox": "",
        }
        return context
@method_decorator(staff_member_required, name='dispatch')
class MessageDetailView(LoginRequiredMixin,View):
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


# Filtr Zleceń
@method_decorator(staff_member_required, name='dispatch')
class Raport1View(LoginRequiredMixin,View):
    """ Filtr zleceń """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    template_name = 'HD_app/raport_order_1.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # Daty
        try:
            today = datetime.today()
            today2 = datetime.today()+timedelta(days=1)
            begin = today.replace(day=1,month=today.month,year=today.year)
            begin2 = today.replace(day=1,month=today.month,year=today.year)-timedelta(days=1)
            dayss = np.busday_count(begin2.date(),today2.date())
            self.printservice.print_green("Daty","OK")
        except:
            self.printservice.print_red("Daty","FAILED")
    # Q object
        try:
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=begin.date(), end_datetime__date__lte=today.date()))
            self.printservice.print_green("Q object","OK")
        except:
            self.printservice.print_green("Q object","FAILED")
    # Efektywność
        try:
            hh = 8
            li = [(c.calculate_timedelta()/60)/60 for c in obj]
            li2 = [{"id":c.care.id,"calculated":(c.calculate_timedelta()/60)/60,"suma":c.calculate_order(),"suma_d":c.calculate_order_with_distance()} for c in obj]
            df = pd.DataFrame(li2)
            df2=df.groupby(['id']).sum()
            ddd = df2.to_dict('index')
            df3 = dict()
            fulltime = hh*dayss
            lis = [{'worker':x,'calculated':y['calculated'],'efficiency':(y['calculated']/fulltime)*100,"suma":y['suma'],"suma_d":y['suma_d'],"fulltime":fulltime } for x,y in ddd.items()]
            self.printservice.print_green("Efektywność","OK")
        except:
            self.printservice.print_red("Efektywność","FAILED")
        self.user = self.request.user
    # Context
        context = {
            "orders": obj,
            "ratestacks": RateStack.objects.all(),
            "rates": Rate.objects.all(),
            "workers": User.objects.filter(is_staff=True,id__in=[obj.values_list("care__id")]),
            "allworkers": User.objects.filter(is_staff=True),
            "companies": Company.objects.filter(id__in=[obj.values_list("agreement__company__id")]),
            "agreements": Agreement2.objects.filter(id__in=[obj.values_list("agreement_id")]),
            "order_types": OrderType.objects.all(),
            "order_status": OrderStatus.objects.all(),
            "suma":sum([c.calculate_order() for c in obj]),
            "count_orders":len(obj),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in obj]),
            "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            "efficiency": None if not 'lis' in locals() else lis
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # Return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
# Filtr zleceń z parametrami
@method_decorator(staff_member_required, name='dispatch')
class Raport1View_filteredByTime(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    template_name = 'HD_app/raport_order_1.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # GET
        try:
        # Definiowanie parametrów w zmiennych w pętli
            for x,y in self.request.GET.items():
                globals()[x] = self.request.GET.get(x,None)
                self.printservice.print_green(x,"OK") if globals()[x] != "0" else self.printservice.print_red(x,"ALL")
            self.printservice.print_green("Parametry GET","OK")
        except:
            self.printservice.print_red("Parametry GET","FAILED")
    # Konwersja GET
        try:
            today = datetime.today().date()
            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True))
            stt = list(OrderStatus.objects.all().values_list("id",flat=True)) if st == "0" else list(OrderStatus.objects.filter(pk=st).values_list("id",flat=True))
            self.printservice.print_green("Konwersja GET","OK") 
        except:
            self.printservice.print_red("Konwersja GET","FAILED") 
    # Q object    
        try:  
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,order_status__id__in=stt,agreement__company__id__in=cc))
            self.printservice.print_green("Q object","OK")
            self.printservice.print_green("Orders",[x.id for x in obj])
        except:
            self.printservice.print_green("Q object","FAILED")
    # Printy
        self.printservice.print_green("OrderType",tt)
        self.printservice.print_green("Pracownik",ww)
        self.printservice.print_green("Firma",cc)
        self.printservice.print_green("Start",ss)
        self.printservice.print_green("End",ee)
    # Efektywność
        try:
            today = datetime.today().date()
            dayss = np.busday_count(ss-timedelta(days=1),ee+timedelta(days=1))
            hh = 8
            li = [(c.calculate_timedelta()/60)/60 for c in obj]
            li2 = [{"id":c.care.id,"calculated":(c.calculate_timedelta()/60)/60,"suma":c.calculate_order(),"suma_d":c.calculate_order_with_distance()} for c in obj]
            df = pd.DataFrame(li2)
            df2=df.groupby(['id']).sum()
            ddd = df2.to_dict('index')
            df3 = dict()
            fulltime = hh*dayss
            lis = [{'worker':x,'calculated':y['calculated'],'efficiency':(y['calculated']/fulltime)*100,"suma":y['suma'],"suma_d":y['suma_d'],"fulltime":fulltime } for x,y in ddd.items()]
            self.printservice.print_green("Efektywność","OK") 
        except:
            self.printservice.print_red("Efektywność","FAILED")
    # Context
        # OrderStatus (zrealizowane)
        included_status = 6
        context = {
            "orders":obj,
            "suma":sum([c.calculate_order() for c in obj]),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
            "workers": User.objects.filter(is_staff=True,id__in=[obj.values_list("care__id")]),
            "allworkers": User.objects.filter(is_staff=True),
            "order_types": OrderType.objects.all(),
            # "companies": Company.objects.all(),
            "count_orders":len(obj),
            "count_orders_completed":len(obj.filter(order_status__pk=included_status)),
            "count_orders_notcompleted":len(obj)-len(obj.filter(order_status__pk=included_status)),
            "order_status":OrderStatus.objects.all(),
            "companies": Company.objects.filter(id__in=[obj.values_list("agreement__company__id")]),
            "agreements": Agreement2.objects.filter(id__in=[obj.values_list("agreement_id")]),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in self.model.objects.all()]),
            "efficiency": None if not 'lis' in locals() else lis,
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
        #return render(request, self.template_name, context={"workers": User.objects.filter(is_staff=True),"order_types": OrderType.objects.all()})
# Generator raportu
@method_decorator(staff_member_required, name='dispatch')
class GenerateRaport(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    template_name = 'HD_app/order_raport.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # GET
        try:
        # Definiowanie parametrów w zmiennych w pętli
            for x,y in self.request.GET.items():
                globals()[x] = self.request.GET.get(x,None)
                self.printservice.print_green(x,"OK") if globals()[x] != "0" else self.printservice.print_red(x,"ALL")
            self.printservice.print_green("Parametry GET","OK")
        except:
            self.printservice.print_red("Parametry GET","FAILED")
    # Konwersja GET
        try:
            today = datetime.today().date()
            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True))
            aa = list(Agreement2.objects.all().values_list("id",flat=True)) if a == "0" else list(Agreement2.objects.filter(pk=a).values_list("id",flat=True))
            self.printservice.print_green("Konwersja GET","OK") 
        except:
            self.printservice.print_red("Konwersja GET","FAILED") 
    # Q object    
        try:  
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,agreement__company__id__in=cc))
            self.printservice.print_green("Q object","OK")
            self.printservice.print_green("Orders",[x.id for x in obj])
        except:
            self.printservice.print_green("Q object","FAILED")
    # Printy
        self.printservice.print_green("OrderType",tt)
        self.printservice.print_green("Pracownik",ww)
        self.printservice.print_green("Firma",cc)
        self.printservice.print_green("Start",ss)
        self.printservice.print_green("End",ee)
    # Efektywność
        try:
            today = datetime.today().date()
            dayss = np.busday_count(ss-timedelta(days=1),ee+timedelta(days=1))
            hh = 8
            li = [(c.calculate_timedelta()/60)/60 for c in obj]
            li2 = [{"id":c.care.id,"calculated":(c.calculate_timedelta()/60)/60,"suma":c.calculate_order(),"suma_d":c.calculate_order_with_distance()} for c in obj]
            df = pd.DataFrame(li2)
            df2=df.groupby(['id']).sum()
            ddd = df2.to_dict('index')
            df3 = dict()
            fulltime = hh*dayss
            lis = [{'worker':x,'calculated':y['calculated'],'efficiency':(y['calculated']/fulltime)*100,"suma":y['suma'],"suma_d":y['suma_d'],"fulltime":fulltime } for x,y in ddd.items()]
            self.printservice.print_green("Efektywność","OK") 
        except:
            self.printservice.print_red("Efektywność","FAILED")
    # Context
        ordertype_rozliczone = 6
        context = {
            "orders":obj,
            "orders_count":len(obj),
            "suma":sum([c.calculate_order() for c in obj]),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
            "workers": User.objects.filter(is_staff=True,id__in=[obj.values_list("care__id")]),
            "allworkers": User.objects.filter(is_staff=True),
            "order_types": OrderType.objects.filter(id__in=[obj.values_list("order_type__id")]),
            "companies": Company.objects.filter(id__in=[obj.values_list("agreement__company__id")]),
            "agreements": Agreement2.objects.filter(id__in=[obj.values_list("agreement__id")]),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in obj]),
            "efficiency": None if not 'lis' in locals() else lis,
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
        #return render(request, self.template_name, context={"workers": User.objects.filter(is_staff=True),"order_types": OrderType.objects.all()})
# Rozliczanie
@method_decorator(staff_member_required, name='dispatch')
class AccountOrders(LoginRequiredMixin,View):
    """ Rozliczanie zleceń """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    def get(self,request,pk=None,*args,**kwargs):
        return JsonResponse(request.GET.dict())
    def post(self,request,pk=None,*args,**kwargs):
    # POST
        try:
            # Definiowanie parametrów w zmiennych w pętli
            for x,y in self.request.POST.items():
                globals()[x] = self.request.POST.get(x,None)
                self.printservice.print_green(x,"OK") if globals()[x] != "0" else self.printservice.print_red(x,"ALL")
            self.printservice.print_green("Parametry POST","OK")
        except:
            self.printservice.print_red("Parametry GET","FAILED")
    # Konwersja POST
        try:
            # OrderStatus - wszystkie procz, bedą updatowane
            excluded_status = 6

            today = datetime.today().date()
            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True))
            stt = list(OrderStatus.objects.exclude(pk=excluded_status).values_list("id",flat=True)) if st == "0" else list(OrderStatus.objects.filter(pk=st).values_list("id",flat=True))
            self.printservice.print_green("Konwersja POST","OK") 
        except:
            self.printservice.print_red("Konwersja POST","FAILED") 
    # Q object    
        try:  
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,order_status__id__in=stt,agreement__company__id__in=cc))
            self.printservice.print_green("Q object","OK")
            self.printservice.print_green("Orders",[x.id for x in obj])
        except:
            self.printservice.print_green("Q object","FAILED")            
    # Q object override
        try:
            try:
                include_status = 6
                os = OrderStatus.objects.filter(pk=include_status).first()
                self.printservice.print_green("Ordertype","SELECTED")
            except:
                self.printservice.print_red("Ordertype","NOTFOUND")
            obj.update(order_status=os)
            self.printservice.print_green("Order update","OVERIDED")
        except:
            self.printservice.print_red("Order update","FAILED")
    # Return
        return JsonResponse(request.POST.dict())

# Zestawienie Umów
@method_decorator(staff_member_required, name='dispatch')
class Raport2View(LoginRequiredMixin,View):
    fields = '__all__'
    model = Agreement2
    template_name = 'HD_app/raport_agreement_1.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.user = self.request.user
    # GET
        try:
            print("%s\nOdbieram bane z GET..." % ("-"*30))
            s = self.request.GET.get('s',None)
            e = self.request.GET.get('e',None)
            t = self.request.GET.get('t',None)
            w = self.request.GET.get('w',None)
            c = self.request.GET.get('c',None)
            print("+ OK")
        except:
            print("- Brak danych z GET")
    # Przygotowanie zakresu dat
        try:
            print("%s\nRozpoczynam kalkulacje zakresu dat" % ("-"*30,))
            print("* Obliczanie dni bezweekendowych...")
            today = datetime.today()
            begin = today.replace(day=1,month=today.month,year=today.year)
            dayss = np.busday_count(begin.date(),today.date())
            print("* Zakres dat: %s - %s" % (begin.date(), today.date()))
            print("* Dni bez weekendów: %s" % dayss)
        except:
            print("- Błąd konwersji dat nieweekendowych")
    # Querysets
        orders_u = Order.objects.filter(care__isnull=False).values_list('id', flat=True)
        orders_au = Order.objects.filter(care__isnull=False).values_list('agreement', flat=True)
        orders_uo = Order.objects.filter(care__isnull=False)
        workers_with_orders = User.objects.filter(id__in=orders_u, is_staff=True)
    # Context
        context = {
            "agreements": self.model.objects.all(),
            "orders": Order.objects.all(),
            "companies": Company.objects.all(),
            "workers": User.objects.filter(is_staff=True),
            "czasy" : Order.objects.all().aggregate(diff=Avg(F('end_datetime') - F('start_datetime'))),
            "workers_with_orders": workers_with_orders,
            "orders_u":orders_u,
            "orders_uo":orders_uo,
            "orders_au":orders_au,
            "order_types": OrderType.objects.all(),
            "suma":sum([c.calculate_order() for c in Order.objects.all()]),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in Order.objects.all()]),
            "suma_km": sum([float(c) for c in Order.objects.all().values_list("address__distance",flat=True) if c]),
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in Order.objects.all()]),
            }
    # Return
        return render(request, self.template_name, context)
# Filtry Umów
@method_decorator(staff_member_required, name='dispatch')
class Agreement1View_filteredByTime(LoginRequiredMixin,View):
    fields = '__all__'
    model = Agreement2
    template_name = 'HD_app/raport_agreement_1.html'
    def get(self, request, pk=None, *args, **kwargs):

        try:

            s = self.request.GET.get('s',None)
            e = self.request.GET.get('e',None)
            t = self.request.GET.get('t',None)
            w = self.request.GET.get('w',None)
            c = self.request.GET.get('c',None)

            today = datetime.today().date()

            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(month=1,day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True)) 
            
            # Q object
            obj = Order.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,agreement__company__id__in=cc))
        
            print("-"*30)
            print("Przeszukuje Q...")
            print(obj)
            print("-"*30)
            print("Ordertype: %s" % tt)
            print("Worker: %s" % ww)
            print("Firma: %s" % cc)
            print("Start: %s" % ss)
            print("End: %s" % ee)
            print("-"*30)

            start = ss
            end = ee

            orders_ = obj
            orders_u = obj.values_list('id', flat=True)
            orders_us = obj.values_list('care__id', flat=True)
            orders_au = obj.values_list('agreement', flat=True)
            orders_uo = obj
            agreements_= self.model.objects.filter(id__in=[a.agreement.id for a in orders_])
            #workers_with_orders = User.objects.filter(id__in=orders_u, is_staff=True)
            workers_with_orders = User.objects.filter(id__in=orders_us, is_staff=True)

            print(workers_with_orders)



            context = {
                "workers": User.objects.filter(is_staff=True),
                "workers_a": User.objects.filter(is_staff=True).filter(id__in=[u.id for u in workers_with_orders]),
                "agreements": agreements_,
                "companies": Company.objects.all(),
                "orders": obj,
                "orders_u":orders_u,
                "orders_uo":orders_uo,
                "orders_au":orders_au,
                "workers_with_orders": workers_with_orders,
                "order_types": OrderType.objects.all(),
                "suma":sum([c.calculate_order() for c in obj]),
                "suma_km_costs":sum([c.calculate_order_with_distance() for c in obj]),
                "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
                "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
                "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            }
            return render(request, self.template_name, context)

        except:
            context= {
                "companies": Company.objects.all(),
                "workers": User.objects.filter(is_staff=True),
                "order_types": OrderType.objects.all(),
            }
            return render(request, self.template_name, context)
# Filtry zleceń dla Umowy w czasie
@method_decorator(staff_member_required, name='dispatch')
class OrderAgreement1View_filteredByTime(LoginRequiredMixin,View):
    """
    Widok raportu serwisowego
    """
    fields = '__all__'
    model = Agreement2
    template_name = 'HD_app/raport_order_1_agreement_filteredbytime.html'
    def get(self, request, pk=None, *args, **kwargs):
        try:
            s = self.request.GET.get('s')
            start = datetime.strptime(s, "%Y-%m-%d").date()
            e = self.request.GET.get('e')
            end = datetime.strptime(e, "%Y-%m-%d").date()

            a = self.request.GET.get('a')
            print("Przeszukuje umowe id...: %s" % a)
            agreement = Agreement2.objects.get(pk=a)
            print(agreement)
            
            u = self.request.GET.get('u')
            print("Przeszukuje usera id...: %s" % u)
            worker = User.objects.get(pk=u)
            print(worker)

            print("Przeszukuje zlecenia opikuna: %s, umowy:  %s, w zakresie od: %s, do: %s" % (worker,agreement,start,end))
            orders = Order.objects.filter(care__isnull=False).filter(start_datetime__gte=start, end_datetime__lte=end, care=worker, agreement=agreement)
            print(orders)

            if start != "" and end != "" and u != "" and a != "":
                print("Wyszukuje w zakresie od ... %s > do %s" % (start,end))
                context = {
                    "start":start,
                    "end":end,
                    "agreement":agreement,
                    "worker": worker,
                    "orders":orders
                }
                return render(request, self.template_name, context=context)
                
        except:
            return render(request, self.template_name, context={})


# INNE --------------------------------------------------
class Stats(APIView):

    def get(self, request, format=None):

        current_day = datetime.today()
        current_time = current_day.time()
        start_time = current_time.replace(hour=8, minute=0, second=0)
        end_time = current_time.replace(hour=16, minute=59, second=59)
        complete_shift_start = datetime.combine(current_day.date(), start_time)
        complete_shift_end = datetime.combine(current_day.date(), end_time)
        time_8a = datetime.combine(current_day.date(), current_time.replace(hour=8, minute=0, second=0))
        time_8b = datetime.combine(current_day.date(), current_time.replace(hour=8, minute=59, second=59))

        stan = 'W realizacji'

        shift_times = ['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00',]

        processing_graph = {
            '08:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=8, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=8, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '09:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=9, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=9, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '10:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=10, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=10, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '11:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=11, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=11, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '12:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=12, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=12, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '13:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=13, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=13, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '14:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=14, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=14, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '15:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=15, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=15, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '16:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=16, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=16, minute=59, second=59))], order_status__name__icontains=stan).count(),
            
        }
        stan = 'Zrealizowane'
        completed_graph = {
            '08:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=8, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=8, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '09:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=9, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=9, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '10:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=10, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=10, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '11:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=11, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=11, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '12:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=12, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=12, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '13:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=13, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=13, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '14:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=14, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=14, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '15:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=15, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=15, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '16:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=16, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=16, minute=59, second=59))], order_status__name__icontains=stan).count(),
        }
        
        d = Order.objects.extra({'x': 'date(created_date)'}).values('x').annotate(y=Count('id'))
        ds = ServiceOrder.objects.extra({'x': 'date(created_date)'}).values('x').annotate(y=Count('id'))
        s = Order.objects.extra({'x': 'date(start_datetime)'}).values('x').annotate(y=Count('id'))
        ss = ServiceOrder.objects.extra({'x': 'date(start_datetime)'}).values('x').annotate(y=Count('id'))
        e = Order.objects.extra({'x': 'date(end_datetime)'}).values('x').annotate(y=Count('id'))
        p = Order.objects.filter(order_status__name__icontains='W realizacji').extra({'x': 'date(created_date)'}).values('x').annotate(y=Count('id'))
        ptc = Order.objects.filter(created_date__date=datetime.today()).filter(order_status__name__icontains='W realizacji').extra({'x': 'time(created_date)'}).values('x').annotate(y=Count('id'))

        c_order_processing = Order.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], order_status__name__icontains='W realizacji').count()
        
        order_processing = Order.objects.filter(agreement__company__care=request.user, order_status__name__icontains='W realizacji').count()
        order_completed = Order.objects.filter(agreement__company__care=request.user, order_status__name__icontains='Zrealizowane').count()
        c_order_completed = Order.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], order_status__name__icontains='Zrealizowane').count()
        
        cs_order_processing = ServiceOrder.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], status__name__icontains='W realizacji').count()
        csc_order_completed = ServiceOrder.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], status__name__icontains='Zrealizowane').count()

        # Queries
        qs = Order.objects.filter(\
            updated_date__year=datetime.now().year, 
            updated_date__month=datetime.now().month
            ).annotate(\
                day=ExtractDay('updated_date'),
                month=ExtractMonth('updated_date')
                ).values(\
                    'day',
                    'month',
                    'updated_date__date'
                    ).annotate(\
                        n=Count('pk')
                        ).order_by(\
                            'day'
                            )
        qs1 = Order.objects.filter(\
            updated_date__year=datetime.now().year, 
            updated_date__month=datetime.now().month,
            order_status__name__icontains="W realizacji",
            ).annotate(\
                day=ExtractDay('updated_date'),
                month=ExtractMonth('updated_date'),
                ).values(\
                    'day',
                    'month',
                    'updated_date__date'
                    ).annotate(\
                        n=Count('pk')
                        ).order_by(\
                            'day'
                            )
        qs2 = Order.objects.filter(\
            updated_date__year=datetime.now().year, 
            updated_date__month=datetime.now().month, 
            order_status__name__icontains="Zrealizowane"
            ).annotate(\
                day=ExtractDay('updated_date'),
                month=ExtractMonth('updated_date')
                ).values(\
                    'day',
                    'month',
                    'updated_date__date'
                    ).annotate(\
                        n=Count('pk')
                        ).order_by(\
                            'day'
                            )

        
        def days_cur_month():
            m = datetime.now().month
            y = datetime.now().year
            ndays = (date(y, m+1, 1) - date(y, m, 1)).days
            d1 = date(y, m, 1)
            d2 = date(y, m, ndays)
            delta = d2 - d1
            return [(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
        def get_hours():
            import datetime as dt
            hours = [(dt.time(i).strftime('%H:%M')) for i in range(24)]
            return hours
        def make_timeline(days, qs, time_field, value_field):
            timeline1 = {}
            for d in days:
                timeline1.update({d: 0})
                for k in qs:
                    if str(d) == str(k[time_field]):
                        timeline1[d] = k[value_field]
            return timeline1
        
        # Complete timelines
        timeline_month_1 = make_timeline(\
            days=days_cur_month(), 
            qs=qs1, 
            time_field='updated_date__date', 
            value_field='n')
        timeline_month_2 = make_timeline(\
            days=days_cur_month(), 
            qs=qs2, 
            time_field='updated_date__date', 
            value_field='n')
        timeline_month_3 = make_timeline(\
            days=days_cur_month(), 
            qs=qs, 
            time_field='updated_date__date', 
            value_field='n')

        unread_messages = Message.objects.filter(receipt=request.user, is_read=False).count()
        
        # Nie wiem czemu musi tutaj byc import?
        from HD_app.models import Company
        companies_not_accepted = Company.objects.filter(is_accepted=False).count()
        myserviceorders = ServiceOrder.objects.filter(care=request.user, status__name__icontains="W realizacji").count()
        myserviceorders_per_company = ServiceOrder.objects.filter(company__care=request.user, status__name__icontains="W realizacji").count()
        myserviceorders_per_company_zrealizowane = ServiceOrder.objects.filter(company__care=request.user, status__name__icontains="Zrealizowane").count()
        


        output = {
            'orders_created_per_day': d,
            'orders_created_per_start' : s,
            'orders_created_per_end' : e,
            'orders_created_per_time_today': ptc,
            'service_orders_created_per_day': ds,
            'service_orders_created_per_start' : ss,
            'current_day': current_day.date(),
            'current_time': current_time,
            'shift_start_time': start_time,
            'shift_end_time': end_time,
            'shift_start_datetime': complete_shift_start,
            'shift_end_datetime': complete_shift_end,
            'order_td_proccessing': c_order_processing,

            'service_order_td_proccessing': cs_order_processing,
            'service_order_td_completed': csc_order_completed,

            'order_processing': order_processing,
            'order_td_completed': c_order_completed,
            'order_completed': order_completed,
            'processing_graph': processing_graph, 
            'completed_graph': completed_graph,
            'shift_times': shift_times, 
            # 'qs': qs,
            # 'qs2': qs2,
            # 'cm': days_cur_month(),
            'timeline_month_1': timeline_month_1,
            'timeline_month_2': timeline_month_2,
            'timeline_month_3': timeline_month_3,
            'hours': get_hours(),
            'unread_messages': unread_messages,
            'companies_not_accepted': companies_not_accepted,
            'serviceorders_processing': myserviceorders,
            'serviceorders_processing_per_company': myserviceorders_per_company,
            'serviceorders_complated_per_company': myserviceorders_per_company_zrealizowane

        }

        return Response(output)
def mystats(request):
    output = {
        'order_processing': Order.objects.filter(user=request.user, order_status__name__icontains="W realizacji").count(),
        'order_completed': Order.objects.filter(user=request.user, order_status__name__icontains="Zrealizowane").count(),
        'unread_messages': Message.objects.filter(receipt=request.user, is_read=False).count(),
    }
    return JsonResponse(output)

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
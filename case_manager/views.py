from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import *
from .forms import * 

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
 


class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {})

class Logout(View):

    def get(self, request):

        logout(request)

        return redirect('login')

@method_decorator(login_required, name='dispatch')
class Home(View):

    def get(self, request):
        print(request.user)

        if request.user.systemuser.role == "attorney":
            user_role = 'attorney'
            system_user = Attorney.objects.get(user=request.user.systemuser)

        elif request.user.systemuser.role == "assistant":
            user_role = 'assistant'
            system_user = Assistant.objects.get(user=request.user.systemuser)

        else:
            user_role = 'admin'
            system_user = request.user.systemuser

        return render(request, 'home.html', {'sysuser':system_user, 'role':user_role}) 


def CaseContext(request, form_class=CaseForm(), return_query=True): 
    search = request.GET.get('search')
    if not search: search = ""

    context = {
        'name':'Case Registers',
        'form':form_class,
        'search':search, 
        'delete_active':False,
        'restore_active':False,
    }

    if not return_query:
        return context
    
    queryset = Case.objects.filter(Q(client__name__icontains=search) | Q(employer__name__icontains=search))
 
    context['items'] = queryset

    return context

class CreateCase(View):
    
    def get(self, request):
        # GET request: formularios vacíos
        case_form = CaseForm(prefix='case')
        client_form = ClientForm(prefix='client')
        employer_form = EmployerForm(prefix='employer')

        # Usar los forms opcionales SIN instancia (None explícito)
        insurance_form = InsuranceCarrierOptionalForm(prefix='insurance', instance=None)
        def_lawfirm_form = DefenseLawFirmOptionalForm(prefix='def_lawfirm', instance=None)
        def_attorney_form = DefenseAttorneyOptionalForm(prefix='def_attorney', instance=None)
        def_assistant_form = DefenseAssistantOptionalForm(prefix='def_assistant', instance=None)
        claim_admin_form = ClaimAdministratorOptionalForm(prefix='claim_admin', instance=None)
        claim_adjuster_form = ClaimAdjusterOptionalForm(prefix='claim_adjuster', instance=None)
 
        client_contact_formset = ClientContactFormSet(prefix='client_contacts')
        injury_formset = InjuryFormSet(prefix='injuries')
        claim_adjuster_contact_formset = ClaimAdjusterContactFormSet(prefix='claim_adjuster_contacts')
        defense_attorney_contact_formset = DefenseAttorneyContactFormSet(prefix='def_attorney_contacts')
        defense_assistant_contact_formset = DefenseAssistantContactFormSet(prefix='def_assistant_contacts')
    
        context = {
            'case_form': case_form,
            'client_form': client_form,
            'employer_form': employer_form,
            'insurance_form': insurance_form,
            'def_lawfirm_form': def_lawfirm_form,
            'def_attorney_form': def_attorney_form,
            'def_assistant_form': def_assistant_form,
            'claim_admin_form': claim_admin_form,
            'claim_adjuster_form': claim_adjuster_form,
            'injury_formset': injury_formset,
            'client_contact_formset': client_contact_formset,
            'claim_adjuster_contact_formset': claim_adjuster_contact_formset,
            'def_attorney_contact_formset': defense_attorney_contact_formset,
            'def_assistant_contact_formset': defense_assistant_contact_formset,
        }
        return render(request, 'create-case.html', context)

    def post(self, request):
        data = request.POST
        
        # Formulario principal del Case
        case_form = CaseForm(data, prefix='case')
        
        # Formsets anidados
        client_contact_formset = ClientContactFormSet(data, prefix='client_contacts')
        injury_formset = InjuryFormSet(data, prefix='injuries')
        
        # Forms OBLIGATORIOS
        client_form = ClientForm(data, prefix='client')
        employer_form = EmployerForm(data, prefix='employer')
        
        # ✅ CORREGIDO: Forms OPCIONALES con instance=None explícito
        insurance_form = InsuranceCarrierOptionalForm(data, prefix='insurance', instance=None)
        def_lawfirm_form = DefenseLawFirmOptionalForm(data, prefix='def_lawfirm', instance=None)
        def_attorney_form = DefenseAttorneyOptionalForm(data, prefix='def_attorney', instance=None)
        def_assistant_form = DefenseAssistantOptionalForm(data, prefix='def_assistant', instance=None)
        claim_admin_form = ClaimAdministratorOptionalForm(data, prefix='claim_admin', instance=None)
        claim_adjuster_form = ClaimAdjusterOptionalForm(data, prefix='claim_adjuster', instance=None)
        
        # Formsets para contactos
        claim_adjuster_contact_formset = ClaimAdjusterContactFormSet(
            data, prefix='claim_adjuster_contacts'
        )
        defense_attorney_contact_formset = DefenseAttorneyContactFormSet(
            data, prefix='def_attorney_contacts'
        )
        defense_assistant_contact_formset = DefenseAssistantContactFormSet(
            data, prefix='def_assistant_contacts'
        )
        
        # Validar TODOS los forms (obligatorios + opcionales + formsets)
        # Los opcionales se validan aunque estén vacíos
        all_forms_valid = all([
            case_form.is_valid(),
            client_form.is_valid(),
            employer_form.is_valid(),
            insurance_form.is_valid(),
            def_lawfirm_form.is_valid(),
            def_attorney_form.is_valid(),
            def_assistant_form.is_valid(),
            claim_admin_form.is_valid(),
            claim_adjuster_form.is_valid(),
            injury_formset.is_valid(),
            client_contact_formset.is_valid(),
            claim_adjuster_contact_formset.is_valid(),
            defense_attorney_contact_formset.is_valid(),
            defense_assistant_contact_formset.is_valid(),
        ])
        
        if all_forms_valid:
            # Guardar instancias OBLIGATORIAS
            client = client_form.save()
            employer = employer_form.save()
            
            # Guardar Case con las relaciones obligatorias
            case = case_form.save(commit=False)
            case.client = client
            case.employer = employer
            
            # ✅ CORREGIDO: Procesar forms OPCIONALES
            # El OptionalModelForm.save() debe retornar None si no hay datos
            insurance = insurance_form.save() if insurance_form.has_changed() else None
            def_lawfirm = def_lawfirm_form.save() if def_lawfirm_form.has_changed() else None
            def_attorney = def_attorney_form.save() if def_attorney_form.has_changed() else None
            def_assistant = def_assistant_form.save() if def_assistant_form.has_changed() else None
            claim_admin = claim_admin_form.save() if claim_admin_form.has_changed() else None
            claim_adjuster = claim_adjuster_form.save() if claim_adjuster_form.has_changed() else None
            
            # Asignar solo si no son None
            if insurance:
                case.insurance = insurance
            if def_lawfirm:
                case.def_lawfirm = def_lawfirm
            if def_attorney:
                case.def_attorney = def_attorney
            if def_assistant:
                case.def_assistant = def_assistant
            if claim_admin:
                case.claim_admin = claim_admin
            if claim_adjuster:
                case.claim_adjuster = claim_adjuster
            
            case.save()
            
            # Guardar formsets que dependen de Client (siempre)
            client_contact_formset.instance = client
            client_contact_formset.save()
            
            # Guardar injury_formset
            injury_formset.instance = case
            injury_formset.save()
            
            # ✅ CORREGIDO: Guardar formsets solo si las instancias existen
            if claim_adjuster:
                claim_adjuster_contact_formset.instance = claim_adjuster
                claim_adjuster_contact_formset.save()
            
            if def_attorney:
                defense_attorney_contact_formset.instance = def_attorney
                defense_attorney_contact_formset.save()
            
            if def_assistant:
                defense_assistant_contact_formset.instance = def_assistant
                defense_assistant_contact_formset.save()
            
            return redirect('case')
        
        # Si hay errores, devolver el template con los datos ingresados
        context = {
            'case_form': case_form,
            'client_form': client_form,
            'employer_form': employer_form,
            'insurance_form': insurance_form,
            'def_lawfirm_form': def_lawfirm_form,
            'def_attorney_form': def_attorney_form,
            'def_assistant_form': def_assistant_form,
            'claim_admin_form': claim_admin_form,
            'claim_adjuster_form': claim_adjuster_form,
            'injury_formset': injury_formset,
            'client_contact_formset': client_contact_formset,
            'claim_adjuster_contact_formset': claim_adjuster_contact_formset,
            'def_attorney_contact_formset': defense_attorney_contact_formset,
            'def_assistant_contact_formset': defense_assistant_contact_formset,
        }
        return render(request, 'create-case.html', context)

class UpdateCase(View):
    
    def get(self, request, pk):
        # Obtener la instancia principal del Case
        case = get_object_or_404(Case, id=pk)
        
        # Obtener las instancias relacionadas
        client = case.client
        employer = case.employer
        insurance = case.insurance
        def_lawfirm = case.def_lawfirm
        def_attorney = case.def_attorney
        def_assistant = case.def_assistant
        claim_admin = case.claim_admin
        claim_adjuster = case.claim_adjuster
        
        # Inicializar formularios con las instancias existentes
        case_form = CaseForm(prefix='case', instance=case)
        client_form = ClientForm(prefix='client', instance=client)
        employer_form = EmployerForm(prefix='employer', instance=employer)
        
        # Usar OptionalModelForm para los que pueden ser nulos
        insurance_form = InsuranceCarrierOptionalForm(prefix='insurance', instance=insurance) if insurance else InsuranceCarrierOptionalForm(prefix='insurance')
        def_lawfirm_form = DefenseLawFirmOptionalForm(prefix='def_lawfirm', instance=def_lawfirm) if def_lawfirm else DefenseLawFirmOptionalForm(prefix='def_lawfirm')
        def_attorney_form = DefenseAttorneyOptionalForm(prefix='def_attorney', instance=def_attorney) if def_attorney else DefenseAttorneyOptionalForm(prefix='def_attorney')
        def_assistant_form = DefenseAssistantOptionalForm(prefix='def_assistant', instance=def_assistant) if def_assistant else DefenseAssistantOptionalForm(prefix='def_assistant')
        claim_admin_form = ClaimAdministratorOptionalForm(prefix='claim_admin', instance=claim_admin) if claim_admin else ClaimAdministratorOptionalForm(prefix='claim_admin')
        claim_adjuster_form = ClaimAdjusterOptionalForm(prefix='claim_adjuster', instance=claim_adjuster) if claim_adjuster else ClaimAdjusterOptionalForm(prefix='claim_adjuster')
        
        # Inicializar formsets con las instancias relacionadas
        injury_formset = InjuryFormSet(prefix='injuries', instance=case, queryset=case.injuries.filter(active=True))
        client_contact_formset = ClientContactFormSet(prefix='client_contacts', instance=client, queryset=client.contacts.filter(active=True))
        claim_adjuster_contact_formset = ClaimAdjusterContactFormSet(prefix='claim_adjuster_contacts', instance=claim_adjuster, queryset=claim_adjuster.contacts.filter(active=True)) if claim_adjuster else ClaimAdjusterContactFormSet(prefix='claim_adjuster_contacts')
        defense_attorney_contact_formset = DefenseAttorneyContactFormSet(prefix='def_attorney_contacts', instance=def_attorney, queryset=def_attorney.contacts.filter(active=True)) if def_attorney else DefenseAttorneyContactFormSet(prefix='def_attorney_contacts')
        defense_assistant_contact_formset = DefenseAssistantContactFormSet(prefix='def_assistant_contacts', instance=def_assistant, queryset=def_assistant.contacts.filter(active=True)) if def_assistant else DefenseAssistantContactFormSet(prefix='def_assistant_contacts')
        
        context = {
            'case_form': case_form,
            'client_form': client_form,
            'employer_form': employer_form,
            'insurance_form': insurance_form,
            'def_lawfirm_form': def_lawfirm_form,
            'def_attorney_form': def_attorney_form,
            'def_assistant_form': def_assistant_form,
            'claim_admin_form': claim_admin_form,
            'claim_adjuster_form': claim_adjuster_form,

            'injury_formset':injury_formset,
            'client_contact_formset': client_contact_formset,
            'claim_adjuster_contact_formset': claim_adjuster_contact_formset,
            'def_attorney_contact_formset': defense_attorney_contact_formset,
            'def_assistant_contact_formset': defense_assistant_contact_formset,
        }
        return render(request, 'create-case.html', context)
    
    def post(self, request, pk):
        data = request.POST
        case = get_object_or_404(Case, id=pk)
        
        # Obtener las instancias relacionadas existentes
        client = case.client
        employer = case.employer
        insurance = case.insurance
        def_lawfirm = case.def_lawfirm
        def_attorney = case.def_attorney
        def_assistant = case.def_assistant
        claim_admin = case.claim_admin
        claim_adjuster = case.claim_adjuster
        
        # Formulario principal del Case con la instancia existente
        case_form = CaseForm(data, prefix='case', instance=case)
        
        # Forms OBLIGATORIOS
        client_form = ClientForm(data, prefix='client', instance=client)
        employer_form = EmployerForm(data, prefix='employer', instance=employer)
        
        # Forms OPCIONALES (actualizando las instancias existentes si las hay)
        insurance_form = InsuranceCarrierOptionalForm(data, prefix='insurance', instance=insurance) if insurance else InsuranceCarrierOptionalForm(data, prefix='insurance')
        def_lawfirm_form = DefenseLawFirmOptionalForm(data, prefix='def_lawfirm', instance=def_lawfirm) if def_lawfirm else DefenseLawFirmOptionalForm(data, prefix='def_lawfirm')
        def_attorney_form = DefenseAttorneyOptionalForm(data, prefix='def_attorney', instance=def_attorney) if def_attorney else DefenseAttorneyOptionalForm(data, prefix='def_attorney')
        def_assistant_form = DefenseAssistantOptionalForm(data, prefix='def_assistant', instance=def_assistant) if def_assistant else DefenseAssistantOptionalForm(data, prefix='def_assistant')
        claim_admin_form = ClaimAdministratorOptionalForm(data, prefix='claim_admin', instance=claim_admin) if claim_admin else ClaimAdministratorOptionalForm(data, prefix='claim_admin')
        claim_adjuster_form = ClaimAdjusterOptionalForm(data, prefix='claim_adjuster', instance=claim_adjuster) if claim_adjuster else ClaimAdjusterOptionalForm(data, prefix='claim_adjuster')
        
        # ✅ CORREGIDO: Formsets con instance desde el principio
        injury_formset = InjuryFormSet(data, prefix='injuries', instance=case, queryset=case.injuries.all())
        client_contact_formset = ClientContactFormSet(data, prefix='client_contacts', instance=client, queryset=client.contacts.all())
        
        # Formsets opcionales con instance solo si existen
        claim_adjuster_contact_formset = None
        defense_attorney_contact_formset = None
        defense_assistant_contact_formset = None
        
        if claim_adjuster:
            claim_adjuster_contact_formset = ClaimAdjusterContactFormSet(
                data, prefix='claim_adjuster_contacts', 
                instance=claim_adjuster, 
                queryset=claim_adjuster.contacts.all()
            )
        else:
            claim_adjuster_contact_formset = ClaimAdjusterContactFormSet(data, prefix='claim_adjuster_contacts')
        
        if def_attorney:
            defense_attorney_contact_formset = DefenseAttorneyContactFormSet(
                data, prefix='def_attorney_contacts', 
                instance=def_attorney, 
                queryset=def_attorney.contacts.all()
            )
        else:
            defense_attorney_contact_formset = DefenseAttorneyContactFormSet(data, prefix='def_attorney_contacts')
        
        if def_assistant:
            defense_assistant_contact_formset = DefenseAssistantContactFormSet(
                data, prefix='def_assistant_contacts', 
                instance=def_assistant, 
                queryset=def_assistant.contacts.all()
            )
        else:
            defense_assistant_contact_formset = DefenseAssistantContactFormSet(data, prefix='def_assistant_contacts')
        
        # Validar formularios obligatorios
        required_forms_valid = all([
            case_form.is_valid(),
            client_form.is_valid(),
            employer_form.is_valid(),
            client_contact_formset.is_valid(),
            injury_formset.is_valid(),  # ✅ Añadido aquí
        ])
        
        # Validar formsets opcionales
        optional_formsets_valid = True
        if claim_adjuster_contact_formset:
            optional_formsets_valid = optional_formsets_valid and claim_adjuster_contact_formset.is_valid()
        if defense_attorney_contact_formset:
            optional_formsets_valid = optional_formsets_valid and defense_attorney_contact_formset.is_valid()
        if defense_assistant_contact_formset:
            optional_formsets_valid = optional_formsets_valid and defense_assistant_contact_formset.is_valid()
        
        if required_forms_valid and optional_formsets_valid:
            # Guardar instancias obligatorias
            client = client_form.save()
            employer = employer_form.save()
            
            # Actualizar Case
            case = case_form.save(commit=False)
            case.client = client
            case.employer = employer
            
            # Procesar forms opcionales (guardar solo si tienen datos)
            new_insurance = insurance_form.save()
            new_def_lawfirm = def_lawfirm_form.save()
            new_def_attorney = def_attorney_form.save()
            new_def_assistant = def_assistant_form.save()
            new_claim_admin = claim_admin_form.save()
            new_claim_adjuster = claim_adjuster_form.save()
            
            # Actualizar relaciones del case
            case.insurance = new_insurance if new_insurance else None
            case.def_lawfirm = new_def_lawfirm if new_def_lawfirm else None
            case.def_attorney = new_def_attorney if new_def_attorney else None
            case.def_assistant = new_def_assistant if new_def_assistant else None
            case.claim_admin = new_claim_admin if new_claim_admin else None
            case.claim_adjuster = new_claim_adjuster if new_claim_adjuster else None
            
            case.save()
            
            # ✅ CORREGIDO: Guardar injury_formset (ya tiene instance=case)
            injury_formset.save()
            
            # Guardar client_contact_formset
            client_contact_formset.save()
            
            # Guardar formsets opcionales
            if new_claim_adjuster:
                claim_adjuster_contact_formset.instance = new_claim_adjuster
                claim_adjuster_contact_formset.save()
            elif claim_adjuster and not new_claim_adjuster:
                # Opcional: eliminar contactos del claim_adjuster eliminado
                ClaimAdjusterContact.objects.filter(claim_adjuster=claim_adjuster).delete()
            
            if new_def_attorney:
                defense_attorney_contact_formset.instance = new_def_attorney
                defense_attorney_contact_formset.save()
            elif def_attorney and not new_def_attorney:
                DefenseAttorneyContact.objects.filter(defense_attorney=def_attorney).delete()
            
            if new_def_assistant:
                defense_assistant_contact_formset.instance = new_def_assistant
                defense_assistant_contact_formset.save()
            elif def_assistant and not new_def_assistant:
                DefenseAssistantContact.objects.filter(defense_assistant=def_assistant).delete()
            
            return redirect('case')
        
        # Si hay errores, devolver el template con los datos ingresados
        context = {
            'case_form': case_form,
            'client_form': client_form,
            'employer_form': employer_form,
            'insurance_form': insurance_form,
            'def_lawfirm_form': def_lawfirm_form,
            'def_attorney_form': def_attorney_form,
            'def_assistant_form': def_assistant_form,
            'claim_admin_form': claim_admin_form,
            'claim_adjuster_form': claim_adjuster_form,
            'injury_formset': injury_formset,
            'client_contact_formset': client_contact_formset,
            'claim_adjuster_contact_formset': claim_adjuster_contact_formset,
            'def_attorney_contact_formset': defense_attorney_contact_formset,
            'def_assistant_contact_formset': defense_assistant_contact_formset,
        }
        return render(request, 'create-case.html', context)
    

class DetailCase(DetailView):
    model = Case
    template_name = 'case-detail.html'
    context_object_name = 'case'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_injuries'] = self.object.injuries.filter(active=True)
        return context  

class DeleteCase(View):
    def post(self, request, pk):

        case = Case.objects.get(id=pk)

        case.soft_delete()
        case.save()

        for injury in case.injuries.all():
            injury.soft_delete()
            injury.save()

class RestoreCase(View):
    def post(self, request, pk):
        case = Case.objects.get(id=pk)

        case.restore()
        case.save()

        for injury in case.injuries.all():
            injury.restore()
            injury.save()


class ListCases(ListView):
    model = Case
    template_name = 'list-cases.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search') 
        
        added_context = CaseContext(self.request)
        context['detail_url'] = True
        context['list_url'] = 'case'
        return context | added_context 


@method_decorator(login_required, name='dispatch')    
class DeleteCase(View):
    def post(self, request, pk):
        case = CaseStatus.objects.get(id=pk) 
        case.soft_delete()

        return redirect('case')
# MODELS CRUD

def CaseStatusContext(request, form_class=CaseStatusForm(), return_query=True): 
    search = request.GET.get('search')
    if not search: search = ""

    context = {
        'name':'Case Status',
        'form':form_class,
        'list_url':'status',
        'search':search,
        'create_active':False,
        'update_active':False,
        'delete_active':False,
        'restore_active':False,
    }

    if not return_query:
        return context
    
    queryset = CaseStatus.objects.filter(Q(name__icontains=search) | Q(id__icontains=search))
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListCaseStatus(ListView):
    model = CaseStatus
    template_name = 'show/show-status.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search') 
        
        added_context = CaseStatusContext(self.request)
        return context | added_context 

@method_decorator(login_required, name='dispatch')    
class CreateStatus(CreateView):
    model = CaseStatus
    form_class = CaseStatusForm
    success_url = reverse_lazy('status')
    template_name = 'show/show-status.html'
    
    def form_invalid(self, form):  
        search = self.request.GET.get('search')

        context = CaseStatusContext(self.request, form) 
        context['create_active'] = True
        
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
class UpdateStatus(UpdateView):
    model = CaseStatus
    form_class = CaseStatusForm
    success_url = reverse_lazy('status')
    template_name = 'show/show-status.html' 
    
    def form_invalid(self, form): 
        search = self.request.GET.get('search')

        context = CaseStatusContext(self.request, form) 
        context['update_active'] = True
        context['temp_name'] = self.get_object().name
        
        return self.render_to_response(context) 

@method_decorator(login_required, name='dispatch')    
class DeleteStatus(View):
    def post(self, request, pk):
        status = CaseStatus.objects.get(id=pk) 
        status.soft_delete()

        return redirect('status')

@method_decorator(login_required, name='dispatch')
class RestoreStatus(View):
    def post(self, request, pk):
        status = CaseStatus.objects.get(id=pk)
        status.restore()

        return redirect('status')

# Contexto para Attorney
def AttorneyContext(request, form_class=SystemAttorneyForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Attorney',
        'form': form_class,
        'list_url':'attorney',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = Attorney.objects.filter(
        Q(name__icontains=search) | Q(id__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListAttorney(ListView):
    model = Attorney
    template_name = 'show/show-attorney.html'  # Nueva plantilla
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = AttorneyContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')    
class CreateAttorney(CreateView):
    model = Attorney
    form_class = SystemAttorneyForm
    success_url = reverse_lazy('attorney')  # Cambiar URL name
    template_name = 'show/show-attorney.html'
    
    def form_invalid(self, form):  
        search = self.request.GET.get('search', '')
        context = AttorneyContext(self.request, form) 
        context['create_active'] = True
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
class UpdateAttorney(UpdateView):
    model = Attorney
    form_class = SystemAttorneyUpdateForm
    success_url = reverse_lazy('attorney')
    template_name = 'show/show-attorney.html'
    
    def form_invalid(self, form): 
        search = self.request.GET.get('search', '')
        context = AttorneyContext(self.request, form) 
        context['update_active'] = True
        context['temp_name'] = self.get_object().name
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')    
class DeleteAttorney(View):
    def post(self, request, pk):
        attorney = Attorney.objects.get(id=pk) 
        attorney.soft_delete()
        return redirect('attorney')

@method_decorator(login_required, name='dispatch')
class RestoreAttorney(View):
    def post(self, request, pk):
        attorney = Attorney.objects.get(id=pk)
        attorney.restore()
        return redirect('attorney')
    

# Contexto para Assistant
def AssistantContext(request, form_class=SystemAssistantForm(), return_query=True):
    search = request.GET.get('search') 
    if not search: 
        search = ""

    context = {
        'name': 'Assistant',
        'form': form_class,
        'list_url':'assistant',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = Assistant.objects.filter(
        Q(name__icontains=search) | Q(id__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListAssistant(ListView):
    model = Assistant
    template_name = 'show/show-assistant.html'  # Template específico
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = AssistantContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateAssistant(CreateView):
    model = Assistant
    form_class = SystemAssistantForm
    success_url = reverse_lazy('assistant')  # Asumiendo que usas 'assistant' como nombre de URL
    template_name = 'show/show-assistant.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = AssistantContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Assistant creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateAssistant(UpdateView):
    model = Assistant
    form_class = SystemAssistantUpdateForm
    success_url = reverse_lazy('assistant')
    template_name = 'show/show-assistant.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = AssistantContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Assistant modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteAssistant(View):
    def post(self, request, pk):
        assistant = Assistant.objects.get(id=pk)
        assistant.soft_delete()
        return redirect('assistant')

@method_decorator(login_required, name='dispatch')
class RestoreAssistant(View):
    def post(self, request, pk):
        assistant = Assistant.objects.get(id=pk)
        assistant.restore()
        return redirect('assistant')
    
def EmployerContext(request, form_class=EmployerForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Employer',
        'form': form_class,
        'list_url':'employer',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = Employer.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search) |
        Q(address__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListEmployer(ListView):
    model = Employer
    template_name = 'show/show-employer.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = EmployerContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateEmployer(CreateView):
    model = Employer
    form_class = EmployerForm
    success_url = reverse_lazy('employer')
    template_name = 'show/show-employer.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = EmployerContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
class UpdateEmployer(UpdateView):
    model = Employer
    form_class = EmployerForm
    success_url = reverse_lazy('employer')
    template_name = 'show/show-employer.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = EmployerContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
class DeleteEmployer(View):
    def post(self, request, pk):
        employer = Employer.objects.get(id=pk)
        employer.soft_delete()
        return redirect('employer')

@method_decorator(login_required, name='dispatch')
class RestoreEmployer(View):
    def post(self, request, pk):
        employer = Employer.objects.get(id=pk)
        employer.restore()
        return redirect('employer')
    
def InsuranceCarrierContext(request, form_class=InsuranceCarrierForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Insurance Carrier',
        'form': form_class,
        'list_url':'insurance-carrier',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = InsuranceCarrier.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search) |
        Q(address__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListInsuranceCarrier(ListView):
    model = InsuranceCarrier
    template_name = 'show/show-insurance-carrier.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = InsuranceCarrierContext(self.request)
        return context | added_context


@method_decorator(login_required, name='dispatch')
class CreateInsuranceCarrier(CreateView):
    model = InsuranceCarrier
    form_class = InsuranceCarrierForm
    success_url = reverse_lazy('insurance-carrier')
    template_name = 'show/show-insurance-carrier.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = InsuranceCarrierContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Insurance Carrier creado exitosamente')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UpdateInsuranceCarrier(UpdateView):
    model = InsuranceCarrier
    form_class = InsuranceCarrierForm
    success_url = reverse_lazy('insurance-carrier')
    template_name = 'show/show-insurance-carrier.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = InsuranceCarrierContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Insurance Carrier modificado exitosamente')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class DeleteInsuranceCarrier(View):
    def post(self, request, pk):
        insurance_carrier = InsuranceCarrier.objects.get(id=pk)
        insurance_carrier.soft_delete()
        messages.success(request, 'Insurance Carrier eliminado exitosamente')
        return redirect('insurance-carrier')


@method_decorator(login_required, name='dispatch')
class RestoreInsuranceCarrier(View):
    def post(self, request, pk):
        insurance_carrier = InsuranceCarrier.objects.get(id=pk)
        insurance_carrier.restore()
        messages.success(request, 'Insurance Carrier restaurado exitosamente')
        return redirect('insurance-carrier')
    


def ClaimAdministratorContext(request, form_class=ClaimAdministratorForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Claim Administrator',
        'form': form_class,
        'list_url':'claim-administrator',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = ClaimAdministrator.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search) |
        Q(address__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListClaimAdministrator(ListView):
    model = ClaimAdministrator
    template_name = 'show/show-claim-administrator.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = ClaimAdministratorContext(self.request)
        return context | added_context


@method_decorator(login_required, name='dispatch')
class CreateClaimAdministrator(CreateView):
    model = ClaimAdministrator
    form_class = ClaimAdministratorForm
    success_url = reverse_lazy('claim-administrator')
    template_name = 'show/show-claim-administrator.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = ClaimAdministratorContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Claim Administrator creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateClaimAdministrator(UpdateView):
    model = ClaimAdministrator
    form_class = ClaimAdministratorForm
    success_url = reverse_lazy('claim-administrator')
    template_name = 'show/show-claim-administrator.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = ClaimAdministratorContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Claim Administrator modificado exitosamente')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class DeleteClaimAdministrator(View):
    def post(self, request, pk):
        claim_admin = ClaimAdministrator.objects.get(id=pk)
        claim_admin.soft_delete()
        messages.success(request, 'Claim Administrator eliminado exitosamente')
        return redirect('claim-administrator')


@method_decorator(login_required, name='dispatch')
class RestoreClaimAdministrator(View):
    def post(self, request, pk):
        claim_admin = ClaimAdministrator.objects.get(id=pk)
        claim_admin.restore()
        messages.success(request, 'Claim Administrator restaurado exitosamente')
        return redirect('claim-administrator')
    

# DEFENSE LAW FIRM
def DefenseLawFirmContext(request, form_class=DefenseLawFirmForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Defense Law Firm',
        'form': form_class,
        'list_url':'defense-law-firm',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = DefenseLawFirm.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search) |
        Q(address__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListDefenseLawFirm(ListView):
    model = DefenseLawFirm
    template_name = 'show/show-defense-law-firm.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = DefenseLawFirmContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateDefenseLawFirm(CreateView):
    model = DefenseLawFirm
    form_class = DefenseLawFirmForm
    success_url = reverse_lazy('defense-law-firm')
    template_name = 'show/show-defense-law-firm.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = DefenseLawFirmContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Defense Law Firm creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateDefenseLawFirm(UpdateView):
    model = DefenseLawFirm
    form_class = DefenseLawFirmForm
    success_url = reverse_lazy('defense-law-firm')
    template_name = 'show/show-defense-law-firm.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = DefenseLawFirmContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Defense Law Firm modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteDefenseLawFirm(View):
    def post(self, request, pk):
        law_firm = DefenseLawFirm.objects.get(id=pk)
        law_firm.soft_delete()
        messages.success(request, 'Defense Law Firm eliminado exitosamente')
        return redirect('defense-law-firm')

@method_decorator(login_required, name='dispatch')
class RestoreDefenseLawFirm(View):
    def post(self, request, pk):
        law_firm = DefenseLawFirm.objects.get(id=pk)
        law_firm.restore()
        messages.success(request, 'Defense Law Firm restaurado exitosamente')
        return redirect('defense-law-firm')
    

def ClientContext(request, form_class=ClientForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Client',
        'form': form_class,
        'list_url':'client',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = Client.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search) |
        Q(address__icontains=search) |
        Q(ssn__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListClient(ListView):
    model = Client
    template_name = 'show/show-client.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = ClientContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateClient(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client')
    template_name = 'show/show-client.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = ClientContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Client creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateClient(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client')
    template_name = 'show/show-client.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = ClientContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Client modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteClient(View):
    def post(self, request, pk):
        client = Client.objects.get(id=pk)
        client.soft_delete()
        messages.success(request, 'Client eliminado exitosamente')
        return redirect('client')

@method_decorator(login_required, name='dispatch')
class RestoreClient(View):
    def post(self, request, pk):
        client = Client.objects.get(id=pk)
        client.restore()
        messages.success(request, 'Client restaurado exitosamente')
        return redirect('client')

def ClaimAdjusterContext(request, form_class=ClaimAdjusterForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Claim Adjuster',
        'form': form_class,
        'list_url':'claim-adjuster',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = ClaimAdjuster.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListClaimAdjuster(ListView):
    model = ClaimAdjuster
    template_name = 'show/show-claim-adjuster.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = ClaimAdjusterContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateClaimAdjuster(CreateView):
    model = ClaimAdjuster
    form_class = ClaimAdjusterForm
    success_url = reverse_lazy('claim-adjuster')
    template_name = 'show/show-claim-adjuster.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = ClaimAdjusterContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Claim Adjuster creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateClaimAdjuster(UpdateView):
    model = ClaimAdjuster
    form_class = ClaimAdjusterForm
    success_url = reverse_lazy('claim-adjuster')
    template_name = 'show/show-claim-adjuster.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = ClaimAdjusterContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Claim Adjuster modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteClaimAdjuster(View):
    def post(self, request, pk):
        claim_adjuster = ClaimAdjuster.objects.get(id=pk)
        claim_adjuster.soft_delete()
        messages.success(request, 'Claim Adjuster eliminado exitosamente')
        return redirect('claim-adjuster')

@method_decorator(login_required, name='dispatch')
class RestoreClaimAdjuster(View):
    def post(self, request, pk):
        claim_adjuster = ClaimAdjuster.objects.get(id=pk)
        claim_adjuster.restore()
        messages.success(request, 'Claim Adjuster restaurado exitosamente')
        return redirect('claim-adjuster')
    


def DefenseAttorneyContext(request, form_class=DefenseAttorneyForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Defense Attorney',
        'form': form_class,
        'list_url':'defense-attorney',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = DefenseAttorney.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListDefenseAttorney(ListView):
    model = DefenseAttorney
    template_name = 'show/show-defense-attorney.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = DefenseAttorneyContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateDefenseAttorney(CreateView):
    model = DefenseAttorney
    form_class = DefenseAttorneyForm
    success_url = reverse_lazy('defense-attorney')
    template_name = 'show/show-defense-attorney.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = DefenseAttorneyContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Defense Attorney creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateDefenseAttorney(UpdateView):
    model = DefenseAttorney
    form_class = DefenseAttorneyForm
    success_url = reverse_lazy('defense-attorney')
    template_name = 'show/show-defense-attorney.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = DefenseAttorneyContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Defense Attorney modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteDefenseAttorney(View):
    def post(self, request, pk):
        defense_attorney = DefenseAttorney.objects.get(id=pk)
        defense_attorney.soft_delete()
        messages.success(request, 'Defense Attorney eliminado exitosamente')
        return redirect('defense-attorney')

@method_decorator(login_required, name='dispatch')
class RestoreDefenseAttorney(View):
    def post(self, request, pk):
        defense_attorney = DefenseAttorney.objects.get(id=pk)
        defense_attorney.restore()
        messages.success(request, 'Defense Attorney restaurado exitosamente')
        return redirect('defense-attorney')


def DefenseAssistantContext(request, form_class=DefenseAssistantForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Defense Assistant',
        'form': form_class,
        'list_url':'defense-assistant',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = DefenseAssistant.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListDefenseAssistant(ListView):
    model = DefenseAssistant
    template_name = 'show/show-defense-assistant.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = DefenseAssistantContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateDefenseAssistant(CreateView):
    model = DefenseAssistant
    form_class = DefenseAssistantForm
    success_url = reverse_lazy('defense-assistant')
    template_name = 'show/show-defense-assistant.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = DefenseAssistantContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Defense Assistant creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateDefenseAssistant(UpdateView):
    model = DefenseAssistant
    form_class = DefenseAssistantForm
    success_url = reverse_lazy('defense-assistant')
    template_name = 'show/show-defense-assistant.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = DefenseAssistantContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Defense Assistant modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteDefenseAssistant(View):
    def post(self, request, pk):
        defense_assistant = DefenseAssistant.objects.get(id=pk)
        defense_assistant.soft_delete()
        messages.success(request, 'Defense Assistant eliminado exitosamente')
        return redirect('defense-assistant')

@method_decorator(login_required, name='dispatch')
class RestoreDefenseAssistant(View):
    def post(self, request, pk):
        defense_assistant = DefenseAssistant.objects.get(id=pk)
        defense_assistant.restore()
        messages.success(request, 'Defense Assistant restaurado exitosamente')
        return redirect('defense-assistant')
    

# InjuryType Context
def InjuryTypeContext(request, form_class=InjuryTypeForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Injury Type',
        'form': form_class,
        'list_url':'injury-type',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
        
    
    queryset = InjuryType.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListInjuryType(ListView):
    model = InjuryType
    template_name = 'show/show-injury-type.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = InjuryTypeContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateInjuryType(CreateView):
    model = InjuryType
    form_class = InjuryTypeForm
    success_url = reverse_lazy('injury-type')
    template_name = 'show/show-injury-type.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = InjuryTypeContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Injury Type creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateInjuryType(UpdateView):
    model = InjuryType
    form_class = InjuryTypeForm
    success_url = reverse_lazy('injury-type')
    template_name = 'show/show-injury-type.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = InjuryTypeContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Injury Type modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteInjuryType(View):
    def post(self, request, pk):
        obj = InjuryType.objects.get(id=pk)
        obj.soft_delete()
        messages.success(request, 'Injury Type eliminado exitosamente')
        return redirect('injury-type')

@method_decorator(login_required, name='dispatch')
class RestoreInjuryType(View):
    def post(self, request, pk):
        obj = InjuryType.objects.get(id=pk)
        obj.restore()
        messages.success(request, 'Injury Type restaurado exitosamente')
        return redirect('injury-type')


# BodyPart Context
def BodyPartContext(request, form_class=BodyPartForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Body Part',
        'form': form_class,
        'list_url':'body-part',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    queryset = BodyPart.objects.filter(
        Q(name__icontains=search) | 
        Q(id__icontains=search)
    )

    if request.user.systemuser.role != "admin":
        queryset = queryset.filter(active=True)

    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListBodyPart(ListView):
    model = BodyPart
    template_name = 'show/show-body-part.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = BodyPartContext(self.request)
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateBodyPart(CreateView):
    model = BodyPart
    form_class = BodyPartForm
    success_url = reverse_lazy('body-part')
    template_name = 'show/show-body-part.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = BodyPartContext(self.request, form)
        context['create_active'] = True
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Body Part creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateBodyPart(UpdateView):
    model = BodyPart
    form_class = BodyPartForm
    success_url = reverse_lazy('body-part')
    template_name = 'show/show-body-part.html'
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = BodyPartContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Body Part modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteBodyPart(View):
    def post(self, request, pk):
        obj = BodyPart.objects.get(id=pk)
        obj.soft_delete()
        messages.success(request, 'Body Part eliminado exitosamente')
        return redirect('body-part')

@method_decorator(login_required, name='dispatch')
class RestoreBodyPart(View):
    def post(self, request, pk):
        obj = BodyPart.objects.get(id=pk)
        obj.restore()
        messages.success(request, 'Body Part restaurado exitosamente')
        return redirect('body-part')

# Injury Context (especial)
def InjuryContext(request, form_class=InjuryForm(), return_query=True):
    search = request.GET.get('search')
    if not search: 
        search = ""

    context = {
        'name': 'Injury',
        'form': form_class,
        'list_url':'injury',
        'search': search,
        'create_active': False,
        'update_active': False,
        'delete_active': False,
        'restore_active': False,
    }

    if not return_query:
        return context
    
    # Búsqueda en campos relacionados
    queryset = Injury.objects.filter(
        Q(id__icontains=search) |
        Q(date__icontains=search) |
        Q(part__name__icontains=search) |
        Q(type__name__icontains=search) |
        Q(case__id__icontains=search)
    )
    context['items'] = queryset

    return context

@method_decorator(login_required, name='dispatch')
class ListInjury(ListView):
    model = Injury
    template_name = 'show/show-injury.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '')
        
        added_context = InjuryContext(self.request)
        
        # Agregar opciones para selects en form
        added_context['body_parts'] = BodyPart.objects.filter(active=True)
        added_context['injury_types'] = InjuryType.objects.filter(active=True)
        
        return context | added_context

@method_decorator(login_required, name='dispatch')
class CreateInjury(CreateView):
    model = Injury
    form_class = InjuryForm
    success_url = reverse_lazy('injury')
    template_name = 'show/show-injury.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['body_parts'] = BodyPart.objects.filter(active=True)
        context['injury_types'] = InjuryType.objects.filter(active=True)
        return context
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = InjuryContext(self.request, form)
        context['create_active'] = True
        context['body_parts'] = BodyPart.objects.filter(active=True)
        context['injury_types'] = InjuryType.objects.filter(active=True)
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Injury creado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateInjury(UpdateView):
    model = Injury
    form_class = InjuryForm
    success_url = reverse_lazy('injury')
    template_name = 'show/show-injury.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['body_parts'] = BodyPart.objects.filter(active=True)
        context['injury_types'] = InjuryType.objects.filter(active=True)
        return context
    
    def form_invalid(self, form):
        search = self.request.GET.get('search', '')
        context = InjuryContext(self.request, form)
        context['update_active'] = True
        context['object_name'] = self.get_object().name  # Usa el método name()
        context['body_parts'] = BodyPart.objects.filter(active=True)
        context['injury_types'] = InjuryType.objects.filter(active=True)
        return self.render_to_response(context)
    
    def form_valid(self, form):
        messages.success(self.request, 'Injury modificado exitosamente')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteInjury(View):
    def post(self, request, pk):
        obj = Injury.objects.get(id=pk)
        obj.soft_delete()
        messages.success(request, 'Injury eliminado exitosamente')
        return redirect('injury')

@method_decorator(login_required, name='dispatch')
class RestoreInjury(View):
    def post(self, request, pk):
        obj = Injury.objects.get(id=pk)
        obj.restore()
        messages.success(request, 'Injury restaurado exitosamente')
        return redirect('injury')
    
 
from django.utils import timezone
from datetime import datetime, timedelta 
import pandas as pd

class Report(View):

    def get(self, request):
        data = request.GET
        
        # Obtener fechas del request, con valores por defecto
        start_date_str = data.get('start_date', '')
        end_date_str = data.get('end_date', '')
        
        # Valores por defecto: una semana atrás y hoy
        today = timezone.now().date()
        default_start = today - timedelta(days=7)
        
        # Procesar start_date
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                start_date = default_start
        else:
            start_date = default_start
        
        # Procesar end_date
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                end_date = today
        else:
            end_date = today
         
        # Aplicar los mismos filtros que usas para mostrar
        cases = Case.objects.filter(
            updated_at__date__gte=start_date,
            updated_at__date__lte=end_date
        ).select_related('client', 'attorney', 'assistant', 'status')
        
        # Verificar si hay que exportar
        if data.get('export') == '1':  # El value="1" se captura aquí
            return self.export_to_excel(cases, start_date, end_date)
        
        # Si no, mostrar la vista normal
        cases = cases.order_by('-updated_at')
        
        context = {
            'items': cases,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }
        
        return render(request, 'report.html', context)
    
    def export_to_excel(self, cases, start_date, end_date):
        """Exporta los casos a un archivo Excel"""
        
        data = []
        for case in cases:
            # Convertir fechas timezone-aware a naive
            updated_at_naive = case.updated_at.replace(tzinfo=None) if case.updated_at else None
            created_at_naive = case.created_at.replace(tzinfo=None) if case.created_at else None
            settlement_date_naive = case.settlement_date  # DateField ya es naive
            adj_date_naive = case.adj_date  # DateField ya es naive
            date_assigned_naive = case.date_assigned if hasattr(case, 'date_assigned') else None  # DateField
            
            data.append({
                'Client Name': case.client.name,
                'Date Assigned': date_assigned_naive,
                'Attorney': case.attorney.name if case.attorney else '',
                'Assistant': case.assistant.name if case.assistant else '',
                'Case Status': case.status.name if case.status else '',
                'Details Registered': 'Yes' if case.claim_num else 'No',
                'ADJ Filed': 'Yes' if case.adj_date else 'No',
                'ADJ Number': case.adj_num or '',
                'Claim Number': case.claim_num or '',
                'Claim Status': case.get_claim_status_display() or '',
                'Settled': 'Yes' if case.settlement_date else 'No',
                'Settlement Date': settlement_date_naive,
                'Active': 'Yes' if case.active else 'No',
                'Source': getattr(case, 'source', ''), 
            })
        
        df = pd.DataFrame(data)
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        filename = f'cases_report_{start_date}_to_{end_date}.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Cases Report', startrow=1)
            
            # Obtener el workbook y worksheet
            workbook = writer.book
            worksheet = writer.sheets['Cases Report']
            
            # Estilo para el encabezado
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            
            header_font = Font(bold=True, color='FFFFFF', size=11)
            header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
            header_alignment = Alignment(horizontal='center', vertical='center')
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            # Aplicar estilo a los encabezados (fila 2 porque startrow=1)
            for col in range(1, len(df.columns) + 1):
                cell = worksheet.cell(row=2, column=col)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = thin_border
            
            # Autoajustar ancho de columnas
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Congelar la fila del encabezado
            worksheet.freeze_panes = 'A3'
        
        return response
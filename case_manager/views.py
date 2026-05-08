from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import *

from django.db.models import Q
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from itertools import zip_longest

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    return render(request, 'base.html', {}) 

class Login(View):

    def get(self, request):

        name = "Comley Fresch"
        context = {"name":name}

        return render(request, 'login.html', context)
    
    def post(self, request):

        data = request.POST

        username = data.get("username")
        password = data.get("password") 

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.GET.get('next')  

            if next_url:
                return redirect(next_url)

            return redirect('home')  # fallback

        else:
            context = {
                "username":username,
                "error_msg":"* Invalid username or password",
            }
            return render(request, 'login.html', context)

@method_decorator(login_required, name='dispatch')   
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class CreateCase(View):
 
    def get(self, request): 

        if request.user.systemuser.role == "attorney":
            user_role = 'attorney'
            system_user = Attorney.objects.get(user=request.user.systemuser)

        elif request.user.systemuser.role == "assistant":
            user_role = 'assistant'
            system_user = Assistant.objects.get(user=request.user.systemuser)

        else:
            user_role = None
            system_user = None

        context = {
            'system_user':system_user,
            'user_role':user_role,
            'case_statuses':CaseStatus.objects.filter(visible=True),
            'attorneys':Attorney.objects.filter(visible=True),
            'assistants':Assistant.objects.filter(visible=True),
            'body_parts':BodyPart.objects.filter(visible=True),
            'injury_types':InjuryType.objects.filter(visible=True),

            'clients':Client.objects.filter(visible=True), 
            'employers':Employer.objects.filter(visible=True),
            'ins_carriers':InsuranceCarrier.objects.filter(visible=True),

            'def_lawfirms':DefenseLawFirm.objects.filter(visible=True),
            'def_atts':DefenseAttorney.objects.filter(visible=True),
            'def_assts':DefenseAssistant.objects.filter(visible=True),

            'claim_admins':ClaimAdministrator.objects.filter(visible=True),
            'claim_adjs':ClaimAdjuster.objects.filter(visible=True),
        }

        return render(request, 'create-case.html', context)
    
    def post(self, request):
        data = request.POST

        try:
            with transaction.atomic():
                print("comienza")

                # =====================
                # CLIENTE (Tom Select)
                # =====================
                client_value = data.get('client')  # Puede ser ID o nombre
                
                if client_value and client_value.isdigit():
                    # Es un ID existente
                    client = Client.objects.get(id=int(client_value))
                elif client_value:
                    # Es un nuevo cliente (nombre)
                    client = Client.objects.create(
                        name=client_value,
                        address=data.get('client-address', ''),
                        ssn=data.get('client-ssn', ''),
                        birth_date=data.get('client-birth') or None,
                    )
                else:
                    # No hay cliente
                    client = None

                # =====================
                # CONTACTOS CLIENTE
                # =====================
                if client:
                    types = data.getlist('client-contact-type')
                    values = data.getlist('client-contact-value')
                    notes = data.getlist('client-contact-notes')

                    for t, v, n in zip(types, values, notes):
                        if v and v.strip():  # evita vacíos
                            Contact.objects.create(
                                contact_type=t,
                                value=v.strip(),
                                notes=n,
                                content_object=client
                            )

                # =====================
                # CASE STATUS 
                # =====================
                case_status_id = data.get('case-status')
                case_status = CaseStatus.objects.get(id=case_status_id)

                # =====================
                # ATTORNEY 
                # =====================
                attorney_id = data.get('attorney-id')
                attorney = Attorney.objects.get(id=attorney_id)

                # =====================
                # ASSISTANT 
                # =====================
                assistant_id = data.get('assistant-id')
                assistant = Assistant.objects.get(id=assistant_id)

                # =====================
                # EMPLOYER (Tom Select)
                # =====================
                employer_value = data.get('employer')
                
                if employer_value and employer_value.isdigit():
                    employer = Employer.objects.get(id=int(employer_value))
                elif employer_value:
                    employer = Employer.objects.create(
                        name=employer_value,
                        address=data.get('employer-address', '')
                    )
                else:
                    employer = None

                # =====================
                # INSURANCE CARRIER (Tom Select)
                # =====================
                ins_carrier_value = data.get('ins-carrier')
                print(ins_carrier_value)
                
                if ins_carrier_value and ins_carrier_value.isdigit():
                    ins_carrier = InsuranceCarrier.objects.get(id=int(ins_carrier_value))
                elif ins_carrier_value:
                    ins_carrier = InsuranceCarrier.objects.create(
                        name=ins_carrier_value,
                        address=data.get('ins-carrier-address', '')
                    )
                else:
                    ins_carrier = None

                # =====================
                # CLAIM ADMIN (Tom Select)
                # =====================
                claim_admin_value = data.get('claim-admin')
                
                if claim_admin_value and claim_admin_value.isdigit():
                    claim_admin = ClaimAdministrator.objects.get(id=int(claim_admin_value))
                elif claim_admin_value:
                    claim_admin = ClaimAdministrator.objects.create(
                        name=claim_admin_value,
                        address=data.get('claim-admin-address', '')
                    )
                else:
                    claim_admin = None

                # =====================
                # CLAIM ADJUSTER (Tom Select)
                # =====================
                claim_adj_value = data.get('claim-adj')
                
                if claim_adj_value and claim_adj_value.isdigit():
                    claim_adj = ClaimAdjuster.objects.get(id=int(claim_adj_value))
                elif claim_adj_value:
                    claim_adj = ClaimAdjuster.objects.create(
                        name=claim_adj_value
                    )
                else:
                    claim_adj = None

                # =====================
                # CONTACTS CLAIM ADJUSTER
                # =====================
                if claim_adj:
                    types = data.getlist('claim-adj-contact-type')
                    values = data.getlist('claim-adj-contact-value')
                    notes = data.getlist('claim-adj-contact-notes')

                    for t, v, n in zip(types, values, notes):
                        if v and v.strip():
                            Contact.objects.create(
                                contact_type=t,
                                value=v.strip(),
                                notes=n,
                                content_object=claim_adj
                            )

                # =====================
                # LAW FIRM / DEFENSE (Tom Select)
                # =====================
                def_law_firm_value = data.get('def-lawfirm')
                
                if def_law_firm_value and def_law_firm_value.isdigit():
                    def_law_firm = DefenseLawFirm.objects.get(id=int(def_law_firm_value))
                elif def_law_firm_value:
                    def_law_firm = DefenseLawFirm.objects.create(
                        name=def_law_firm_value,
                        address=data.get('law-firm-address', '')
                    )
                else:
                    def_law_firm = None

                # =====================
                # DEFENSE ATTORNEY (Tom Select)
                # =====================
                def_att_value = data.get('def-att')
                
                if def_att_value and def_att_value.isdigit():
                    def_att = DefenseAttorney.objects.get(id=int(def_att_value))
                elif def_att_value:
                    def_att = DefenseAttorney.objects.create(
                        name=def_att_value
                    )
                else:
                    def_att = None

                # =====================
                # DEFENSE ASSISTANT (Tom Select)
                # =====================
                def_asst_value = data.get('def-asst')
                
                if def_asst_value and def_asst_value.isdigit():
                    def_asst = DefenseAssistant.objects.get(id=int(def_asst_value))
                elif def_asst_value:
                    def_asst = DefenseAssistant.objects.create(
                        name=def_asst_value
                    )
                else:
                    def_asst = None

                # =====================
                # CONTACTS DEFENSE ASSISTANT
                # =====================
                if def_asst:
                    types = data.getlist('def-asst-contact-type')
                    values = data.getlist('def-asst-contact-value')
                    notes = data.getlist('def-asst-contact-notes')

                    for t, v, n in zip(types, values, notes):
                        if v and v.strip():
                            Contact.objects.create(
                                contact_type=t,
                                value=v.strip(),
                                notes=n,
                                content_object=def_asst
                            )

                # =====================
                # CREAR CASE
                # =====================
                case = Case.objects.create(
                    adj_num=data.get('case-adj-num'),
                    adj_date=data.get('case-adj-date') or None,
                    claim_num=data.get('case-claim-num'),
                    claim_status=data.get('case-claim-status'),
                    settlement_date=data.get('case-settlement-date') or None,
                    status=case_status,
                    attorney=attorney,
                    assistant=assistant,
                    client=client,
                    employer=employer,
                    ins_carrier=ins_carrier,
                    claim_admin=claim_admin,
                    claim_adjuster=claim_adj,
                    def_lawfirm=def_law_firm,
                    def_attorney=def_att,
                    def_assistant=def_asst
                )

                # =====================
                # INJURIES
                # =====================
                fechas = data.getlist('injury-date')
                partes = data.getlist('injury-body-part')
                tipos = data.getlist('injury-type')

                for f, p, t in zip(fechas, partes, tipos):
                    if f and f.strip():  # evita registros vacíos
                        inj = Injury.objects.create(
                            case=case,
                            date=f,
                            body_part=BodyPart.objects.get(id=p),
                            type=InjuryType.objects.get(id=t)
                        )

                return redirect('search-cases')

        except Exception as e:
            print("ERROR:", e)
            
            # Context para re-renderizar el formulario
            context = {
                'case_statuses': CaseStatus.objects.filter(visible=True),
                'attorneys': Attorney.objects.filter(visible=True),
                'assistants': Assistant.objects.filter(visible=True),
                'body_parts': BodyPart.objects.filter(visible=True),
                'injury_types': InjuryType.objects.filter(visible=True),
                
                # Valores enviados para mantenerlos en el formulario
                'client_name': data.get('client', ''),
                'client_address': data.get('client-address', ''),
                'client_ssn': data.get('client-ssn', ''),
                'client_birth': data.get('client-birth', ''),
            }
            
            return render(request, 'create-case.html', context)

@method_decorator(login_required, name='dispatch')
class UpdateCase(View):

    def get(self, request, case_id):

        case = Case.objects.get(id=case_id)

        if not case.visible:
            redirect('home')

        context = {
            'case_statuses':CaseStatus.objects.filter(visible=True),
            'attorneys':Attorney.objects.filter(visible=True),
            'assistants':Assistant.objects.filter(visible=True),
            'body_parts':BodyPart.objects.filter(visible=True),
            'injury_types':InjuryType.objects.filter(visible=True),

            'case':case,
            'client':case.client,
            'client_contacts':case.client.contacts.filter(visible=True),
            'case_attorney':case.attorney,
            'case_assistant':case.assistant,
            'case_status':case.status,
            'employer':case.employer,
            'ins_carrier':case.ins_carrier,
            'claim_admin':case.claim_admin,
            'claim_adj':case.claim_adjuster,
            'claim_adj_contacts':case.claim_adjuster.contacts.filter(visible=True),
            'def_lawfirm':case.def_lawfirm,
            'def_att':case.def_attorney,
            'def_asst':case.def_assistant,
            'def_asst_contacts':case.def_assistant.contacts.filter(visible=True),
            'status_color':'#0b0',
            'injuries':case.injuries.filter(visible=True),
        }

        print(context['claim_adj'])

        return render(request, 'edit-case.html', context)

    def post(self, request, case_id):
        data = request.POST

        try:
            with transaction.atomic():

                case = Case.objects.get(id=case_id)

                # =====================
                # CASE INFO
                # =====================
                case.status = CaseStatus.objects.get(id=data.get('case-status'))
                case.attorney = Attorney.objects.get(id=data.get('attorney-id'))
                case.assistant = Assistant.objects.get(id=data.get('assistant-id'))

                case.adj_num = data.get('case-adj-num')
                case.adj_date = data.get('case-adj-date') or None
                case.claim_num = data.get('case-claim-num')
                case.claim_status = data.get('case-claim-status')
                case.settlement_date = data.get('case-settlement-date') or None

                # =====================
                # CLIENT
                # =====================
                client = case.client
                client.name = data.get('client-name')
                client.address = data.get('client-address')
                client.ssn = data.get('client-ssn')
                client.birth_date = data.get('client-birth')
                client.save()

                # =====================
                # CLIENT CONTACTS (reset + recreate)
                # =====================
                ids = data.getlist('client-contact-id')
                types = data.getlist('client-contact-type')
                values = data.getlist('client-contact-value')
                notes = data.getlist('client-contact-notes')

                existing_ids = []

                for contact_id, t, v, n in zip_longest(ids, types, values, notes):
                    if not v or not v.strip():
                        continue

                    if contact_id:
                        contact = Contact.objects.get(id=contact_id)

                        if contact:
                            contact.contact_type = t
                            contact.value = v
                            contact.notes = n
                            contact.save()
                            existing_ids.append(contact.id)
                            continue

                    # CREATE
                    contact = Contact.objects.create(
                        contact_type=t,
                        value=v,
                        notes=n,
                        content_object=client
                    )
                    existing_ids.append(contact.id)

                for contact in client.contacts.exclude(id__in=existing_ids):
                    contact.visible = False
                    contact.save()

                # =====================
                # EMPLOYER
                # =====================
                employer = case.employer
                employer.name = data.get('employer-name')
                employer.address = data.get('employer-address')
                employer.save()

                # =====================
                # INSURANCE
                # =====================
                ins = case.ins_carrier
                ins.name = data.get('insurance-name')
                ins.address = data.get('insurance-address')
                ins.save()

                # =====================
                # CLAIM ADMIN
                # =====================
                claim_admin = case.claim_admin
                claim_admin.name = data.get('claim-admin-name')
                claim_admin.address = data.get('claim-admin-address')
                claim_admin.save()

                # =====================
                # CLAIM ADJUSTER
                # =====================
                
                claim_adj = case.claim_adjuster
                claim_adj.name = data.get('claim-adj-name')
                claim_adj.save()

                ids = data.getlist('claim-adj-contact-id')
                types = data.getlist('claim-adj-contact-type')
                values = data.getlist('claim-adj-contact-value')
                notes = data.getlist('claim-adj-contact-notes')

                existing_ids = []

                for contact_id, t, v, n in zip_longest(ids, types, values, notes):
                    if not v or not v.strip():
                        continue

                    if contact_id:
                        contact = Contact.objects.get(id=contact_id)

                        if contact:
                            contact.contact_type = t
                            contact.value = v
                            contact.notes = n
                            contact.save()
                            existing_ids.append(contact.id)
                            continue

                    # CREATE
                    contact = Contact.objects.create(
                        contact_type=t,
                        value=v,
                        notes=n,
                        content_object=claim_adj
                    )
                    existing_ids.append(contact.id)

                for contact in claim_adj.contacts.exclude(id__in=existing_ids):
                    contact.visible = False
                    contact.save()

                # =====================
                # DEFENSE
                # =====================
                def_law = case.def_lawfirm
                def_law.name = data.get('law-firm-name')
                def_law.address = data.get('law-firm-address')
                def_law.save()

                def_att = case.def_attorney
                def_att.name = data.get('def-att-name')
                def_att.save()

                def_asst = case.def_assistant
                def_asst.name = data.get('def-asst-name')
                def_asst.save()

                # contactos assistant 

                ids = data.getlist('def-asst-contact-id')
                types = data.getlist('def-asst-contact-type')
                values = data.getlist('def-asst-contact-value')
                notes = data.getlist('def-asst-contact-notes')

                existing_ids = []

                for contact_id, t, v, n in zip_longest(ids, types, values, notes):
                    if not v or not v.strip():
                        continue

                    if contact_id:
                        contact = Contact.objects.get(id=contact_id)

                        if contact:
                            contact.contact_type = t
                            contact.value = v
                            contact.notes = n
                            contact.save()
                            existing_ids.append(contact.id)
                            continue

                    # CREATE
                    contact = Contact.objects.create(
                        contact_type=t,
                        value=v,
                        notes=n,
                        content_object=def_asst
                    )
                    existing_ids.append(contact.id)

                for contact in def_asst.contacts.exclude(id__in=existing_ids):
                    contact.visible = False
                    contact.save()


                # =====================
                # INJURIES
                # =====================
                ids = data.getlist('injury-id')
                dates = data.getlist('injury-date')
                parts = data.getlist('injury-body-part')
                types = data.getlist('injury-type')

                existing_ids = []

                for injury_id, d, p, t in zip_longest(ids, dates, parts, types):

                    if not d:  # evita vacíos
                        continue

                    if injury_id:
                        injury = Injury.objects.filter(id=injury_id).first()

                        if injury:
                            injury.date = d
                            injury.body_part = BodyPart.objects.get(id=p)
                            injury.injury_type = InjuryType.objects.get(id=t)
                            injury.visible = True  # 🔥 por si estaba oculto
                            injury.save()

                            existing_ids.append(injury.id)
                            continue

                    # CREATE
                    injury = Injury.objects.create(
                        case=case,
                        date=d,
                        body_part=BodyPart.objects.get(id=p),
                        injury_type=InjuryType.objects.get(id=t)
                    )

                    existing_ids.append(injury.id)

                for injury in case.injuries.exclude(id__in=existing_ids):
                    injury.visible = False
                    injury.save()
 

                case.save()

                return redirect('view-case', case_id=case_id)

        except Exception as e:
            print("ERROR:", e)
            context = {
                'case_statuses':CaseStatus.objects.filter(visible=True),
                'attorneys':Attorney.objects.filter(visible=True),
                'assistants':Assistant.objects.filter(visible=True),
                'body_parts':BodyPart.objects.filter(visible=True),
                'injury_types':InjuryType.objects.filter(visible=True),

                'case':case,
                'client':case.client,
                'client_contacts':case.client.contacts.filter(visible=True),
                'employer':case.employer,
                'ins_carrier':case.ins_carrier,
                'claim_admin':case.claim_admin,
                'claim_adj':case.claim_adjuster,
                'adj_contacts':case.claim_adjuster.contacts.filter(visible=True),
                'def_lawfirm':case.def_lawfirm,
                'def_att':case.def_attorney,
                'def_asst':case.def_assistant,
                'def_asst_contacts':case.def_assistant.contacts.filter(visible=True),
                'status_color':'#0b0',
                'case_status':case.status,
                'injuries':case.injuries.filter(visible=True),
            }
 
            return redirect('view-case', case_id=case_id)

        data = request.POST

        case = Case.objects.get(id=case_id)
        case.status = CaseStatus.objects.get(id=data.get('case-status'))
        case.attorney = Attorney.objects.get(id=data.get('attorney'))
        case.assistant = Assistant.objects.get(id=data.get('assistant'))

        if not case.visible:
            redirect('home')
        
        client = case.client
        client.name = data.get('client-name')
        client.address = data.get('client-address')
        client.ssn = data.get('client.ssn')
        client.birth_date = data.get('client.birth')

        employer = case.employer
        employer.name = data.get('employer-name')
        employer.address = data.get()

        return redirect('view-case', case_id=case_id)

@method_decorator(login_required, name='dispatch')
class SearchCases(View):

    def get(self, request):

        data = request.GET

        search = data.get('q') if data.get('q') != "" else None
        selected_filter = data.get('filter') if data.get('filter') != "" else None

        filter_options = [
            ('', ''),
            ('client', 'Clients'),
            ('status', 'Status'),
            ('employer', 'Employers'),
            ('insurance', 'Insurance Carrier'),
            ('claim_admin', 'Claim Admin'),
            ('claim_adjuster', 'Claim Adjuster'),
            ('def_lawfirm', 'D. Law firm'),
            ('def_attorney', 'D. Attorney'),
            ('def_assistant', 'D. Assistant'),
        ]

        cases = Case.objects.all().order_by('-id')

        if search:
            if selected_filter == 'client':
                cases = cases.filter(client__name__icontains=search)

            elif selected_filter == 'status':
                cases = cases.filter(status__name__icontains=search)

            elif selected_filter == 'employer':
                cases = cases.filter(employer__name__icontains=search)

            elif selected_filter == 'insurance':
                cases = cases.filter(ins_carrier__name__icontains=search)

            elif selected_filter == 'claim_admin':
                cases = cases.filter(claim_admin__name__icontains=search)

            elif selected_filter == 'claim_adjuster':
                cases = cases.filter(claim_adjuster__name__icontains=search)

            elif selected_filter == 'lawfirm':
                cases = cases.filter(def_lawfirm__name__icontains=search)

            elif selected_filter == 'def_attorney':
                cases = cases.filter(def_attorney__name__icontains=search)

            elif selected_filter == 'def_assistant':
                cases = cases.filter(def_assistant__name__icontains=search)

            else:
                cases = cases.filter(
                    Q(client__name__icontains=search) |
                    Q(status__name__icontains=search) |
                    Q(employer__name__icontains=search) |
                    Q(ins_carrier__name__icontains=search) |
                    Q(claim_admin__name__icontains=search) |
                    Q(claim_adjuster__name__icontains=search) |
                    Q(def_lawfirm__name__icontains=search) |
                    Q(def_attorney__name__icontains=search) |
                    Q(def_assistant__name__icontains=search)
                )

            context = {
                "cases": cases,
                "search": search,
                "selected_filter": selected_filter,
                "filter_options": filter_options,
            }
            
            return render(request, 'search-cases.html', context)
        
        else:
            context = {
                'cases': Case.objects.filter(visible=True).order_by('-id'),
                'selected_filter': None,
                'filter_options': filter_options,
            }
            return render(request, 'search-cases.html', context)
    
@method_decorator(login_required, name='dispatch')
class ViewCase(View):

    def get(self, request, case_id):

        
 
        case = Case.objects.get(id=case_id)
        context = {
            'case':case,
            'client':case.client,
            'client_contacts':case.client.contacts.filter(visible=True) if case.client else None,
            'employer':case.employer,
            'ins_carrier':case.ins_carrier,
            'claim_admin':case.claim_admin,
            'claim_adj':case.claim_adjuster,
            'adj_contacts':case.claim_adjuster.contacts.filter(visible=True) if case.claim_adjuster else None,
            'def_lawfirm':case.def_lawfirm,
            'def_att':case.def_attorney,
            'def_asst':case.def_assistant,
            'def_asst_contacts':case.def_assistant.contacts.filter(visible=True) if case.def_assistant else None,
            'injuries':case.injuries.filter(visible=True),
            'status_color':'#0b0',
            'status':case.status.name
        } 

        return render(request, 'view-case.html', context)


# Vistas individuales para cada modelo.
@method_decorator(login_required, name='dispatch')
class ViewClients(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        clients = Client.objects.filter(visible=True) 

        if search:
            clients = Client.objects.filter(
                Q(name__icontains=search) | 
                Q(ssn__icontains=search) |
                Q(address__icontains=search),
                Q(visible=True)
            )

        else: search = ""

        context = {
            "clients":clients,
            "search_value":search,
        }
        return render(request, 'view-clients.html', context)
    
    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            client = Client.objects.get(id=id)
            print(client)
            client.visible = False
            client.save()
            return redirect('view-clients')
    
        if action == "save":
            client = Client.objects.get(id=id)
        else: 
            client = Client() 

        client.name = data.get("name")
        client.address = data.get("address")
        client.ssn = data.get("ssn")
        client.birth_date = data.get("birth_date") 
        client.save()
        
        return redirect('view-clients')

@method_decorator(login_required, name='dispatch')
class ViewEmployers(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        employers = Employer.objects.filter(visible=True) 

        if search:
            employers = Employer.objects.filter( 
                Q(name__icontains=search) |  
                Q(address__icontains=search),
                Q(visible=True)
            )

        else: search = ""

        context = {
            "employers":employers,
            "search_value":search,
        }
        return render(request, 'view-employers.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            employer = Employer.objects.get(id=id) 
            employer.visible = False
            employer.save()

            print(employer.visible)
            return redirect('view-employers')
    
        if action == "save":
            employer = Employer.objects.get(id=id)
        else: 
            employer = Employer() 

        employer.name = data.get("name")
        employer.address = data.get("address") 
        employer.save()
        
        return redirect('view-employers')
    
@method_decorator(login_required, name='dispatch')
class ViewInsCarriers(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        ins_carriers = InsuranceCarrier.objects.filter(visible=True) 

        if search:
            ins_carriers = InsuranceCarrier.objects.filter( 
                Q(name__icontains=search) |  
                Q(address__icontains=search),
                Q(visible=True)
            )

        else: search = ""

        context = {
            "ins_carriers":ins_carriers,
            "search_value":search,
        }
        return render(request, 'view-ins-carriers.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            ins_carrier = InsuranceCarrier.objects.get(id=id) 
            ins_carrier.visible = False
            ins_carrier.save()

            print(ins_carrier.visible)
            return redirect('view-ins-carriers')
    
        if action == "save":
            ins_carrier = InsuranceCarrier.objects.get(id=id)
        else: 
            ins_carrier = InsuranceCarrier() 

        ins_carrier.name = data.get("name")
        ins_carrier.address = data.get("address") 
        ins_carrier.save()
        
        return redirect('view-ins-carriers')

@method_decorator(login_required, name='dispatch')
class ViewClaimAdmins(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        claim_admins = ClaimAdministrator.objects.filter(visible=True) 

        if search:
            claim_admins = ClaimAdministrator.objects.filter( 
                Q(name__icontains=search) |  
                Q(address__icontains=search),
                Q(visible=True)
            )

        else: search = ""

        context = {
            "claim_admins":claim_admins,
            "search_value":search,
        }
        return render(request, 'view-claim-admins.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            claim_admin = ClaimAdministrator.objects.get(id=id) 
            claim_admin.visible = False
            claim_admin.save() 
            return redirect('view-claim-admins')
    
        if action == "save":
            claim_admin = ClaimAdministrator.objects.get(id=id)
        else: 
            claim_admin = ClaimAdministrator() 

        claim_admin.name = data.get("name")
        claim_admin.address = data.get("address") 
        claim_admin.save()
        
        return redirect('view-claim-admins')

@method_decorator(login_required, name='dispatch')    
class ViewDefLawFirms(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        def_lawfirms = DefenseLawFirm.objects.filter(visible=True) 

        if search:
            def_lawfirms = DefenseLawFirm.objects.filter( 
                Q(name__icontains=search) |  
                Q(address__icontains=search),
                Q(visible=True)
            )

        else: search = ""

        context = {
            "def_lawfirms":def_lawfirms,
            "search_value":search,
        }
        return render(request, 'view-def-lawfirms.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            def_lawfirm = DefenseLawFirm.objects.get(id=id) 
            def_lawfirm.visible = False
            def_lawfirm.save()

            return redirect('view-def-lawfirms')
    
        if action == "save":
            def_lawfirm = DefenseLawFirm.objects.get(id=id)
        else: 
            def_lawfirm = DefenseLawFirm() 

        def_lawfirm.name = data.get("name")
        def_lawfirm.address = data.get("address") 
        def_lawfirm.save()
        
        return redirect('view-def-lawfirms')

@method_decorator(login_required, name='dispatch')
class ViewCaseStatuses(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        case_statuses = CaseStatus.objects.filter(visible=True) 

        if search:
            case_statuses = CaseStatus.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "case_statuses":case_statuses,
            "search_value":search,
        }
        return render(request, 'view-case-statuses.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            case_status = CaseStatus.objects.get(id=id) 
            case_status.visible = False
            case_status.save()
            return redirect('view-case-statuses')
    
        if action == "save":
            case_status = CaseStatus.objects.get(id=id)
        else: 
            case_status = CaseStatus() 

        case_status.name = data.get("name") 
        case_status.save()
        
        return redirect('view-case-statuses')

@method_decorator(login_required, name='dispatch')
class ViewBodyParts(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        body_parts = BodyPart.objects.filter(visible=True) 

        if search:
            body_parts = BodyPart.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "body_parts":body_parts,
            "search_value":search,
        }
        return render(request, 'view-body-parts.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            body_part = BodyPart.objects.get(id=id) 
            body_part.visible = False
            body_part.save()
            return redirect('view-body-parts')
    
        if action == "save":
            body_part = BodyPart.objects.get(id=id)
        else: 
            body_part = BodyPart() 

        body_part.name = data.get("name") 
        body_part.save()
        
        return redirect('view-body-parts')

@method_decorator(login_required, name='dispatch')
class ViewInjuryTypes(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        injury_types = InjuryType.objects.filter(visible=True) 

        if search:
            injury_types = InjuryType.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "injury_types":injury_types,
            "search_value":search,
        }
        return render(request, 'view-injury-types.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            injury_type = InjuryType.objects.get(id=id) 
            injury_type.visible = False
            injury_type.save()
            return redirect('view-injury-types')
    
        if action == "save":
            injury_type = InjuryType.objects.get(id=id)
        else: 
            injury_type = InjuryType() 

        injury_type.name = data.get("name") 
        injury_type.save()
        
        return redirect('view-injury-types')

@method_decorator(login_required, name='dispatch')   
class ViewDefAttorneys(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        def_attorneys = DefenseAttorney.objects.filter(visible=True) 

        if search:
            def_attorneys = DefenseAttorney.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "def_attorneys":def_attorneys,
            "search_value":search,
        }
        return render(request, 'view-def-attorneys.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            def_attorney = DefenseAttorney.objects.get(id=id) 
            def_attorney.visible = False
            def_attorney.save()
            return redirect('view-def-attorneys')
    
        if action == "save":
            def_attorney = DefenseAttorney.objects.get(id=id)
        else: 
            def_attorney = DefenseAttorney() 

        def_attorney.name = data.get("name") 
        def_attorney.save()
        
        return redirect('view-def-attorneys')

@method_decorator(login_required, name='dispatch')    
class ViewDefAssistants(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        def_assistants = DefenseAssistant.objects.filter(visible=True) 

        if search:
            def_assistants = DefenseAssistant.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "def_assistants":def_assistants,
            "search_value":search,
        }
        return render(request, 'view-def-assistants.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            def_assistant = DefenseAssistant.objects.get(id=id) 
            def_assistant.visible = False
            def_assistant.save()
            return redirect('view-def-assistants')
    
        if action == "save":
            def_assistant = DefenseAssistant.objects.get(id=id)
        else: 
            def_assistant = DefenseAssistant() 

        def_assistant.name = data.get("name") 
        def_assistant.save()
        
        return redirect('view-def-assistants')

@method_decorator(login_required, name='dispatch') 
class ViewClaimAdjusters(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        claim_adjusters = ClaimAdjuster.objects.filter(visible=True) 

        if search:
            claim_adjusters = ClaimAdjuster.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "claim_adjusters":claim_adjusters,
            "search_value":search,
        }
        return render(request, 'view-claim-adjusters.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            claim_adjuster = ClaimAdjuster.objects.get(id=id) 
            claim_adjuster.visible = False
            claim_adjuster.save()
            return redirect('view-claim-adjusters')
    
        if action == "save":
            claim_adjuster = ClaimAdjuster.objects.get(id=id)
        else: 
            claim_adjuster = ClaimAdjuster() 

        claim_adjuster.name = data.get("name") 
        claim_adjuster.save()
        
        return redirect('view-claim-adjusters')

@method_decorator(login_required, name='dispatch')  
class ViewAttorneys(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        attorneys = Attorney.objects.filter(visible=True) 

        if search:
            attorneys = Attorney.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "attorneys":attorneys,
            "search_value":search,
        }
        return render(request, 'view-attorneys.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            attorney = Attorney.objects.get(id=id) 
            attorney.visible = False
            attorney.save()

            user = attorney.user
            user.visible = False
            user.save()
        
            return redirect('view-attorneys')
    
        if action == "save":
            attorney = Attorney.objects.get(id=id)
            user = attorney.user
        else: 
            attorney = Attorney.objects.filter(name=data.get("name")).first()
            if not attorney:
                attorney = Attorney()

            user = SystemUser()
            attorney.user = user

        user.username = data.get("name")
        user.set_password(data.get("password"))
        user.role = "attorney"
        user.save()

        attorney.name = data.get("name") 
        attorney.save()
        
        return redirect('view-attorneys')

@method_decorator(login_required, name='dispatch')
class ViewAssistants(View):

    def get(self, request):
        data = request.GET
        search = data.get("search-value")

        assistants = Assistant.objects.filter(visible=True) 

        if search:
            assistants = Assistant.objects.filter( 
                Q(id__icontains=search) |
                Q(name__icontains=search),   
                Q(visible=True)
            )

        else: search = ""

        context = {
            "assistants":assistants,
            "search_value":search,
        }
        return render(request, 'view-assistants.html', context)

    def post(self, request):
        data = request.POST

        action = data.get("action") 
        id = data.get("id")

        if action == "delete":
            assistant = Assistant.objects.get(id=id) 
            assistant.visible = False
            assistant.save()

            user = assistant.user
            user.visible = False
            user.save()
        
            return redirect('view-assistants')
    
        if action == "save":
            assistant = Assistant.objects.get(id=id)
            user = assistant.user
        else: 
            assistant = Assistant.objects.filter(name=data.get("name")).first()
            if not assistant:
                assistant = Assistant()

            user = SystemUser()
            assistant.user = user

        user.username = data.get("name")
        user.set_password(data.get("password"))
        user.role = "assistant"
        user.save()

        assistant.name = data.get("name") 
        assistant.save()

        
        return redirect('view-assistants')



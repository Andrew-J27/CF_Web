from django.db import models as m
from django.contrib.auth.models import User
from datetime import date
from simple_history.models import HistoricalRecords

# Create your models here.
class SystemUser(User):
    ROLES = [
        ('admin','Admin'),
        ('attorney','Attorney'),
        ('assistant', 'Assistant')
    ]

    active = m.BooleanField(default=True)
    role = m.CharField(max_length=20, choices=ROLES, default='admin')

    class Meta:
        db_table = 'system_user'

    def __str__(self):
        return self.username
    
    def soft_delete(self):
        self.active = False
        self.save()
    
    def restore(self): 
        self.active = True
        self.save()
    
class BaseModel(m.Model):
    active = m.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.active = False
        self.save()
    
    def restore(self): 
        self.active = True
        self.save()

class CaseStatus(BaseModel):
    name = m.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'case_status'

class Attorney(BaseModel):
    name = m.CharField(max_length=50, unique=True)
    user = m.OneToOneField(SystemUser, on_delete=m.CASCADE, related_name='attorney')

    class Meta:
        db_table = 'attorney'
     
class Assistant(BaseModel):
    name = m.CharField(max_length=50, unique=True)
    user = m.OneToOneField(SystemUser, on_delete=m.CASCADE, related_name='assistant')

    class Meta:
        db_table = 'assistant'

class Client(BaseModel):
    name = m.CharField(max_length=50, blank=False)
    address = m.CharField(max_length=100, null=True, blank=True)
    ssn = m.CharField(max_length=30, null=True, blank=True)
    birth = m.DateField(null=True)

    class Meta:
        db_table = 'client' 
    
class Employer(BaseModel):
    name = m.CharField(max_length=100, unique=True)
    address = m.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'employer' 

class InsuranceCarrier(BaseModel):
    name = m.CharField(max_length=100, unique=True)
    address = m.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'insurance_carrier'

class ClaimAdministrator(BaseModel):
    name = m.CharField(max_length=100, unique=True)
    address = m.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'claim_administrator'

class ClaimAdjuster(BaseModel):
    name = m.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'claim_adjuster' 

class DefenseLawFirm(BaseModel):
    name = m.CharField(max_length=100, unique=True)
    address = m.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'defense_law_firm'

class DefenseAttorney(BaseModel):
    name = m.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'defense_attorney'
    
class DefenseAssistant(BaseModel):
    name = m.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'defense_assistant'


class Case(BaseModel):

    STATUSES = [
        ('denied','Denied'),
        ('delayed','Delayed'),
        ('accepted','Accepted')
    ]

    adj_date = m.DateField(null=True, blank=True)
    adj_num = m.CharField(max_length=40, null=True, blank=True)

    claim_num = m.CharField(max_length=40, null=True, blank=True)
    claim_status = m.CharField(max_length=10, null=True, blank=True, choices=STATUSES)
 
    settlement_date = m.DateField(null=True, blank=True)

    date_assigned = m.DateField(null=True, blank=True, help_text="Fecha en que el caso fue asignado a la firma o al asistente")

    status = m.ForeignKey(CaseStatus, on_delete=m.PROTECT, related_name='cases')
    attorney = m.ForeignKey(Attorney, on_delete=m.PROTECT, related_name='cases')
    assistant = m.ForeignKey(Assistant, on_delete=m.PROTECT, related_name='cases')

    client = m.ForeignKey(Client, on_delete=m.PROTECT, related_name='cases')
    employer = m.ForeignKey(Employer, on_delete=m.PROTECT, related_name='cases')
    
    insurance = m.ForeignKey(InsuranceCarrier, on_delete=m.PROTECT, related_name='cases', null=True)

    def_lawfirm = m.ForeignKey(DefenseLawFirm, on_delete=m.PROTECT, related_name='cases', null=True)
    def_attorney = m.ForeignKey(DefenseAttorney, on_delete=m.PROTECT, related_name='cases', null=True)
    def_assistant = m.ForeignKey(DefenseAssistant, on_delete=m.PROTECT, related_name='cases', null=True)

    claim_admin = m.ForeignKey(ClaimAdministrator, on_delete=m.PROTECT, related_name='cases', null=True)
    claim_adjuster = m.ForeignKey(ClaimAdjuster, on_delete=m.PROTECT, related_name='cases', null=True)

    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'case'

    def __str__(self):
        return f"{self.client.name} vs {self.employer.name}"
    
    def name(self):
        return f"{self.client.name} vs {self.employer.name}"
    
    def days_active(self):
        if self.settlement_date and self.adj_date:
            return (self.settlement_date - self.adj_date).days
        elif self.adj_date:
            return (date.today() - self.adj_date).days
        else:
            return "Case has not been adjudicated."


class InjuryType(BaseModel):
    name = m.CharField(max_length=50, unique=True)

    class Meta:
        db_table =  'injury_type'
    
class BodyPart(BaseModel):
    name = m.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'body_part'

class Injury(BaseModel):

    case = m.ForeignKey(Case, on_delete=m.CASCADE, related_name='injuries')
    date = m.DateField()
    part = m.ForeignKey(BodyPart, on_delete=m.CASCADE)
    type = m.ForeignKey(InjuryType, on_delete=m.CASCADE, null=True)

    class Meta:
        db_table = 'injury'

    def name(self):
        if self.part and self.type:
            return f"{self.type.name} on {self.part.name}"
        
        elif self.part and not self.type:
            return f"{self.part.name} injured"
        
        elif not self.part and self.type:
            return self.type.name

# Contacts 
class Contact(BaseModel):
    CONTACT_TYPES = [
        ('phone','📞'),
        ('email','🖂'),
        ('fax','🖷')
    ]

    type = m.CharField(max_length=30, choices=CONTACT_TYPES, default='phone')
    value = m.CharField(max_length=50) 
    notes = m.CharField(max_length=50, null=True, blank=True)

    class Meta: 
        abstract = True

    def __str__(self):
        return f"({self.type}) {self.value}"
    
class ClientContact(Contact):
    client = m.ForeignKey(Client, on_delete=m.CASCADE, related_name='contacts')

    class Meta:
        db_table = 'client_contact'

class ClaimAdjusterContact(Contact):
    claim_adj = m.ForeignKey(ClaimAdjuster, on_delete=m.CASCADE, related_name='contacts')

    class Meta:
        db_table = 'claim_adj_contact'

class DefenseAttorneyContact(Contact):
    def_attorney = m.ForeignKey(DefenseAttorney, on_delete=m.CASCADE, related_name='contacts')

    class Meta:
        db_table = 'def_attorney_contact'

class DefenseAssistantContact(Contact):
    def_assistant = m.ForeignKey(DefenseAssistant, on_delete=m.CASCADE, related_name='contacts')

    class Meta:
        db_table = 'def_assistant_contact'
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class SystemUser(User):
    ROLES = [
        ('admin','Admin'),
        ('attorney','Attorney'),
        ('assistant', 'Assistant')
    ]

    visible = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLES)

    class Meta:
        db_table = 'system_user'

    def __str__(self):
        return self.username
    
class BaseModel(models.Model):
    visible = models.BooleanField(default=True)

    class Meta:
        abstract = True

class CaseStatus(BaseModel): # Catalog of statuses
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'case_status'

    def __str__(self):
        return self.name
    
class BodyPart(BaseModel): # Catalog
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'body_part'

    def __str__(self):
        return self.name

class InjuryType(BaseModel): # Catalog
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'injury_type'

    def __str__(self):
        return self.name
    
class Contact(BaseModel):
    CONTACT_TYPES = [
        ('email','Email'),
        ('phone','Phone'),
        ('fax', 'Fax')
    ]

    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPES)
    value = models.CharField(max_length=100)
    notes = models.CharField(max_length=100, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return f"{self.value}"
    

class Attorney(BaseModel):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, null=True)    

    class Meta:
        db_table = 'attorney'

    def __str__(self):
        return self.name

class Assistant(BaseModel):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'assistant'

    def __str__(self):
        return self.name
    
class Client(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    ssn = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    contacts = GenericRelation(Contact, related_query_name='client')

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.name
    
class Employer(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'employer'

    def __str__(self):
        return self.name
    
class InsuranceCarrier(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'insurance_carrier'

    def __str__(self):
        return self.name

class ClaimAdministrator(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'claim_administrator'

    def __str__(self):
        return self.name
    
class ClaimAdjuster(BaseModel):
    name = models.CharField(max_length=100)
    contacts = GenericRelation(Contact, related_query_name='claim_adjuster')

    class Meta:
        db_table = 'claim_adjuster'

    def __str__(self):
        return self.name

class DefenseLawFirm(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'defense_law_firm'

    def __str__(self):
        return self.name
    
class DefenseAttorney(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'defense_attorney'

    def __str__(self):
        return self.name

class DefenseAssistant(BaseModel):
    name = models.CharField(max_length=100)
    contacts = GenericRelation(Contact, related_query_name='defense_assistant')

    class Meta:
        db_table = 'defense_assistant'

    def __str__(self):
        return self.name
    
class Case(BaseModel):
    adj_num = models.CharField(max_length=50)
    adj_date = models.DateField(null=True, blank=True)
    claim_num = models.CharField(max_length=100)
    claim_status = models.CharField(max_length=100)

    settlement_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(CaseStatus, null=True, on_delete=models.SET_NULL)
    last_update = models.DateTimeField(auto_now=True)

    attorney = models.ForeignKey(Attorney, on_delete=models.SET_NULL, null=True)
    assistant = models.ForeignKey(Assistant, on_delete=models.SET_NULL, null=True)

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, null=True)
    ins_carrier = models.ForeignKey(InsuranceCarrier, on_delete=models.SET_NULL, null=True)

    claim_admin = models.ForeignKey(ClaimAdministrator, on_delete=models.SET_NULL, null=True)
    claim_adjuster = models.ForeignKey(ClaimAdjuster, on_delete=models.SET_NULL, null=True)

    def_lawfirm = models.ForeignKey(DefenseLawFirm, on_delete=models.SET_NULL, null=True)
    def_attorney = models.ForeignKey(DefenseAttorney, on_delete=models.SET_NULL, null=True)
    def_assistant = models.ForeignKey(DefenseAssistant, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'case'

    def __str__(self):
        return f"{self.client.name} vs {self.employer.name}"
    
    def get_injuries(self):
        return self.injuries.filter(visible=True)
    

class Injury(BaseModel):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='injuries')
    
    type = models.ForeignKey(InjuryType, on_delete=models.SET_NULL, null=True)
    body_part = models.ForeignKey(BodyPart, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'injury'

    def __str__(self):
        if self.type:
            return f"{self.injury_type.name} on {self.body_part.name}"
        else: 
            return f"{self.body_part.name}"
from django.forms import ModelForm 
from .models import * 
from django import forms
from django.forms import inlineformset_factory

class CaseStatusForm(ModelForm): 
    class Meta:
        model = CaseStatus
        exclude = ['active'] 

class AttorneyForm(ModelForm):
    class Meta:
        model = Attorney
        exclude = ['active'] 

class AssistantForm(forms.ModelForm):
    class Meta:
        model = Assistant
        exclude = ['active']


# COMPANIES FORMS
class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ['active']

class InsuranceCarrierForm(forms.ModelForm):
    class Meta:
        model = InsuranceCarrier
        exclude = ['active']


class ClaimAdministratorForm(forms.ModelForm):
    class Meta:
        model = ClaimAdministrator
        exclude = ['active'] 
        
class DefenseLawFirmForm(forms.ModelForm):
    class Meta:
        model = DefenseLawFirm
        exclude = ['active']
 
# Client
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['active']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field'}),
            'address': forms.TextInput(attrs={'class': 'form-field'}),
            'ssn': forms.TextInput(attrs={'class': 'form-field'}),
            'birth': forms.DateInput(attrs={'class': 'form-field', 'type': 'date'}),
        }


class ClientContactForm(forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = ['type', 'value', 'notes', 'active']
        widgets = {
            'type': forms.Select(),
            'value': forms.TextInput(),
            'notes': forms.TextInput(),
            'active': forms.CheckboxInput(),
        }

ClientContactFormSet = inlineformset_factory(
    Client, 
    ClientContact,
    form=ClientContactForm,
    extra=0,  # Número de formularios vacíos adicionales
    can_delete=True,  # Permitir eliminar contactos
    min_num=0,  # Mínimo 1 contacto
    validate_min=False,  # Validar mínimo
    max_num=10,  # Máximo 10 contactos
    validate_max=True
)

# Claim Adjuster
class ClaimAdjusterForm(forms.ModelForm):
    class Meta:
        model = ClaimAdjuster
        exclude = ['active']

class ClaimAdjusterContactForm(forms.ModelForm):
    class Meta:
        model = ClaimAdjusterContact
        fields = ['type', 'value', 'notes', 'active']
        widgets = {
            'type': forms.Select(),
            'value': forms.TextInput(),
            'notes': forms.TextInput(),
            'active': forms.CheckboxInput(),
        }

ClaimAdjusterContactFormSet = inlineformset_factory(
    ClaimAdjuster, 
    ClaimAdjusterContact,
    form=ClaimAdjusterContactForm,
    extra=0,  # Número de formularios vacíos adicionales
    can_delete=True,  # Permitir eliminar contactos
    min_num=0,  # Mínimo 1 contacto
    validate_min=True,  # Validar mínimo
    max_num=10,  # Máximo 10 contactos
    validate_max=True
)


class DefenseAttorneyForm(forms.ModelForm):
    class Meta:
        model = DefenseAttorney
        exclude = ['active']

class DefenseAttorneyContactForm(forms.ModelForm):
    class Meta:
        model = DefenseAttorneyContact
        fields = ['type', 'value', 'notes', 'active']
        widgets = {
            'type': forms.Select(),
            'value': forms.TextInput(),
            'notes': forms.TextInput(),
            'active': forms.HiddenInput(),
        }

DefenseAttorneyContactFormSet = inlineformset_factory(
    DefenseAttorney, 
    DefenseAttorneyContact,
    form=DefenseAttorneyContactForm,
    extra=0,  # Número de formularios vacíos adicionales
    can_delete=True,  # Permitir eliminar contactos
    min_num=0,  # Mínimo 1 contacto
    validate_min=True,  # Validar mínimo
    max_num=10,  # Máximo 10 contactos
    validate_max=True
)

class DefenseAssistantForm(forms.ModelForm):
    class Meta:
        model = DefenseAssistant
        exclude = ['active'] 

class DefenseAssistantContactForm(forms.ModelForm):
    class Meta:
        model = DefenseAssistantContact
        fields = ['type', 'value', 'notes', 'active']
        widgets = {
            'type': forms.Select(),
            'value': forms.TextInput(),
            'notes': forms.TextInput(),
            'active': forms.CheckboxInput(),
        }

DefenseAssistantContactFormSet = inlineformset_factory(
    DefenseAssistant, 
    DefenseAssistantContact,
    form=DefenseAssistantContactForm,
    extra=0,  # Número de formularios vacíos adicionales
    can_delete=True,  # Permitir eliminar contactos
    min_num=0,  # Mínimo 1 contacto
    validate_min=True,  # Validar mínimo
    max_num=10,  # Máximo 10 contactos
    validate_max=True
)

         
class InjuryTypeForm(forms.ModelForm):
    class Meta:
        model = InjuryType
        exclude = ['active']

class BodyPartForm(forms.ModelForm):
    class Meta:
        model = BodyPart
        exclude = ['active']

class InjuryForm(forms.ModelForm):
    class Meta:
        model = Injury
        fields = ['date', 'part', 'type', 'active']
        
        widgets = { 
            'date': forms.DateInput(attrs={'class': 'form-field', 'type': 'date'}),
            'part': forms.Select(attrs={'class': 'form-field'}),
            'type': forms.Select(attrs={'class': 'form-field'}),
            'active': forms.CheckboxInput(),
        }

# Para usar con el modelo Case
InjuryFormSet = inlineformset_factory(
    Case,  # modelo padre
    Injury,  # modelo hijo
    form=InjuryForm, 
    extra=0,  # número de formularios vacíos adicionales
    can_delete=True,  # permite eliminar registros existentes
    min_num=1,  # número mínimo de formularios
    validate_min=False,  # Validar mínimo
    max_num=10,  # número máximo de formularios 
    validate_max=True
)

 
class CaseForm(forms.ModelForm):
    class Meta:
        model = Case

        fields = [
            'adj_date', 'adj_num', 'claim_num', 'claim_status',
            'settlement_date', 'status', 'attorney', 'assistant'
        ]

        widgets = {
            'adj_date': forms.DateInput(attrs={'type': 'date'}),
            'settlement_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'adj_date': 'Adjudication date',
            'adj_num': 'Adjudication number',
            'claim_num': 'Claim number',
            'claim_status': 'Claim Status',
            'settlement_date': 'Settlement date',
            'status': 'Case Status',
            'attorney': 'Attorney Handling',
            'assistant':'Assistant Handling'
        }


class OptionalModelForm(forms.ModelForm):

    """ModelForm que permite campos opcionales pero no guarda si está vacío"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
    
    def has_data(self):
        """Verifica si el formulario tiene algún dato"""
        return any(
            value for value in self.data.values() 
            if value and value != 'None'
        )
    
    def save(self, commit=True):
        """Solo guarda si hay datos"""
        if self.has_data() and self.is_valid():
            return super().save(commit=commit)
        return None
    
# Luego úsalos así:
class InsuranceCarrierOptionalForm(OptionalModelForm):
    class Meta:
        model = InsuranceCarrier
        exclude = ['active']

class DefenseLawFirmOptionalForm(OptionalModelForm):
    class Meta:
        model = DefenseLawFirm
        exclude = ['active']

class DefenseAttorneyOptionalForm(OptionalModelForm):
    class Meta:
        model = DefenseAttorney
        exclude = ['active']

class DefenseAssistantOptionalForm(OptionalModelForm):
    class Meta:
        model = DefenseAssistant
        exclude = ['active']

class ClaimAdministratorOptionalForm(OptionalModelForm):
    class Meta:
        model = ClaimAdministrator
        exclude = ['active']

class ClaimAdjusterOptionalForm(OptionalModelForm):
    class Meta:
        model = ClaimAdjuster
        exclude = ['active' ]

# Y así con los demás forms opcionales
# OPTIONAL MODEL FORMS

# forms.py 
from django.contrib.auth.hashers import make_password 
 
class SystemAttorneyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = Attorney
        fields = ['name']
        exclude = ['active', 'user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and SystemUser.objects.filter(username=name).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe")
        return name
    
    def clean(self): 
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data
    
    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("El formulario no es válido")
        
        # Usar el mismo 'name' como username
        username = self.cleaned_data['name']
        
        try:
            user = SystemUser.objects.create(
                username=username,
                password=make_password(self.cleaned_data['password']),
                role='attorney',
                active=True
            )
        except Exception as e:
            print(f'Error al crear SystemUser: {e}')
            raise
        
        # Crear el Attorney asociado
        attorney = super().save(commit=False)
        attorney.user = user
        attorney.name = username  # Aseguramos que coincidan
        
        if commit:
            attorney.save()
        
        return attorney
    

class SystemAssistantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = Assistant
        fields = ['name']
        exclude = ['active', 'user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and SystemUser.objects.filter(username=name).exists():
            raise forms.ValidationError("User already exists")
        return name
    
    def clean(self): 
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data
    
    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Form invalid")
        
        # Usar el mismo 'name' como username
        username = self.cleaned_data['name']
        
        try:
            user = SystemUser.objects.create(
                username=username,
                password=make_password(self.cleaned_data['password']),
                role='assistant',
                active=True
            )
        except Exception as e:
            print(f'Error al crear SystemUser: {e}')
            raise
        
        # Crear el Attorney asociado
        assistant = super().save(commit=False)
        assistant.user = user
        assistant.name = username  # Aseguramos que coincidan
        
        if commit:
            assistant.save()
        
        return assistant
    


# forms.py

class SystemAttorneyUpdateForm(forms.ModelForm):
    # Contraseña opcional
    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False,
        help_text="Dejar en blanco para mantener la contraseña actual"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False
    )
    
    class Meta:
        model = Attorney
        fields = ['name']  # Solo nombre es editable
        exclude = ['active', 'user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El nombre es opcional en actualización
        self.fields['name'].required = False
        self.fields['name'].help_text = "Dejar en blanco para mantener el nombre actual"
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Si no hay nombre, no validar
        if not name:
            return name
        
        # Verificar si ya existe otro usuario con ese nombre
        if SystemUser.objects.filter(username=name).exists():
            # Permitir si es el mismo usuario
            if self.instance and self.instance.user and self.instance.user.username == name:
                return name
            raise forms.ValidationError("Este nombre de usuario ya existe")
        
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # Solo validar si se proporcionó contraseña
        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Las contraseñas no coinciden")
            
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        return cleaned_data
    
    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("El formulario no es válido")
        
        attorney = self.instance
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')
        
        # Actualizar nombre si cambió
        if name and name != attorney.name:
            # Actualizar SystemUser
            if attorney.user:
                attorney.user.username = name
                attorney.user.save()
            
            # Actualizar Attorney
            attorney.name = name
        
        # Actualizar contraseña si se proporcionó
        if password and attorney.user:
            attorney.user.password = make_password(password)
            attorney.user.save()
        
        if commit:
            attorney.save()
        
        return attorney
    

class SystemAssistantUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False,
        help_text="Leave blank to keep current password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False
    )
    
    class Meta:
        model = Assistant
        fields = ['name']
        exclude = ['active', 'user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['name'].help_text = "Leave blank to keep current name"
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            return name
        
        if SystemUser.objects.filter(username=name).exists():
            if self.instance and self.instance.user and self.instance.user.username == name:
                return name
            raise forms.ValidationError("Username already exists")
        
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords don't match")
            
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters")
        
        return cleaned_data
    
    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Form invalid")
        
        assistant = self.instance
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')
        
        if name and name != assistant.name:
            if assistant.user:
                assistant.user.username = name
                assistant.user.save()
            assistant.name = name
        
        if password and assistant.user:
            assistant.user.password = make_password(password)
            assistant.user.save()
        
        if commit:
            assistant.save()
        
        return assistant
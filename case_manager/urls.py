from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),


    # CASE CRUD 
    path('case/', ListCases.as_view(), name='case'),
    path('case/create/', CreateCase.as_view(), name='create-case'),
    path('case/<int:pk>/update/', UpdateCase.as_view(), name='update-case'),
    path('case/<int:pk>/detail/', DetailCase.as_view(), name='detail-case'),
    path('case/<int:pk>/delete/', DeleteCase.as_view(), name='delete-case'),
    path('case/<int:pk>/restore/', RestoreCase.as_view(), name='restore-case'),

    path('case/<int:pk>/history/', CaseHistory.as_view(), name='case-history'),

    # REPORT
    path('report/', Report.as_view(), name='report'),
    path('download-report/', Home.as_view(), name='case_report'),    

    
    # ELEMENTS CRUD
    path('status/', ListCaseStatus.as_view(), name='status'),
    path('status/create/', CreateCaseStatus.as_view(), name='create-status'),
    path('status/<int:pk>/delete/', DeleteCaseStatus.as_view(), name='delete-status'),
    path('status/<int:pk>/update/', UpdateCaseStatus.as_view(), name='update-status'),
    path('status/<int:pk>/restore/', RestoreCaseStatus.as_view(), name='restore-status'),

    path('attorney/', ListAttorney.as_view(), name='attorney'),
    path('attorney/create/', CreateAttorney.as_view(), name='create-attorney'),
    path('attorney/<int:pk>/update/', UpdateAttorney.as_view(), name='update-attorney'),
    path('attorney/<int:pk>/delete/', DeleteAttorney.as_view(), name='delete-attorney'),
    path('attorney/<int:pk>/restore/', RestoreAttorney.as_view(), name='restore-attorney'),

    path('assistant/', ListAssistant.as_view(), name='assistant'),
    path('assistant/create/', CreateAssistant.as_view(), name='create-assistant'),
    path('assistant/<int:pk>/update/', UpdateAssistant.as_view(), name='update-assistant'),
    path('assistant/<int:pk>/delete/', DeleteAssistant.as_view(), name='delete-assistant'),
    path('assistant/<int:pk>/restore/', RestoreAssistant.as_view(), name='restore-assistant'),

    path('employer/', ListEmployer.as_view(), name='employer'),
    path('employer/create/', CreateEmployer.as_view(), name='create-employer'),
    path('employer/<int:pk>/update/', UpdateEmployer.as_view(), name='update-employer'),
    path('employer/<int:pk>/delete/', DeleteEmployer.as_view(), name='delete-employer'),
    path('employer/<int:pk>/restore/', RestoreEmployer.as_view(), name='restore-employer'),

    path('insurance-carrier/', ListInsuranceCarrier.as_view(), name='insurance-carrier'),
    path('insurance-carrier/create/', CreateInsuranceCarrier.as_view(), name='create-insurance-carrier'),
    path('insurance-carrier/<int:pk>/update/', UpdateInsuranceCarrier.as_view(), name='update-insurance-carrier'),
    path('insurance-carrier/<int:pk>/delete/', DeleteInsuranceCarrier.as_view(), name='delete-insurance-carrier'),
    path('insurance-carrier/<int:pk>/restore/', RestoreInsuranceCarrier.as_view(), name='restore-insurance-carrier'),

    path('claim-administrator/', ListClaimAdministrator.as_view(), name='claim-administrator'),
    path('claim-administrator/create/', CreateClaimAdministrator.as_view(), name='create-claim-administrator'),
    path('claim-administrator/<int:pk>/update/', UpdateClaimAdministrator.as_view(), name='update-claim-administrator'),
    path('claim-administrator/<int:pk>/delete/', DeleteClaimAdministrator.as_view(), name='delete-claim-administrator'),
    path('claim-administrator/<int:pk>/restore/', RestoreClaimAdministrator.as_view(), name='restore-claim-administrator'),
     
    path('defense-law-firm/', ListDefenseLawFirm.as_view(), name='defense-law-firm'),
    path('defense-law-firm/create/', CreateDefenseLawFirm.as_view(), name='create-defense-law-firm'),
    path('defense-law-firm/<int:pk>/update/', UpdateDefenseLawFirm.as_view(), name='update-defense-law-firm'),
    path('defense-law-firm/<int:pk>/delete/', DeleteDefenseLawFirm.as_view(), name='delete-defense-law-firm'),
    path('defense-law-firm/<int:pk>/restore/', RestoreDefenseLawFirm.as_view(), name='restore-defense-law-firm'),

        # Client URLs
    path('client/', ListClient.as_view(), name='client'),
    path('client/create/', CreateClient.as_view(), name='create-client'),
    path('client/<int:pk>/update/', UpdateClient.as_view(), name='update-client'),
    path('client/<int:pk>/delete/', DeleteClient.as_view(), name='delete-client'),
    path('client/<int:pk>/restore/', RestoreClient.as_view(), name='restore-client'),
    
    # Claim Adjuster URLs
    path('claim-adjuster/', ListClaimAdjuster.as_view(), name='claim-adjuster'),
    path('claim-adjuster/create/', CreateClaimAdjuster.as_view(), name='create-claim-adjuster'),
    path('claim-adjuster/<int:pk>/update/', UpdateClaimAdjuster.as_view(), name='update-claim-adjuster'),
    path('claim-adjuster/<int:pk>/delete/', DeleteClaimAdjuster.as_view(), name='delete-claim-adjuster'),
    path('claim-adjuster/<int:pk>/restore/', RestoreClaimAdjuster.as_view(), name='restore-claim-adjuster'),
    
    # Defense Attorney URLs
    path('defense-attorney/', ListDefenseAttorney.as_view(), name='defense-attorney'),
    path('defense-attorney/create/', CreateDefenseAttorney.as_view(), name='create-defense-attorney'),
    path('defense-attorney/<int:pk>/update/', UpdateDefenseAttorney.as_view(), name='update-defense-attorney'),
    path('defense-attorney/<int:pk>/delete/', DeleteDefenseAttorney.as_view(), name='delete-defense-attorney'),
    path('defense-attorney/<int:pk>/restore/', RestoreDefenseAttorney.as_view(), name='restore-defense-attorney'),
    
    # Defense Assistant URLs
    path('defense-assistant/', ListDefenseAssistant.as_view(), name='defense-assistant'),
    path('defense-assistant/create/', CreateDefenseAssistant.as_view(), name='create-defense-assistant'),
    path('defense-assistant/<int:pk>/update/', UpdateDefenseAssistant.as_view(), name='update-defense-assistant'),
    path('defense-assistant/<int:pk>/delete/', DeleteDefenseAssistant.as_view(), name='delete-defense-assistant'),
    path('defense-assistant/<int:pk>/restore/', RestoreDefenseAssistant.as_view(), name='restore-defense-assistant'),

    path('injury-type/', ListInjuryType.as_view(), name='injury-type'),
    path('injury-type/create/', CreateInjuryType.as_view(), name='create-injury-type'),
    path('injury-type/<int:pk>/update/', UpdateInjuryType.as_view(), name='update-injury-type'),
    path('injury-type/<int:pk>/delete/', DeleteInjuryType.as_view(), name='delete-injury-type'),
    path('injury-type/<int:pk>/restore/', RestoreInjuryType.as_view(), name='restore-injury-type'),
    
    # Body Part URLs
    path('body-part/', ListBodyPart.as_view(), name='body-part'),
    path('body-part/create/', CreateBodyPart.as_view(), name='create-body-part'),
    path('body-part/<int:pk>/update/', UpdateBodyPart.as_view(), name='update-body-part'),
    path('body-part/<int:pk>/delete/', DeleteBodyPart.as_view(), name='delete-body-part'),
    path('body-part/<int:pk>/restore/', RestoreBodyPart.as_view(), name='restore-body-part'),
    
    # Injury URLs
    path('injury/', ListInjury.as_view(), name='injury'),
    path('injury/create/', CreateInjury.as_view(), name='create-injury'),
    path('injury/<int:pk>/update/', UpdateInjury.as_view(), name='update-injury'),
    path('injury/<int:pk>/delete/', DeleteInjury.as_view(), name='delete-injury'),
    path('injury/<int:pk>/restore/', RestoreInjury.as_view(), name='restore-injury'),

]
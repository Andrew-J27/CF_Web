 
from django.urls import path 
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('new-case/', CreateCase.as_view(), name='create-case'),
    path('search-cases/', SearchCases.as_view(), name='search-cases'),
    path('view-cases/<int:case_id>/', ViewCase.as_view(), name='view-case'),
    path('edit-case/<int:case_id>/', UpdateCase.as_view(), name='edit-case'),

    path('view-clients/', ViewClients.as_view(), name='view-clients'),
    path('view-attorneys/', ViewAttorneys.as_view(), name='view-attorneys'),
    path('view-assistants/', ViewAssistants.as_view(), name='view-assistants'),
    path('view-employers/', ViewEmployers.as_view(), name='view-employers'),
    path('view-ins-carriers/', ViewInsCarriers.as_view(), name='view-ins-carriers'),
    path('view-claim-admins/', ViewClaimAdmins.as_view(), name='view-claim-admins'),
    path('view-def-lawfirms/', ViewDefLawFirms.as_view(), name='view-def-lawfirms'),
    path('view-case-statuses/', ViewCaseStatuses.as_view(), name='view-case-statuses'),
    path('view-body-parts/', ViewBodyParts.as_view(), name='view-body-parts'),
    path('view-injury-types/', ViewInjuryTypes.as_view(), name='view-injury-types'),
    path('view-def-attorneys/', ViewDefAttorneys.as_view(), name='view-def-attorneys'),
    path('view-def-assistants/', ViewDefAssistants.as_view(), name='view-def-assistants'),
    path('view-claim-adjusters/', ViewClaimAdjusters.as_view(), name='view-claim-adjusters'),
    
]

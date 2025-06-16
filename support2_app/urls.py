from django.urls import path

from .views import *

urlpatterns = [
    path('agent', AgentView.as_view()),
    path('agent/<int:tg_id>', AgentGetView.as_view()),
    path('count', CountGetView.as_view()),
    path('count/update', CountUpdateView.as_view()),
    path('contract', ContractView.as_view()),
    path('contract/get', ContractListView.as_view()),
    path('project/<int:id>', ProjectGetView.as_view()),
    path('project', ProjectView.as_view())
]
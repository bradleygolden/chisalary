from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from . import views


router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, base_name='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='chisalary'))
]

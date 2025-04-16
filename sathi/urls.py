from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import landing,register_view,login_view,logout_view,login_student_view, dashboard_view

urlpatterns = [
    path('landing/', landing, name="Landing"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('loginstudent/', login_student_view, name='login_student'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name="dashboard"),
]
# Only use in development!
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
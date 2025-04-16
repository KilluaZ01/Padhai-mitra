<<<<<<< HEAD
 # urls.py
=======
# urls.py
>>>>>>> a6510effefeb436d93ffaefc27ef1a07b424284b
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    landing, register_view, login_view,
<<<<<<< HEAD
    logout_view, login_student_view,upload_audio,test, teacher_student_add_view, teacher_notes, ask_view_student, dashboard_view, make_notes_view_student, dashboard_view_student, notes_view_student
=======
    logout_view, login_student_view, teacher_student_add_view, teacher_notes, ask_view_student, dashboard_view, make_notes_view_student, dashboard_view_student, notes_view_student
>>>>>>> a6510effefeb436d93ffaefc27ef1a07b424284b
)

urlpatterns = [
    path('', landing, name='Landing'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('login/student/', login_student_view, name='login_student'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard_student/', dashboard_view_student, name='dashboard_student'),
    path('student_notes/', notes_view_student, name='student_notes'),
    path('make_notes/', make_notes_view_student, name='make_notes'),
    path('student_ask/', ask_view_student, name='student_ask'),
    path('teacher_student/', teacher_student_add_view, name = 'teacher_student'),
    path('teacher_notes/', teacher_notes, name = 'teacher_notes'),
<<<<<<< HEAD
    path('test/', test, name='test'),
    path('upload_audio/',upload_audio, name='upload_audio'),
=======
>>>>>>> a6510effefeb436d93ffaefc27ef1a07b424284b
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
<<<<<<< HEAD

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
>>>>>>> a6510effefeb436d93ffaefc27ef1a07b424284b

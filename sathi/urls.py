# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    landing, register_view, register_student,save_image, login_view,test,logout_view, login_student_view,save_note_audio,upload_audio, teacher_student_add_view, teacher_notes, ask_view_student, dashboard_view, make_notes_view_student, dashboard_view_student, notes_view_student
    landing, register_view, register_student, login_view,test,logout_view, login_student_view,save_note_audio,upload_audio, teacher_student_add_view, teacher_notes, ask_view_student, dashboard_view, make_notes_view_student, teacher_questions, dashboard_view_student, notes_view_student

)

urlpatterns = [
    path('', landing, name='Landing'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('login/student/', login_student_view, name='login_student'),
    path('logout/', logout_view, name='logout'),
    path('test/', test, name='test'),
    path('upload_audio/', upload_audio, name='upload_audio'),
    path('save_note_audio/', save_note_audio, name='save_note_audio'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard_student/', dashboard_view_student, name='dashboard_student'),
    path('student_notes/', notes_view_student, name='student_notes'),
    path('make_notes/', make_notes_view_student, name='make_notes'),
    path('student_ask/', ask_view_student, name='student_ask'),
    path('teacher_student/', teacher_student_add_view, name = 'teacher_student'),
    path('teacher_notes/', teacher_notes, name = 'teacher_notes'),
    path("register_student/", register_student, name="register_student"),
    path('save_image/', save_image, name='save_image'),

    path('teacher_questions/', teacher_questions, name = 'teacher_questions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

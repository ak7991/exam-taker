from django.urls import path
from main import views

urlpatterns = [
    path('login/', views.login),
    path('teacher/login/', views.teacherLogin),
    path('student/login/', views.studentLogin),
    path('teacher/dashboard/', views.teacherDashboard),
    path('teacher/exam/create/', views.examCreate),
    path('teacher/exam/update/', views.examUpdate),
    path('teacher/exam/update/file', views.examUpdateFile),
    path('teacher/exam/request/', views.teacherExamRequest),
    path('teacher/exam/assign/', views.teacherExamStart),
    path('teacher/exam/end/', views.teacherExamEnd),
    path('teacher/exam/window', views.teacherExamWindow),
    path('exam/chat/request', views.examChatRequest),
    path('exam/users/request', views.examUsersRequest),
    path('', views.home),
]

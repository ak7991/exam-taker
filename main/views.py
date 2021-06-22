from django.http import request
from django.http.response import JsonResponse
from pyasn1.type.univ import Null
from main.models import *
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from .forms import DocumentForm
import pyrebase

#firebase config
config = {
    "apiKey": "AIzaSyD7ddl63JBC-Xxj2vKe99R5JJkxBJDvTVY",
    "authDomain": "exam-3d397.firebaseapp.com",
    "databaseURL": "https://exam-3d397-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "exam-3d397",
    "storageBucket": "exam-3d397.appspot.com",
    "messagingSenderId": "647787494671",
    "appId": "1:647787494671:web:6afa3e03b1184d113c127a",
    "measurementId": "G-2CTKYSPY7P"
}

firebase=pyrebase.initialize_app(config)
db=firebase.database()
storage = firebase.storage()

def home(request):
    return render(request, 'index.html')

def login(request):
    #check if already logged in
    if 'loggedIn' in request.COOKIES:
        if request.COOKIES.get('loggedIn') == 'teacher':
            return redirect(teacherDashboard)
        elif request.COOKIES.get('loggedIn') == 'student':
            return redirect(studentDashboard)

    #render login page
    return render(request, 'login.html')

def teacherLogin(request):
    if request.method == 'POST':
        teacherUsername = request.POST.get('teacher-username')
        teacherPassword = request.POST.get('teacher-password')
        if len(teacherUsername) < 3 or len(teacherPassword) < 8:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Details', 'displayError':'flex'})

        #check username, password
        loginDdata = db.child('Login').child('Teacher').get()
        teacherData = []
        if loginDdata is not None:
            for data in loginDdata.each():
                teacherData.append(data.val())
        for i in range(len(teacherData)):
            if teacherUsername == teacherData[i]['username']:
                if teacherPassword == teacherData[i]['password']:
                    response = redirect(teacherDashboard)
                    #save credentials to cookies
                    response.set_cookie('loggedIn', 'teacher', max_age=60*60*60*60*60)
                    response.set_cookie('uid', teacherUsername, max_age=60*60*60*60*60)
                    #render dashboard
                    return response
                else:
                    #return password error
                    response = render(request, 'login.html', {'error':'Login Failed! Invalid Password', 'error-display':'flex'})
                    return response

    #redirect to login
    return redirect(login)

def studentLogin(request):
    validateList = [[12,11,10,9,8,7,6,5,4,3,2,1],['A','B','C','D','E','F','G','H','I','J','K']]
    if request.method == 'POST':
        studentUsername = request.POST.get('student-username')
        studentPassword = request.POST.get('student-password')
        studentClass = request.POST.get('student-class')
        studentSection = request.POST.get('student-section')
        
        if studentClass not in validateList[0]:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Class'})
        if studentSection not in validateList[1]:
            return render(request, 'login.html', {'error':'Login Failed! Ivalid Section'})

        loginDdata = db.child('Login').child('Student').child(studentClass).child(studentSection).get()
        dataList = []

        if loginDdata is not None:
            for data in loginDdata.each():
                dataList.append(data.val())
        
        if len(dataList) > 0:
            for i in range(len(dataList)):
                if dataList[i]['username'] == studentUsername:
                    if dataList[i]['password'] == studentPassword:
                        return redirect(teacherDashboard)
                    else:
                        #return invalid password
                        return False
            else:
                #invalid details (data not exist)
                return False
        
    return redirect(login)

def teacherDashboard(request):
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    return render(request, 'teacherDashboard.html', {'username':currentUser})

def examCreate(request):
    print('thiss')
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('file')
        date = request.POST['date']

        #return error if title is empty
        if len(title) < 1:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Enter a title!','error-display':'flex'})

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'false', 'ended':'false', 'result':[]}

        db.child("Assignments").child(currentClass).child(title).set(assignmentData)
        print('yesss')    
        return HttpResponse('')
    
    print('nooo')
    return redirect(teacherDashboard)

def examUpdate(request):
    validClass = ['12','11','10','9','8','7','6','5','4','3','2','1']

    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')
    
    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['assignment_title']

        #return error if title is empty
        if len(title) < 1 or currentClass not in validClass:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Information!','error-display':'flex'})

        assignmentData = db.child("Assignments").child(currentClass).child(title).get()
        sendData = []
        
        if assignmentData is not None:
            for data in assignmentData.each():
                sendData.append(data.val())

        print(sendData)
        
        return JsonResponse({'assignmentData':sendData})
    
    return redirect(teacherDashboard)

def examUpdateFile(request):
    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    validClass = ['12','11','10','9','8','7','6','5','4','3','2','1']

    if request.method == 'POST':
        currentClass = request.POST['class']
        oldtitle = request.POST['old_title']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('fileURL')
        date = request.POST['date']

        if len(title) < 1 or currentClass not in validClass:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})
        
        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'false', 'ended':'false', 'result':[]}
        
        db.child("Assignments").child(currentClass).child(oldtitle).remove()
        db.child("Assignments").child(currentClass).child(title).update(assignmentData)

        return redirect(teacherDashboard)

    return redirect(teacherDashboard)

def teacherExamRequest(request):
    validClass = ['12','11','10','9','8','7','6','5','4','3','2','1']

    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']

        if currentClass not in validClass:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Class!','error-display':'flex'})
        
        assignments = db.child('Assignments').child(currentClass).get()
        assignments_data = []

        if assignments.val() is not None:
            for assignment in assignments.each():
                assignments_data.append(assignment.val())

        return JsonResponse({'assignment_list': assignments_data})

    return redirect(teacherDashboard)

def teacherExamStart(request):
    validClass = ['12','11','10','9','8','7','6','5','4','3','2','1']

    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('fileURL')
        date = request.POST['date']

        if len(title) < 1 or currentClass not in validClass:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'true', 'ended':'false', 'result':[]}

        db.child("Assignments").child(currentClass).child(title).update(assignmentData)

    return render(request, 'login.html')

def teacherExamEnd(request):
    validClass = ['12','11','10','9','8','7','6','5','4','3','2','1']

    if 'loggedIn' not in request.COOKIES:
        if request.COOKIES.get('loggedIn') != 'teacher':
            return redirect(login)
    if 'uid' in request.COOKIES:
        currentUser = request.COOKIES.get('uid')

    if request.method == 'POST':
        currentClass = request.POST['class']
        title = request.POST['title']
        time = request.POST['time']
        description = request.POST['description']
        file_URL = request.POST.get('fileURL')
        date = request.POST['date']

        if len(title) < 1 or currentClass not in validClass:
            return render(request, 'teacherDashboard.html', {'username':currentUser, 'error':'Invalid Details!','error-display':'flex'})

        assignmentData = {'title':title, 'time':time, 'description':description, 'file':file_URL, 'date':date, 'assigned':'true', 'ended':'true', 'result':[]}

        db.child("Assignments").child(currentClass).child(title).update(assignmentData)

    return render(request, 'login.html')

def teacherExamWindow(request):
    return render(request, 'login.html')

def examChatRequest(request):
    return HttpResponse('')

def examUsersRequest(request):
    return HttpResponse('')

def studentDashboard(request):
    return render(request, 'studentDashboard.html')
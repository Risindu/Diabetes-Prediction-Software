from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import  messages
from DiaSense import settings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression






# Create your views here.
def home(request):
    return render(request,"app/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Tyr another username")
            return redirect('home')

        if len(username)>20:
            messages.error(request,"Username must be 10 characters")

        if pass1 != pass2:
            messages.error(request,"Password didn't match!")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha numeric")
            return redirect('home')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, "Your account has been successfully created We have sent you a confirmation email, please confirm your email to activate your account")

        #welcome email
        subject = "Welcome to DiaSense- Diabetes Predictor"
        message = "Hello"+myuser.first_name+"! \n"+"Welcome to DiaSense! \n"+ "Thank you for visiting our website\n Please click on confirmation email to confirm your email address. \n\n Thank You! \n DiaSense(Team)"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently = True)
        return redirect('signin')

    return render(request,"app/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username= username, password = pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "app/index.html",{'fname': fname})


        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request,"app/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')


def predict(request):
    return render(request, 'app/predict.html')

def result(request):
    data = pd.read_csv("E:\\NDT IT\\Semester 2\\Software Engineering Fundementals\\Diabetes Prediction Software\\DiaSense\\Dataset\\diabetes.csv")
    X = data.drop(["Outcome","SkinThickness","BloodPressure","Insulin","DiabetesPedigreeFunction"], axis = 1)
    Y = data["Outcome"]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, Y_train)

    val1 = float(request.GET['pregnancies'])
    val2 = float(request.GET['glucose'])
    val3 = float(request.GET['bmi'])
    val4 = float(request.GET['age'])


    pred = model.predict(([[val1, val2, val3, val4]]))

    result1 = ""
    if pred==[1]:
        result1 = "Positive"

    else:
        result1 = "Negative"


    return render(request, 'app/result.html',{"result2":result1})

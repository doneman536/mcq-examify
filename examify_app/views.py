from django.shortcuts import render,redirect
from .forms import AI_mcq_gen, Signup_form
from .forms import Login_form
from .src.types_of_gens.none_text import safe_generate_mcqs
from .models import UserSignup
from django.db.models import Q
import os
from django.conf import settings




def display(request):
    return render(request, "index.html")

def display_mcqs(request,generated_mcqs=None,generated_mcqs_ans=None):
    if generated_mcqs == None :
        return render(request,'display_mcqs.html')
    return render(request,'display_mcqs.html',{'mcqs':generated_mcqs})


def Mcq_gen_view(request, username):
    form = AI_mcq_gen()
    if request.method == "POST":
        form = AI_mcq_gen(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            text = form.cleaned_data['text']
            count = form.cleaned_data['No_of_questions']
            mode = form.cleaned_data['mode']


            generated_mcqs , generated_mcqs_ans = safe_generate_mcqs(topic=topic,text=text,count=count,mode=mode)

            user = UserSignup.objects.get(username=username)
            if not user.history:
                file_path = os.path.join(settings.MEDIA_ROOT, f"user_histories/history_{username}.txt")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as fb:
                    fb.write(str(generated_mcqs))

                user.history.name = f"user_histories/history_{username}.txt"
                user.save()

            else :
                file_path = user.history.path
                with open(file_path, 'a') as fb:
                    fb.write("\n" + generated_mcqs)

            return display_mcqs(request,generated_mcqs,generated_mcqs_ans)
    return render(request, 'mcq_gen_web.html',{'form':form, 'username': username})




def user_signup(request):

    if request.method == "POST" :
        form = Signup_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if UserSignup.objects.filter(username=username).exists():
                return render(request,'user_signup.html',{'form':Signup_form,'username_msg':"User Already Exists"})
            
            model = UserSignup(username=username,email=email,password=password)
            model.save()

            return redirect('start_up')
    return render(request,'user_signup.html',{'form':Signup_form()})


def display_dashboard(request,username):
    user = UserSignup.objects.filter(username= username).first()


    if user :
        return render(request,'user_dashboard.html',{'username':user.username})
    

    return render(request,'user_dashboard.html')


def user_login(request):
    if request.method == "POST":
        form =Login_form(request.POST)
        if form.is_valid() :
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = UserSignup.objects.filter(Q(username=username) | Q(email=username)).first()

            if user :
                if user.password == password:
                    return redirect('user_dashboard',username=user.username)
                else :
                    return render(request,'user_login.html',{'form':Login_form(),'password_error':"Wrong Password"})
            else :
                return render(request, 'user_login.html',{'form':Login_form(),'username_error':"User doesn't exists"})
        

    return render(request,'user_login.html',{'form':Login_form()})




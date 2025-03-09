from django.shortcuts import render
from .forms import AI_mcq_gen
from .src.types_of_gens.none_text import safe_generate_mcqs



def display(request):
    return render(request, "index.html")




def Mcq_gen_view(request):
    form = AI_mcq_gen()
    if request.method == "POST":
        form = AI_mcq_gen(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            text = form.cleaned_data['text']
            count = form.cleaned_data['No_of_questions']
            mode = form.cleaned_data['mode']

            generated_mcqs , generated_mcqs_ans = safe_generate_mcqs(topic=topic,text=text,count=count,mode=mode)
            return render(request,'mcq_gen_web.html',{'form':form, 'mcqs':generated_mcqs,'ans':generated_mcqs_ans})
    return render(request, 'mcq_gen_web.html',{'form':form})

# Create your views here.

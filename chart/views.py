from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Avg
from .models import *
from .forms import *

User = get_user_model()


def home(request):
    charts_count = Chart.objects.count()
    user_count = User.objects.count()
    elem_count = Element.objects.count()
    context = {
        "charts_count":charts_count,
        "user_count":user_count,
        "elem_count":elem_count
    }
    return render(request, 'pages/home.html', context)

def PublicProfileView(request, username):
    user_p = User.objects.get(username=username)
    author = get_object_or_404(User, username=username)
    # Tab
    tab = request.GET.get('tab')
    title = None
    if tab == "charts":
        tab_chart = author.tanla.all()
        title = "Charts"
    else:
        tab_chart = ""
        title = f"amCharts - @{user_p.username}"

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                          request.FILES,
                                          instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_name = user_form.cleaned_data.get('username')
            user_form.save()
            profile_form.save()
            return redirect("app:profile", user_name)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    user_chart_count = author.tanla.count()
    context = {
        "user_p": user_p,
        "user_form":user_form,
        "profile_form":profile_form,
        "tab_chart":tab_chart,
        "title":title,
        "user_chart_count":user_chart_count
    }
    return render(request, 'pages/profile.html', context)

def NewDashboardView(request, username):
    user_p = User.objects.get(username=username)
    initial = {'key': 'value'}
    user = User.objects.get(username=username)
    author = get_object_or_404(User, username=username)
    dash = author.tanla.all()
    new_dash = None
    if request.method == 'POST':
        NewChart = NewChartFrom(data=request.POST)
        if NewChart.is_valid():
            new_dash = NewChart.save(commit=False)
            slug = NewChart.cleaned_data.get('slug')
            new_dash.author = author
            new_dash.save()
            return redirect("app:chart", slug) 
    else:
        NewChart = NewChartFrom()
    context={
        "user_p": user_p,
        "NewChart":NewChart,
    }
    return render(request, "pages/new.html", context)

def signup(request):
    form = Registration()
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    return render(request, 'registration/signup.html', {"form":form})

def ChartView(request, slug):
    chart = Chart.objects.get(slug=slug)
    post = get_object_or_404(Chart, slug=slug)
    elements = post.qoshish.all()
    elements_count = post.qoshish.count()
    number_avg = post.qoshish.aggregate(Avg("value"))
    new_element= None
    if request.method == 'POST':
        comment_form = NewElementForm(data=request.POST)
        if comment_form.is_valid():
            new_element = comment_form.save(commit=False)
            new_element.post = post
            new_element.save()
            return redirect("app:chart", slug) # redirect to this url
    else:
        comment_form = NewElementForm()

    context= {
        'elements': elements,
        'comment_form': comment_form,
        "chart":chart,
        "elements_count":elements_count,
        "number_avg":number_avg
        }
    
    return render(request, "pages/chart.html", context)
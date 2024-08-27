from django.shortcuts import render

# Create your views here.


def competitions(request):
    return render(request, 'core/competitions.html')

def datasets(request):
    return render(request, 'core/datasets.html')

def competitionForm(request):
    return render(request, 'core/competitionForm.html')

def datasetForm(request):
    return render(request, 'core/datasetForm.html')

def competitionView(request):
    return render(request, 'core/competitionView.html')

def datasetView(request):
    return render(request, 'core/datasetView.html')

def profile(request):
    return render(request, 'core/profile.html')

def signIn(request):
    return render(request, 'core/signIn.html')

def signUp(request):
    return render(request, 'core/signUp.html')

def rankings(request):
    return render(request, 'core/rankings.html')
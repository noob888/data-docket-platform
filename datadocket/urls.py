"""datadocket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import competitions,datasets, competitionView
from backend.views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/',datasets,name='profile'),
    path('competitions/', competition_list_html, name='competition_list'),
    path('competitions/',competitions,name='competitions'),
    path('datasets/', dataset_list, name='dataset_list'),
    path('datasets/',datasets,name='datasets'),
    path('datasetView/',datasets,name='datasetView'),
    # path('datasetForm/',datasets,name='datasetForm'),
    path('dataset/<int:dataset_id>/', dataset_detail, name='dataset_detail'),
    # path('dataset/create/', dataset_create, name='dataset_create'),
    path('dataset/<int:pk>/update/', dataset_update, name='dataset_update'),
    path('dataset/<int:pk>/delete/', dataset_delete, name='dataset_delete'),
    path('dataset/upload', upload_dataset,name='upload_dataset'),
    path('dataset/<int:dataset_id>/download', dataset_download,name='dataset_download'),
    path('competitionsForm/',competitions_form,name='competitionForm'),
    # path('competitionView/',competitionView,name='competitionView'),
    path('competitionJoin/<int:competition_id>/', competition_join, name='competition_join'),
    path('competitionView/<int:competition_id>/', competition_detail, name='competition_detail'),
    path('competitionView/<int:competition_id>/upload-solution', upload_solution, name='upload_solution'),
    # path('solution/<int:solution_id>/', solution_view, name='solution_view'),
    # path('signIn/',datasets,name='signIn'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('rankings/',rankings,name='rankings'),
    path('admin/', admin.site.urls),
    # User backend routes
    path('user/', user_list, name='user_list'),
    path('profile/<int:user_id>/', user_detail, name='profile'),
    path('update_competition/<int:competition_id>/', update_competition, name='update_competition'),
    path('competition/<int:competition_id>/contestant/<int:contestant_id>/delete/', contestant_delete, name='contestant_delete'),
    path('competition/<int:pk>/delete/', competition_delete, name='competition_delete'),
    path('competition/<int:competition_id>/contestant/<int:contestant_id>/delete/', remove_submission,name='remove_submission')
    # path('user/create/', user_create, name='user_create'),
    # path('user/<int:pk>/update/', user_update, name='user_update'),
    # path('user/<int:pk>/delete/', user_delete, name='user_delete'),
    # path('competitions/', competition_list, name='competition-list'),
]

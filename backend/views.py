from pyexpat.errors import messages
from django.http import Http404, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
# from azure.storage.blob import BlobServiceClient
from backend.models import*
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.db import IntegrityError
from django.utils import timezone

def user_list(request):
    users = User.objects.all()
    return render(request, 'user/user_list.html', {'users': users})


def user_detail(request, user_id):
    current_user = request.user
    my_profile = False
    if (current_user.user_id == user_id):
        my_profile = True
    this_user = get_object_or_404(User, user_id=user_id)
    datasets_list = []
    
    datasets_list = Dataset.objects.filter(uploaded_by = user_id)
    competitions_list = Competition.objects.filter(host = user_id)
    contestant_list = Contestant.objects.filter(user = user_id)
    participated_competitions_list =[]
    for row in contestant_list:
        participated_competitions_list.append(get_object_or_404(Competition, competition_id=row.competition_id))
    return render(request, 'core/profile.html', {'this_user': this_user, 'datasets_list': datasets_list,'competitions_list':competitions_list,'participated_competitions_list':participated_competitions_list, 'my_profile': my_profile})
   
    


def user_create(request):
    if request.method == 'POST':
        # Retrieve data from the form
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        is_superadmin = request.POST.get('is_superadmin')
        rank = request.POST.get('rank')
        university = request.POST.get('university')
        company = request.POST.get('company')

        # Create User object with given data
        user = User(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number,
                    is_superadmin=is_superadmin, rank=rank, university=university, company=company)

        try:
            user.save()
            print('PRIMARY KEY', user.pk)
            return redirect('user_detail', pk=user.pk)
        except Exception as e:
            print(f"Error saving user: {str(e)}")
            return HttpResponseServerError("Error creating user")
    else:
        return render(request, 'user/user_form.html')

@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        # Retrieve data from the form
        email = request.POST.get('email')

        # Update User object with given data
        user.email = email

        user.save()

        return redirect('user_detail', pk=user.pk)
    else:
        return render(request, 'user/user_form.html', {'user': user})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    else:
        return render(request, 'user/user_confirm_delete.html', {'user': user})

# TODO why is this here? Who put this? Was it created by Django?
# John is commenting this out because it's confusing. Also commented the view.
# @csrf_exempt
# def competition_list(request):
#     if request.method == 'GET':
#         competitions = Competition.objects.all()
#         competitions_json = serializers.serialize('json', competitions)
#         competitions_list = json.loads(competitions_json)
#         return JsonResponse(competitions_list, safe=False)

#     elif request.method == 'POST':
#         competition_data = json.loads(request.body)
#         competition = Competition.objects.create(
#             name=competition_data['name'],
#             category=competition_data['category'],
#             host_id=competition_data['host_id'],
#             prize_amount=competition_data['prize_amount'],
#             start_date=competition_data['start_date'],
#             end_date=competition_data['end_date'],
#             deliverable=competition_data['deliverable'],
#             visualization=competition_data['visualization'],
#             guaranteed_submissions=competition_data['guaranteed_submissions'],
#             is_featured=competition_data['is_featured'],
#             live_presentations=competition_data['live_presentations']
#         )
#         competition_json = serializers.serialize('json', [competition])
#         competition_dict = json.loads(competition_json)[0]
#         return JsonResponse(competition_dict, status=201)


def competition_list_html(request):
    competitions = Competition.objects.order_by('-created_date')
    return render(request, 'core/competitions.html', {'competitions': competitions,
                                                      'page_title': 'Competitions',
                                                      'description': 'Test your skills in a Datadocket competition.',
                                                      'banner_action': reverse('competitionForm'),
                                                      'banner_button': 'Host a Competition'})

@login_required
def competition_delete(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    userId=  competition.host.user_id
    competition.delete()
    
    return redirect(reverse('profile', args=[userId]))
@login_required
def remove_submission(request, contestant_id,competition_id):
    competition = get_object_or_404(Competition, competition_id=competition_id)
    contestant = get_object_or_404(Contestant, contestant_id=contestant_id)

    if request.method == 'POST':
        # Delete the contestant's submission for the competition
        CompetitionSolution.objects.filter(
            competition=competition,
            contestant=contestant
        ).delete()

        # Remove the contestant from the competition
        contestant.delete()

        # Redirect to the competition detail page
        return redirect('competition_detail', competition_id=competition_id)

    return render(request, 'competition_id.html', {'competition': competition})


@login_required
def competition_join(request, competition_id):
    try:
        # Attempt to create a new contestant entry for the current user and the given competition
        Contestant.objects.create(user=request.user, competition_id=competition_id, score=0)
    except IntegrityError:
        # If a contestant entry already exists for the current user and the given competition, do nothing
        pass

    return redirect('competition_detail', competition_id=competition_id)

def competition_detail(request, competition_id):
    competition = get_object_or_404(Competition, competition_id=competition_id)
    competition_dataset = get_list_or_404(CompetitionDataset, competition=competition_id)
    contestants = Contestant.objects.filter(competition=competition_id).order_by('-score')
    datac = []
    for contestant in contestants:
        contestant_username = contestant.user.username
        score =contestant.score

        data = {
            'username': contestant_username,
            'score': score,
            
        }
        datac.append((data))
    dataset = []
    for row in competition_dataset:
        dataset.append(get_object_or_404(Dataset, dataset_id=row.dataset_id))

    # TODO determine the current logged in user's user_id
    # then load the correct info depending on who's logged in
    # also determine if the current user has already joined this competition
    display_name = 'Join this Competition'
    destination_url = reverse('competition_join', args=[competition.competition_id])
    if request.user.is_authenticated:
        print(f'user is logged in with id: {request.user.user_id}')
        subscriber_list = []
        for contestant in contestants:
            print(f'competition id:{contestant.competition_id}', end=' ')
            print(f'user_id: {contestant.user_id}')
            subscriber_list.append(contestant.user_id)
        user = request.user
        today = datetime.today()
        today = today.replace(tzinfo=None)
        competition_start_naive = competition.start_date.replace(tzinfo=None)
        #TODO Add this later After tuesday
        if competition.host_id == user.user_id:
            if today < competition_start_naive:
                display_name = 'Manage this Competition'
                destination_url = reverse('update_competition', args=[competition.competition_id])
                # TODO create the manage competition page
                print('Current user is the host and competition hasn\'t started')
            elif today >= competition_start_naive:
                display_name = 'View Submissions'
                destination_url = reverse('update_competition', args=[competition.competition_id])
                # TODO pass a parameter to disable the competition edit form
                print('Current user is the host and competition has started')
        elif user.user_id in subscriber_list:
            display_name = 'Submit a Solution'
            destination_url = reverse('upload_solution', args=[competition.competition_id])
    else:
        # user is logged out
        display_name = 'Log in to Compete'
        destination_url = reverse('login')


    if request.method == 'GET':
        return render(request, 'core/competitionView.html', {'competition': competition,
                                                             'dataset': dataset,
                                                             'page_title': competition.name,
                                                             'description': competition.category,
                                                             'banner_action': destination_url,
                                                             'banner_button': display_name,
                                                             'contestants': datac})

    elif request.method == 'PUT':
        competition.name = request.POST['name']
        competition.category = request.POST['category']
        competition.host = request.POST['host_id']
        competition.prize_amount = request.POST['prize_amount']
        competition.start_date = request.POST['start_date']
        competition.end_date = request.POST['end_date']
        competition.deliverable = request.POST['deliverable']
        competition.visualization = request.POST['visualization']
        competition.guaranteed_submissions = request.POST['guaranteed_submissions']
        competition.is_featured = request.POST['is_featured']
        competition.live_presentations = request.POST['live_presentations']
        competition.save()
        return render(request, 'core/competitionView.html', {'competition': competition})

@login_required
def competitions_form(request):
    competitions = Competition.objects.all()

    if request.method == 'POST':
        form = CompetitionForm(request.POST, request.FILES)
        # print(request.user.pk)
        if form.is_valid():
           
            # Get the uploaded file from the form data
            file = form.cleaned_data['dataset_file']
            filename= file.name
            # Upload the file to Azure Blob Storage
            try:
                connect_str = "DefaultEndpointsProtocol=https;AccountName=datadocketdev;AccountKey=U6wIRDwFi5bCudkB/nEdNGtcnAKRNIhz0U20N9VJZq7MmfWrEU60qYubtF1vN/srP8Txob2BGsMG+AStWEE8wQ==;EndpointSuffix=core.windows.net"
                container_name = 'container1'
                blob_service_client = BlobServiceClient.from_connection_string(
                    connect_str)
                container_client = blob_service_client.get_container_client(
                    container_name)
                container_client.upload_blob(
                    name=filename, data=file.read(), overwrite=True)
            except Exception as e:
                messages.error(
                    request, 'Error uploading file: {}'.format(str(e)))
                return redirect('index')
            # Create a Dataset object and save it to the database
            dataset_obj = Dataset.objects.create(
                name=form.cleaned_data['dataset_name'],
                description=form.cleaned_data['dataset_description'],
                file_uri='https://{}.blob.core.windows.net/{}/{}'.format(
                    blob_service_client.account_name, container_name, filename),
                uploaded_by=User.objects.get(user_id = request.user.user_id)
            )
            dataset_obj.save()

            competition_obj = Competition.objects.create(
                name=form.cleaned_data['competition_name'],
                category=form.cleaned_data['categories'],
                host_id=request.user.user_id, # assuming that there's a user logged in
                prize_amount=form.cleaned_data['competition_prize'],
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                # deliverable=form.cleaned_data['competition_description'],
                guaranteed_submissions=form.cleaned_data.get('guaranteed_submissions', False),
                is_featured=form.cleaned_data.get('features', []) and True or False,
                live_presentations=form.cleaned_data.get('live_presentations', False),
                premium= form.cleaned_data.get('premium', False)
            )
            competition_obj.save()

            competitionDataset = CompetitionDataset.objects.create(
                competition = Competition.objects.get(competition_id=competition_obj.competition_id),
                dataset = Dataset.objects.get(dataset_id=dataset_obj.dataset_id),
            )
            competitionDataset.save()

            return redirect('competition_detail', competition_id=competition_obj.competition_id)
            
    else:
        form = CompetitionForm()

    return render(request, 'core/competitionsForm.html', {
        'competitions': competitions,
        'page_title': 'Host a Competition',
        'description': 'Let Datadocket\'s users take care of the work',
        'banner_action': None,
        'banner_button': '',
        'form': form,
    })


def dataset_list(request):
    datasets = Dataset.objects.order_by('-count_of_downloads')
    return render(request, 'core/datasets.html', {'datasets': datasets,
                                                  'page_title': 'Datasets',
                                                  'description': 'Make your next discovery with one of Datadocket\'s datasets',
                                                  # TODO go to Dataset Create page
                                                  'banner_action': reverse('upload_dataset'),
                                                  'banner_button': 'Upload a Dataset'})


def dataset_detail(request, dataset_id):
    try:
        dataset = Dataset.objects.get(dataset_id=dataset_id)
    except Dataset.DoesNotExist:
        raise Http404("Dataset does not exist")

    competition_dataset = CompetitionDataset.objects.filter(dataset=dataset)

    '''
    # TODO determine the current user
    # if it is the uploader of the dataset, THEN display button to Delete dataset
    # if the dataset is currently used by an ACTIVE competition then disable button and
    # add note below, "this dataset cannot currently be deleted as it is in use by an active competition"
    '''

    show_delete = False
    disable_delete = False
    '''
    SELECT host, start_date, end_date
    FROM competition co
    JOIN competitiondataset cd ON co.competition_id=cd.competition_id
    JOIN dataset da ON da.dataset_id=cd.dataset_id
    WHERE dataset = THIS.DATASET_ID

    if host == request.user.id:
        show_delete = True
    for each competitiondataset where competitiondataset.dataset_id=   
    '''
    
    if not competition_dataset.exists():
        return render(request, 'core/datasetView.html', {'dataset': dataset,
                                                         'show_delete':show_delete,
                                                         'disable_delete': disable_delete,
                                                         'page_title': dataset.name,
                                                         'description': dataset.description,
                                                         'banner_action': reverse('dataset_download', args=[dataset.dataset_id]),
                                                         'banner_button': 'Download this Dataset'})
    else:
        competition = []
        for row in competition_dataset:
            competition.append(get_object_or_404(
                Competition, competition_id=row.competition.competition_id))
        this_user = dataset.uploaded_by
        if this_user is not None:
            this_user = get_object_or_404(User, user_id=this_user.user_id)
        return render(request, 'core/datasetView.html', {'dataset': dataset,
                                                         'competition': competition,
                                                         'this_user': this_user,
                                                         'page_title': dataset.name,
                                                         'description': dataset.description,
                                                         'banner_action': reverse('dataset_download', args=[dataset.dataset_id]),
                                                         'banner_button': 'Download this Dataset'})

    # TODO display tiles of competitions where the dataset is being used along with start/end dates

@login_required
def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file from the form data
            file = request.FILES['file']
            # Use the original filename as the blob name
            filename = file.name
            # Upload the file to Azure Blob Storage
            try:
                connect_str = "DefaultEndpointsProtocol=https;AccountName=datadocketdev;AccountKey=U6wIRDwFi5bCudkB/nEdNGtcnAKRNIhz0U20N9VJZq7MmfWrEU60qYubtF1vN/srP8Txob2BGsMG+AStWEE8wQ==;EndpointSuffix=core.windows.net"
                container_name = 'container1'
                blob_service_client = BlobServiceClient.from_connection_string(connect_str)
                container_client = blob_service_client.get_container_client(container_name)
                # Check if a blob with the same name already exists
                if container_client.get_blob_client(filename).exists():
                    # If the blob already exists, add a timestamp to the filename
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"{timestamp}_{filename}"
                # Upload the file to Azure Blob Storage
                container_client.upload_blob(name=filename, data=file.read(), overwrite=True)
            except Exception as e:
                messages.error(request, 'Error uploading file: {}'.format(str(e)))
                return redirect('upload_dataset')
            # Create a Dataset object and save it to the database
            dataset = form.save(commit=False)
            dataset.file_uri = 'Dataset - {}'.format(filename)
            dataset.uploaded_by = User.objects.get(user_id = request.user.user_id)
            dataset.save()
            # messages.success(request, 'Dataset created successfully.')
            return redirect('dataset_detail', dataset_id=dataset.dataset_id)
        else:
            return render(request, 'core/datasetsForm.html', {'form': form})
    else:
        form = DatasetForm()
        return render(request, 'core/datasetsForm.html', {'form': form})


@login_required
def upload_solution(request, competition_id):
    comp = Competition.objects.filter(competition_id = competition_id)
    cont = Contestant.objects.filter(user_id = request.user.user_id,
                                      competition_id = competition_id)
    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            
         
            # Use the original filename as the blob name
           
            # Get the uploaded file from the form data
            file = request.FILES['file']
            filename = file.name
            # Upload the file to Azure Blob Storage
            try:
                connect_str = "DefaultEndpointsProtocol=https;AccountName=datadocketdev;AccountKey=U6wIRDwFi5bCudkB/nEdNGtcnAKRNIhz0U20N9VJZq7MmfWrEU60qYubtF1vN/srP8Txob2BGsMG+AStWEE8wQ==;EndpointSuffix=core.windows.net"
                container_name = 'container1'
                blob_service_client = BlobServiceClient.from_connection_string(
                    connect_str)
                container_client = blob_service_client.get_container_client(
                    container_name)
                container_client.upload_blob(
                    name=filename, data=file.read(), overwrite=True)
            except Exception as e:
                messages.error(
                    request, 'Error uploading file: {}'.format(str(e)))
                return redirect('upload_solution')
            # Create a CompetitionSolution object and save it to the database
            solution = form.save(commit=False)
            solution.competition = comp[0]
            solution.contestant = cont[0]
            solution.name = form.cleaned_data['name']
            solution.submission_uri = 'https://{}.blob.core.windows.net/{}/{}'.format(
            blob_service_client.account_name, container_name, filename)
            #solution.uploaded_by = User.objects.get(user_id = request.user.user_id)
            solution.save()
            # messages.success(request, 'Dataset created successfully.')
            return redirect('competition_detail', competition_id)
        else:
            return render(request, 'core/solutionsForm.html', {'form': form})
    else:
        form = SolutionForm()
        return render(request, 'core/solutionsForm.html', {'form': form,
                                                           'competition_id': competition_id})


@login_required
def dataset_update(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    if request.method == 'POST':
        dataset.name = request.POST.get('name')
        dataset.description = request.POST.get('description')
        dataset.file_uri = request.POST.get('file_uri')
        dataset.save()
        return redirect('dataset_detail', pk=dataset.pk)
    else:
        return render(request, 'dataset_form.html', {'dataset': dataset})
    
@login_required
def dataset_delete(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    userId=  dataset.uploaded_by.user_id
    dataset.delete()
    return redirect(reverse('profile', args=[userId]))



@login_required
def dataset_download(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    dataset.count_of_downloads += 1
    dataset.save()
    file_uri = dataset.file_uri

    response = HttpResponse()
    response['Content-Type'] = ''
    response['Content-Disposition'] = f'attachment; filename={file_uri}'
    response['X-Sendfile'] = file_uri
    return response


def rankings(request):
    users = User.objects.order_by('-rank')
    return render(request, 'core/ranking.html', {'users': users,
                                                 'page_title': 'Rankings',
                                                 'description': 'Check out the leaderboards!',
                                                 'banner_action': None,
                                                 'banner_button': ''})


def index(request):
    return render(request, 'core/index.html', {'page_title': 'Home',
                                     'description': 'Welcome to Datadocket',
                                     'banner_action': None,
                                     'banner_button': ''})

def update_competition(request, competition_id):
    
    competition = get_object_or_404(Competition, competition_id=competition_id)
    competition_dataset = CompetitionDataset.objects.filter(competition=competition_id)
   
    submittedcontestants =  CompetitionSolution.objects.filter(competition=competition_id)
    contestants = []
    for contestant in submittedcontestants:
        contestant_username = contestant.contestant.user.username
        submission_url =contestant.submission_uri
        contestant_id = contestant.contestant.contestant_id

        data = {
            'username': contestant_username,
            'submission_url': submission_url,
            'contestant_id': contestant_id,
            'competition_id' : competition_id

            
        }
        contestants.append((data))
    
    competition_form = CompetitionForm(initial={
    'competition_name': competition.name,
    'competition_description': competition.description,
    'competition_prize': competition.prize_amount,
    'categories': competition.category,
    'start_date': competition.start_date,
    'end_date': competition.end_date,
    'premium': competition.premium
    })
    # if true, then disable the competition's edit form
    is_started = False # true if we're on or past the start date/time
    if(competition.start_date.replace(tzinfo=timezone.utc) >= datetime.now(timezone.utc)):
        is_started=True

    # if true, then display the winners ranking section
    is_ended = False # true if we're on or past the end date/time
    if(competition.end_date.replace(tzinfo=timezone.utc) >= datetime.now(timezone.utc)):
        is_ended= True

    # if true, disable further ranking of the winners
    is_paid = False # true if the winners have been confirmed
    if(competition.winners_paid == True):
        is_paid = True

    

    print(competition.start_date.replace(tzinfo=timezone.utc))
    print(datetime.now(timezone.utc))
    return render(request, 'core/competitionManage.html', {
        'contestants': contestants,
        'competition': competition,
        'competition_dataset': competition_dataset,
        'competition_form': competition_form,
        'is_started' : is_started,
        'is_ended': is_ended,
        'is_paid': is_paid
    })

@login_required
def contestant_delete(request, contestant_id, competition_id):
    contestant = get_object_or_404(Contestant, pk=contestant_id)
    contestant.delete()
    competition = get_object_or_404(Competition, competition_id=competition_id)
    return redirect('update_competition', competition_id=competition.competition_id)



class SignUpView(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# HOME PAGE
def index(request):
  
    datasets_list = []
   # Get the last 15 datasets created
    datasets_list = Dataset.objects.order_by('created_date')[:15]
    
    # Get the last 15 competitions created
    competitions_list = Competition.objects.order_by('created_date')[:15]
    
    return render(request, 'core/index.html', { 'datasets_list': datasets_list,'competitions_list':competitions_list})

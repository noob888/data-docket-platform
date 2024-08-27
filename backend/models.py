from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, null=True)
    is_superadmin = models.BooleanField(default=False)
    rank = models.IntegerField(default=0)
    university = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)


class Competition(models.Model):
    competition_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    CATEGORY_CHOICES = [
        ('public', 'Public'),
        ('economic', 'Economic'),
        ('finance', 'Finance'),
        ('technology', 'Technology'),
        ('sports', 'Sports'),
        ('custom', 'Custom'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    prize_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, default='')
    rules = models.TextField(max_length=1000, default='')
    banner_uri = models.CharField(max_length=255, default="https://datadocketdev.blob.core.windows.net/container1/default_db_img.jpg")
    deliverable = models.BooleanField(default=False)
    visualization = models.BooleanField(default=False)
    guaranteed_submissions = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    live_presentations = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    winners_paid = models.BooleanField(default=False)



class Dataset(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    file_uri = models.CharField(max_length=255)
    banner_uri = models.CharField(max_length=255, default='https://datadocketdev.blob.core.windows.net/container1/default_db_img.jpg')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    count_of_downloads = models.IntegerField(default=0)

class Contestant(models.Model):
    contestant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    score = models.IntegerField()

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    
class CompetitionTag(models.Model):
    competition_tag_id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)


class CompetitionSolution(models.Model):
    competition_solution_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    submission_uri = models.CharField(max_length=500)


class CompetitionDataset(models.Model):
    competition_dataset_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
# Generated by Django 4.1.7 on 2023-03-14 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_premiumfeature_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competition',
            old_name='host_id',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='competitiondataset',
            old_name='competition_id',
            new_name='competition',
        ),
        migrations.RenameField(
            model_name='competitiondataset',
            old_name='dataset_id',
            new_name='dataset',
        ),
        migrations.RenameField(
            model_name='competitionfeature',
            old_name='competition_id',
            new_name='competition',
        ),
        migrations.RenameField(
            model_name='competitionfeature',
            old_name='premium_feature_id',
            new_name='premium_feature',
        ),
        migrations.RenameField(
            model_name='competitionsolution',
            old_name='competition_id',
            new_name='competition',
        ),
        migrations.RenameField(
            model_name='competitionsolution',
            old_name='contestant_id',
            new_name='contestant',
        ),
        migrations.RenameField(
            model_name='competitiontag',
            old_name='competition_id',
            new_name='competition',
        ),
        migrations.RenameField(
            model_name='competitiontag',
            old_name='tag_id',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='competition_id',
            new_name='competition',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='user_id',
            new_name='user',
        ),
    ]

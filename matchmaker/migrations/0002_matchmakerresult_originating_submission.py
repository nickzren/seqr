# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-04 20:55

from django.db import migrations, models
import django.db.models.deletion

from tqdm import tqdm

def set_originating_submissions(apps, schema_editor):
    MatchmakerSubmission = apps.get_model("matchmaker", "MatchmakerSubmission")
    MatchmakerResult = apps.get_model("matchmaker", "MatchmakerResult")
    db_alias = schema_editor.connection.alias
    submissions_by_id = {s.submission_id: s for s in MatchmakerSubmission.objects.using(db_alias).all()}
    local_results = MatchmakerResult.objects.using(db_alias).filter(result_data__patient__id__in=submissions_by_id)
    if local_results:
        print('Updating originating_submission for {} results'.format(len(local_results)))
        for result in tqdm(local_results, unit=' samples'):
            result.originating_submission = submissions_by_id[result.result_data['patient']['id']]
            result.save()


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchmakerresult',
            name='originating_submission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origin_results', to='matchmaker.MatchmakerSubmission'),
        ),
        migrations.RunPython(set_originating_submissions, reverse_code=migrations.RunPython.noop),
    ]

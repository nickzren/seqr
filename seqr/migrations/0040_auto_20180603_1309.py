# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-03 13:09
from __future__ import unicode_literals

from django.db import migrations, models


def transfer_info_from_dataset_to_sample_fields(apps, schema_editor):
    # for cases where a sample is attached to multiple datasets (for example both VARIANTS and read alignments),
    # then use the existing Sample record to store metadata from the most recent VARIANTS Dataset, and use
    # update_projects_in_new_schema to create the additional Sample records for read alignments.
    # This is because Django doesn't currently support creating new records inside a RunPython migration.
    Dataset = apps.get_model('seqr', 'Dataset')
    Sample = apps.get_model('seqr', 'Sample')

    print("\nTransferring metadata from {0} Dataset records to {1} Sample records".format(
        Dataset.objects.filter(analysis_type="VARIANTS").count(),
        Sample.objects.count(),
        ))

    for sample in Sample.objects.all():
        dataset = sample.dataset_set.filter(analysis_type="VARIANTS").order_by('-loaded_date', '-pk').first()
        if dataset:
            sample.dataset_file_path = dataset.source_file_path
            sample.dataset_type = dataset.analysis_type
            sample.elasticsearch_index = dataset.dataset_id
            sample.loaded_date = dataset.loaded_date
            sample.sample_status = "loaded" if dataset.is_loaded else None
            sample.save()


class Migration(migrations.Migration):

    dependencies = [
        ('seqr', '0039_merge_20180531_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='genome_version',
            field=models.CharField(choices=[(b'37', b'GRCh37'), (b'38', b'GRCh38')], default=b'37', max_length=5),
        ),
        migrations.AddField(
            model_name='sample',
            name='dataset_file_path',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='dataset_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='dataset_type',
            field=models.CharField(blank=True, choices=[(b'ALIGN', b'Alignment'), (b'VARIANTS', b'Variant Calls'), (b'SV', b'SV Calls'), (b'BREAK', b'Breakpoints'), (b'SPLICE', b'Splice Junction Calls'), (b'ASE', b'Allele Specific Expression')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='elasticsearch_index',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='loaded_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_status',
            field=models.CharField(blank=True, choices=[(b'seq', b'In Sequencing'), (b'seq_done', b'Completed Sequencing'), (b'seq_fail_1', b'Failed Sequencing - Abandoned'), (b'loading', b'Loading'), (b'loaded', b'Loaded')], db_index=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_type',
            field=models.CharField(blank=True, choices=[(b'WES', b'Exome'), (b'WGS', b'Whole Genome'), (b'RNA', b'RNA'), (b'ARRAY', b'ARRAY')], max_length=20, null=True),
        ),

        migrations.RunPython(transfer_info_from_dataset_to_sample_fields),

        migrations.RemoveField(
            model_name='dataset',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='project',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='samples',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='deprecated_base_project',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='is_external_data',
        ),
        migrations.DeleteModel(
            name='Dataset',
        ),
    ]

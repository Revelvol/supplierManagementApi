# Generated by Django 4.1.6 on 2023-02-14 04:27

import base.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_ingredientdocument_allergendocument_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientdocument',
            name='allergenDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='ingredientdocument',
            name='coaDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='ingredientdocument',
            name='gmoDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='ingredientdocument',
            name='halalDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='ingredientdocument',
            name='isoDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='ingredientdocument',
            name='kosherDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='ingredientdocument',
            name='msdsDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='ingredientdocument',
            name='tdsDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_ingredient_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='supplierdocument',
            name='gmpDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_supplier_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='supplierdocument',
            name='haccpDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_supplier_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
        migrations.AlterField(
            model_name='supplierdocument',
            name='isoDocument',
            field=models.FileField(blank=True, null=True, upload_to=base.models.get_supplier_doc_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]),
        ),
    ]

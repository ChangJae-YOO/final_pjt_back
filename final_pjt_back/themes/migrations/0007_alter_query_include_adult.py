# Generated by Django 3.2.12 on 2023-05-19 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0006_alter_query_include_adult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='include_adult',
            field=models.CharField(max_length=10, null=True),
        ),
    ]

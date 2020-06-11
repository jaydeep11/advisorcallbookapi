# Generated by Django 2.1.7 on 2020-06-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200611_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advisor_name', models.CharField(default='name', max_length=255)),
                ('advisor_photo_url', models.ImageField(blank=True, max_length=255, null=True, upload_to='pictures/%Y/%m/%d/')),
            ],
        ),
    ]
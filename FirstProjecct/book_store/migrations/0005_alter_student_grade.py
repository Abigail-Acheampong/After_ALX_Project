# Generated by Django 5.1.6 on 2025-05-01 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_store', '0004_fee_student_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.IntegerField(choices=[(1, 'Grade 1'), (2, 'Grade 2'), (3, 'Grade 3'), (4, 'Grade 4'), (5, 'Grade 5'), (6, 'Grade 6'), (7, 'Grade 7'), (8, 'Grade 8')]),
        ),
    ]

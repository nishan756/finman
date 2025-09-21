import django.utils.timezone
import django_summernote.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('small_name', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('roll', models.PositiveIntegerField(unique=True)),
                ('semester', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th'), ('Ex', 'Ex')], max_length=4)),
                ('shift', models.CharField(blank=True, choices=[('1st', '1st'), ('2nd', '2nd')], max_length=4, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact', models.CharField(max_length=11, unique=True)),
                ('joined_at', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-joined_at'],
            },
        ),
        migrations.CreateModel(
            name='MemberTransactionDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.PositiveIntegerField()),
                ('account_no', models.CharField(max_length=30)),
                ('transaction_id', models.CharField(max_length=20, unique=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('took_loan', models.BooleanField(default=False)),
                ('due', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('detail', django_summernote.fields.SummernoteTextField(blank=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PaymentContext',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('start_date', models.DateTimeField(verbose_name='Started from')),
                ('end_date', models.DateTimeField(verbose_name='End on')),
                ('amount', models.PositiveIntegerField()),
                ('detail', django_summernote.fields.SummernoteTextField(blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('posted_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'ordering': ['-posted_at'],
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('Income', 'Income'), ('Expense', 'Expense')], max_length=9, verbose_name='Transaction Type')),
                ('title', models.CharField(max_length=300)),
                ('detail', django_summernote.fields.SummernoteTextField(blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]

# Generated by Django 4.1.5 on 2023-02-24 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auctionlisting_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='category',
        ),
        migrations.RemoveField(
            model_name='auctionlisting',
            name='created',
        ),
        migrations.RemoveField(
            model_name='auctionlisting',
            name='image',
        ),
        migrations.RemoveField(
            model_name='auctionlisting',
            name='listedBy',
        ),
        migrations.RemoveField(
            model_name='auctionlisting',
            name='modified',
        ),
    ]
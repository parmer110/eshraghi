# Generated by Django 4.1.5 on 2023-02-27 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0030_remove_auctionlisting_startingbid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='currentBid',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='startingBid',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

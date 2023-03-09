# Generated by Django 4.1.5 on 2023-02-25 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_remove_auctionlisting_bidstarting_bids_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='startingBid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='startingBid', to='auctions.bids'),
        ),
    ]
# Generated by Django 4.1.5 on 2023-02-28 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_alter_auctionlisting_startingbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='startingBid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startingPrice', to='auctions.bids'),
        ),
    ]
from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.
# 
class CardInfo(models.Model):
    card_name = models.CharField(max_length=100)
    card_set = models.CharField(max_length=10)
    rarity = models.CharField(max_length=10)
    user = models.CharField(max_length=50,default='')
    card_link = models.CharField(max_length=200,default='')
    card_image_link = models.CharField(max_length=200,default='')
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)    

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % str(self.card_name)

class CardPrice(models.Model):
    card_id = models.CharField(max_length=100)
    card_price = models.FloatField(default=0.0)
    post_date = models.CharField(max_length=10)
    user = models.CharField(max_length=50,default='')
    decks = models.IntegerField(default=0)
    standard = models.IntegerField(default=0)
    modern = models.IntegerField(default=0)
    legacy = models.IntegerField(default=0)
    vintage = models.IntegerField(default=0)
    commander = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)    

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % str(self.id)

class CardCollect(models.Model):
    Investment = 'Investment'
    Battle = 'Battle'
    Usege = (
        (Investment, 'Investment'),
        (Battle, 'Battle'),
    )

    usege = models.CharField(
        max_length=20,
        choices=Usege,
        #default=STANDARD,
    )
    card_name = models.CharField(max_length=100)
    card_set = models.CharField(max_length=10)
    quantity = models.IntegerField()
    cost = models.FloatField()
    current = models.FloatField(default=0.0)
    profit = models.FloatField(default=0.0)
    percent = models.FloatField(default=0.0)
    daily = models.FloatField(default=0.0)
    weekly = models.FloatField(default=0.0)
    user = models.CharField(max_length=50,default='')
    card_link = models.CharField(max_length=200,default='')
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)    

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % str(self.card_name)

class CardHistroy(models.Model):
    Investment = 'Investment'
    Battle = 'Battle'
    Usege = (
        (Investment, 'Investment'),
        (Battle, 'Battle'),
    )

    usege = models.CharField(
        max_length=20,
        choices=Usege,
        #default=STANDARD,
    )
    card_name = models.CharField(max_length=100)
    card_set = models.CharField(max_length=10)
    quantity = models.IntegerField()
    cost = models.FloatField(default=0.0)
    current = models.FloatField()
    profit = models.FloatField()
    percent = models.FloatField()
    user = models.CharField(max_length=50,default='')
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)    

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % str(self.id)

class CardCollectForm(ModelForm):
    class Meta:
        model = CardCollect
        fields = ['usege','card_name','card_set','quantity','cost']

class CardHistroyForm(ModelForm):
    class Meta:
        model = CardHistroy
        fields = ['card_name','card_set','quantity','current']
        fields = ['quantity','current']
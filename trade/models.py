from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.
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
from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.
class ConstructLeague(models.Model):
    STANDARD = 'Standard'
    MODERN = 'Modern'
    PAUPER = 'Pauper'
    LEGACY = 'Legacy'
    COMMANDER = 'Commander'
    Construct_LEAGUE = (
        (STANDARD, 'Standard'),
        (MODERN, 'Modern'),
        (PAUPER, 'Pauper'),
        (LEGACY, 'Legacy'),
        (COMMANDER, 'Commander'),
    )

    #league_format = models.CharField(max_length=50)
    #
    FRIENDLY = 'Friendly'
    COMPETITIVE = 'Competitive'
    Construct_LEAGUE_Type = (
        (FRIENDLY, 'Friendly'),
        (COMPETITIVE, 'Competitive'),
    )

    league_format = models.CharField(
        max_length=20,
        choices=Construct_LEAGUE,
        #default=STANDARD,
    )
    league_type = models.CharField(max_length=20,
                                   choices=Construct_LEAGUE_Type)
    deck = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    profit = models.FloatField(default=0.0)
    finish = models.BooleanField(default=False)
    result = models.CharField(max_length=10,default='')
    during = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    #during123 = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)    

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % str(self.id)

class ConstructGame(models.Model):
    WIN = 'Win'
    LOSE = 'Lose'
    RESULT = (
        (WIN, 'Win'),
        (LOSE, 'Lose'),
    )
    

    lg_id = models.CharField(max_length=10)
    opp_deck = models.CharField(max_length=50)
    during = models.IntegerField()
    game_result = models.CharField(
        max_length=10,
        choices=RESULT,
        #default=STANDARD,
    )
    user = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)    

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % str(self.id)

class ConstructLeagueForm(ModelForm):
    class Meta:
        model = ConstructLeague
        fields = ['league_format','league_type','deck']

class ConstructGameForm(ModelForm):
    class Meta:
        model = ConstructGame
        fields = ['opp_deck','game_result','during']

class BonusForm(forms.Form):
    chest_num = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Treasure Chest Quantity'}))
    chest_price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Treasure Chest Price'}))
    play_point = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Play Point'}))

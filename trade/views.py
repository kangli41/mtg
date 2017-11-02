from django.shortcuts import render
from django.http import HttpResponse
from .models import CardCollect,CardCollectForm,CardHistroy,CardHistroyForm
import datetime
import time
import urllib.request
import re
import sys
import json
import os
import threading
# Create your views here.
def make_url(card_name,set_name,set_dir):
    for key in set_dir:
        if key == set_name:
            set_name = set_dir[set_name]
            break
    card_name = card_name.replace(',','')
    card_name = card_name.replace("'","")
    if card_name.find(' (F)') == -1 :
        card_name = card_name.replace(' ','+') 
        url = 'http://www.mtggoldfish.com/price/' + set_name + '/' + card_name + '#online'
    else:
        card_name = card_name.replace(' (F)','') 
        card_name = card_name.replace(' ','+') 
        url = 'http://www.mtggoldfish.com/price/' + set_name + ':Foil/' + card_name + '#online'
    print(url) 
    return url   

def get_html(card_name,set_name,set_dir):
    #response = urllib2.urlopen(url)  
    url = make_url(card_name,set_name,set_dir)
    response = urllib.request.urlopen(url)
    html = response.read().decode()
    return html

def request_price(html): 
    #make_url(card_name,set_name)   
    find_price_flag = 0
    price_key = r".*<div class='price-box-price'>(.+)</div>"
    type_key = r".*<div class='price-box-type'>(\D+)</div>"
    for line in html.split("\n"):
        if find_price_flag:
            price_match = re.match(price_key , line)
            if price_match:
                #print('price = ' , price_match.group(1))
                find_price_flag = 0
                return price_match.group(1)
        type_match = re.match(type_key , line)  
        if type_match:
            #print type_match.group(1)
            if type_match.group(1) == 'ONLINE':
                find_price_flag = 1

def request_change(html):
    find_change_flag = 0
    find_dchange_flag = 0
    find_wchange_flag = 0
    stats_match = r"<div class='price-card-statistics-online' style='display:none;'>"
    dchange_match = r"<td>Daily Change</td>"
    wchange_match = r"<td>Weekly Change</td>"
    change_match_re = r"<td class='text-right'.*>(.+)</span></td>"
    change_match_re2 = r"<td class='text-right'.*>(.+)</td>"
    for line in html.split("\n"):
        if stats_match == line:
            find_change_flag = 1
        if find_change_flag:
            #print(line)
            if dchange_match == line:
                find_dchange_flag = 1
            if wchange_match == line:
                find_wchange_flag = 1
            if find_dchange_flag:
                dchange_match = re.match(change_match_re , line)
                if dchange_match:
                    dchange = dchange_match.group(1)
                    #print(dchange)
                    find_dchange_flag = 0
            if find_wchange_flag:
                wchange_match = re.match(change_match_re , line)
                if wchange_match:
                    wchange = wchange_match.group(1)
                    #print(wchange)
                    break
                else:
                    wchange_match2 = re.match(change_match_re2 , line)
                    if wchange_match2:
                        wchange = wchange_match2.group(1)
                        #print(wchange)
                        break
    result = [dchange,wchange]                
    return result

def home(request):    
    form = CardCollectForm(request.POST or None)
    form_sell = CardHistroyForm(request.POST or None)
    const_lg = CardCollect.objects.filter(user='kangli')
    print(const_lg)
    total_tix = 0
    total_cost = 0
    for coll in const_lg:
        total_tix += coll.quantity * coll.current
        total_cost += coll.quantity * coll.cost
    total_tix = "%.2f" % total_tix

    context = {'form':form ,
               'form_sell':form_sell,
               'const_lg':const_lg,
               'total_tix':total_tix,
               'total_cost':total_cost
               }
    if form.is_valid():
        #
        #form.user = 'kangli'
        #print(form.cleaned_data)
        a = form.save(commit=False)
        a.user = 'kangli'
        found = False
        for card in const_lg:
            if card.card_name == a.card_name and card.card_set == a.card_set:
                card.cost = (a.cost * a.quantity + card.cost * card.quantity) / (a.quantity + card.quantity)
                card.quantity += a.quantity
                card.cost = float("%.2f" % card.cost)
                card.save()
                found = True
        if found == False:
            a.save()
        #form.save()
        #mailto = form.cleaned_data.get('mailto')
        #resp = genjob_form(form)
        return render(request,'trade_home.html',context)    

    if form_sell.is_valid():
        #
        #form.user = 'kangli'
        #print(form.cleaned_data)
        a = form_sell.save(commit=False)
        a.user = 'kangli'
        found = False
        for card in const_lg:
            if card.card_name == a.card_name and card.card_set == a.card_set:
                a.profit = (a.current - card.cost) * a.quantity
                a.percent = (a.current - card.cost) / card.cost
                left = card.quantity - a.quantity
                a.usege = card.usege
                a.cost = card.cost
                if left <= 0:
                    card.delete()
                else:
                    card.quantity = left
                    card.save()
                a.save()
                return render(request,'trade_home.html',context) 
        #form.save()
        #mailto = form.cleaned_data.get('mailto')
        #resp = genjob_form(form)
        return HttpResponse('can not find card') 
    
    return render(request,'trade_home.html',context)

def card_update(request):
    
    card_list = CardCollect.objects.filter(user='kangli')
    print(card_list)
    set_dir = {}
    with open('/Users/kangli/Personal/game/Magic/set_dictionary') as f:
        for line in f:
            subline = line.split(" ")
            set_key = subline[-1].strip("\r\n")
            set_key = set_key.upper()
            subpop = subline.pop(-1)
            set_value = ''
            for value_line in subline:
                if value_line == subline[0]:
                    set_value = value_line
                else:
                    set_value = set_value + '+' + value_line
            #print(set_key,set_value)
            set_dir[set_key] = set_value
    #print(set_dir)
    #
    for card in card_list:
        html = get_html(card.card_name,card.card_set,set_dir)
        #change = request_change(html)
        print(float(request_price(html)))
        card.current = float(request_price(html))
        change = request_change(html)
        card.daily = change[0]
        card.weekly = change[1]
        card.profit = card.current - card.cost
        card.percent = card.profit / card.cost * 100
        card.profit = "%.2f" % card.profit
        card.percent = "%.2f" % card.percent
        card.save()
    res = 'Success'
    return HttpResponse(res)


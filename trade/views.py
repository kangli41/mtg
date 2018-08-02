from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import CardCollect,CardCollectForm,CardHistroy,CardHistroyForm ,CardInfo,CardPrice
import datetime
import time
import urllib.request
import re
import sys
import json
import os
import threading
from bs4 import BeautifulSoup
from datetime import date

# Create your views here.
# 
# 

#T2_SET = ['XLN','HOU','AKH','AER','KLD']
T2_SET = ['HOU','AKH','AER','KLD']
RARITY_LIST = ['Mythic','Rare']


SET_DIR = {}
with open('/home/kangli/mtg/set_dictionary') as f:
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
        SET_DIR[set_key] = set_value

def str_to_date(str_date):
    date_arr = str_date.split('-')
    return date(date_arr[0],date_arr[1],date_arr[2])

def make_url(card_name,set_name,set_dir):
    for key in set_dir:
        if key == set_name:
            set_name = set_dir[set_name]
            break
    card_name = card_name.replace(',','')
    card_name = card_name.replace("'","")
    card_name = card_name.replace(" // "," ")
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

@login_required(login_url='/admin/login/')
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
                a.percent = a.profit * 100
                left = card.quantity - a.quantity
                a.usege = card.usege
                a.cost = card.cost
                a.profit = "%.2f" % a.profit
                a.percent = "%.2f" % a.percent
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

def card_sell(request,card_id):    
    form = CardCollectForm(request.POST or None)
    form_sell = CardHistroyForm(request.POST or None)
    const_lg = CardCollect.objects.filter(id=card_id)
    print(const_lg)

    context = {'form':form ,
               'form_sell':form_sell,
               'const_lg':const_lg,
               }
    if form_sell.is_valid():
        #
        #form.user = 'kangli'
        #print(form.cleaned_data)
        a = form_sell.save(commit=False)
        a.user = 'kangli'
        found = False
        for card in const_lg:
            a.profit = (a.current - card.cost) * a.quantity
            a.percent = (a.current - card.cost) / card.cost 
            a.percent = a.percent * 100
            left = card.quantity - a.quantity
            a.usege = card.usege
            a.cost = card.cost
            a.profit = "%.2f" % a.profit
            a.percent = "%.2f" % a.percent
            a.card_name = card.card_name
            a.card_set = card.card_set
            if left <= 0:
                card.delete()
            else:
                card.quantity = left
                card.save()
            a.save()
            return render(request,'trade_sell_succuess.html',context) 
        #form.save()
        #mailto = form.cleaned_data.get('mailto')
        #resp = genjob_form(form)
        return HttpResponse('can not find card') 
    
    return render(request,'trade_sell.html',context)

def card_update(request):
    
    card_list = CardCollect.objects.filter(user='kangli')
    print(card_list)
    
    #print(set_dir)
    #
    for card in card_list:
        html = get_html(card.card_name,card.card_set,SET_DIR)
        card.card_link = make_url(card.card_name,card.card_set,SET_DIR)
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

@login_required(login_url='/admin/login/')
def trade_history(request):

    trade_list = CardHistroy.objects.all()
    total_tix = 0
    for coll in trade_list:
        total_tix += coll.profit
        #total_cost += coll.quantity * coll.cost
    total_tix = float("%.2f" % total_tix)

    print(trade_list)
    context = {'lg_list':trade_list, 
    'total_tix':total_tix,  
               }   
    return render(request,'trade_history.html',context)  

def card_scrubber(request):
    
    for card_set in T2_SET:
        url = 'https://www.mtggoldfish.com/index/'+card_set+'#online'
        response = urllib.request.urlopen(url)
        html = response.read().decode()
        #print('########################'*10)
        #print(html)
        #print('########################'*10)
        soup = BeautifulSoup(html)
        set_price = soup.td.div.div.text
        #print(set_price)
        i = 0
        for card_info in soup.find_all('td','card'):
            #print(card_info.parent.find_all('td'))
            card_name = card_info.text
            print(card_info.a)
            card_price = card_info.parent.find_all('td')[3].get_text(strip=True)
            card_image = card_info.a.get('data-full-image')
            card_rarity = card_info.parent.find_all('td')[2].get_text(strip=True)
            if card_rarity in RARITY_LIST:
                search_result = CardInfo.objects.filter(card_name=card_name)
                url1 = make_url(card_name,card_set,SET_DIR)
                #print(search_result)
                #print(len(search_result))
                if len(search_result) == 0:
                    new_card = CardInfo.objects.create(card_name=card_name)
                    new_card.card_link = url1
                    new_card.card_image_link = card_image
                    new_card.rarity = card_rarity
                    new_card.card_set = card_set
                    new_card.save()
                    #print(make_url(card_name,card_set,SET_DIR))
                response1 = urllib.request.urlopen(url1)
                html1 = response1.read().decode()
                soup1 = BeautifulSoup(html1)
                #price_history_list = soup1.find_all('script')[8].get_text(strip=True).split('\n')
                #print(html1)
                use_deck = soup1.find_all('div','price-card-recent-decks')[0].find_all('td','col-num-decks')
                use_format = soup1.find_all('div','price-card-recent-decks')[0].find_all('td','col-format')
                standard = 0
                modern = 0
                legacy = 0
                vintage = 0
                commander =0
                deck = 0
                for i in range(len(use_deck)-1):
                    if use_format[i].text == 'standard':
                        standard += int(use_deck[i].text)
                    elif use_format[i].text == 'modern':
                        modern += int(use_deck[i].text)
                    elif use_format[i].text == 'legacy':
                        legacy += int(use_deck[i].text)
                    elif use_format[i].text == 'vintage':
                        vintage += int(use_deck[i].text)
                    else:
                        deck += int(use_deck[i].text)
                found = False
                for price_history_list in soup1.find_all('script'):
                    for line in price_history_list.get_text(strip=True).split('\n'):
                        # print('1')
                        # print(line)
                        if '$(".price-sources-paper").toggle(false);' in line:
                            #print('2')
                            found = True
                        if found == True:
                            if 'd +=' in line:
                                value = line.split(',')
                                #print(value)
                                post_date = value[0].split('d += "\\n')[1][:10]
                                #print(post_date)
                                price = value[1].strip().split('"')[0]
                                #print(price)
                                card_id = CardInfo.objects.filter(card_name=card_name)
                                #print(card_id[0].id)
                                cp = CardPrice.objects.filter(card_id=str(card_id[0].id)).filter(post_date=post_date)
                                if len(cp) == 0:
                                    new_cp = CardPrice.objects.create(card_id=str(card_id[0].id))
                                    new_cp.post_date = post_date
                                    new_cp.card_price = price
                                    if post_date == '2017-11-14':
                                        new_cp.standard = standard
                                        new_cp.modern = modern
                                        new_cp.legacy = legacy
                                        new_cp.vintage = vintage
                                        new_cp.deck = deck
                                    new_cp.save()
                
                                #i+=1
                                #print(i)
                #break

        #print(soup.prettify())
    #print(set_dir)
    #
    # for card in card_list:
    #     html = get_html(card.card_name,card.card_set,set_dir)
    #     card.card_link = make_url(card.card_name,card.card_set,set_dir)
    #     #change = request_change(html)
    #     print(float(request_price(html)))
    #     card.current = float(request_price(html))
    #     change = request_change(html)
    #     card.daily = change[0]
    #     card.weekly = change[1]
    #     card.profit = card.current - card.cost
    #     card.percent = card.profit / card.cost * 100
    #     card.profit = "%.2f" % card.profit
    #     card.percent = "%.2f" % card.percent
    #     card.save()
    res = 'Success'
    return HttpResponse(res)

def card_analysis(request):
    card_list = CardInfo.objects.all()
    mythic_list = []
    rare_list = []
    for card in card_list:
        cp = CardPrice.objects.filter(card_id=str(card.id)).last()
        deck = cp.standard+cp.modern+cp.vintage+cp.legacy
        if card.rarity == 'Mythic':
            mythic_list.append([card.card_name,cp.card_price,deck])
        else:
            rare_list.append([card.card_name,cp.card_price,deck])
    #print(card.card_name+' '+str(cp.card_price)+' '+str(deck))
    print(mythic_list)

    res = 'Success'
    return HttpResponse(res)

def card_wave(request):
    card_list = CardInfo.objects.all()
    mythic_list = []
    rare_list = []
    for card in card_list:
        cp_list = CardPrice.objects.filter(card_id=str(card.id))
        deck = cp.standard+cp.modern+cp.vintage+cp.legacy
        if card.rarity == 'Mythic':
            mythic_list.append([card.card_name,cp.card_price,deck])
        else:
            rare_list.append([card.card_name,cp.card_price,deck])
    #print(card.card_name+' '+str(cp.card_price)+' '+str(deck))
    print(mythic_list)

    res = 'Success'
    return HttpResponse(res)

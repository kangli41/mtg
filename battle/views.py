from django.shortcuts import render
from .models import ConstructLeagueForm,ConstructLeague,ConstructGameForm,ConstructGame,BonusForm
from django.contrib.auth.decorators import login_required

def get_card_info(card,card_set):
    html = get_html(card,card_set)
    #change = request_change(html)
    return float(request_price(html))

LG_TYPE = ['Friendly','Competitive']
LG_FORMAT = ['Standard','Modern','Pauper','Legacy','Commander']

# Create your views here.
@login_required(login_url='/admin/login/')
def home(request):
    
    form = ConstructLeagueForm(request.POST or None)
    const_lg = ConstructLeague.objects.filter(user='kangli')
    print(const_lg)


    context = {'form':form ,
               'const_lg':const_lg           
               }
    if form.is_valid():
        #
        #form.user = 'kangli'
        #print(form.cleaned_data)
        a = form.save(commit=False)
        a.user = 'kangli'
        a.save()
        #form.save()
        #mailto = form.cleaned_data.get('mailto')
        #resp = genjob_form(form)
        return render(request,'battle_home.html',context)    
    

    #print(context)      
    
    return render(request,'battle_home.html',context)

@login_required(login_url='/admin/login/')
def league_detail(request,id):
    form = ConstructGameForm(request.POST or None)
    form_finish = BonusForm(request.POST or None)
    const_game = ConstructGame.objects.filter(lg_id=id).filter(user='kangli')


    context = {'form':form,   
               'form_finish':form_finish,
               'const_game':const_game,
               "lg_id":id}      

    if form.is_valid():
        #
        #form.user = 'kangli'
        #print(form.cleaned_data)
        a = form.save(commit=False)
        a.lg_id = id
        a.user = 'kangli'
        a.save()
        #form.save()
        #mailto = form.cleaned_data.get('mailto')
        #resp = genjob_form(form)
        return render(request,'battle_lg_detail.html',context)    

    if form_finish.is_valid():
        #
        #form.user = 'kangli'
        print(form_finish.cleaned_data)
        const_lg = ConstructLeague.objects.filter(user='kangli').get(id=id)
        if const_lg.league_type == 'Friendly':
            entry_fee = 8
        else:
            entry_fee = 12
        const_lg.finish = True
        profit = form_finish.cleaned_data.get('chest_num') * form_finish.cleaned_data.get('chest_price') + form_finish.cleaned_data.get('play_point')/10 - entry_fee
        profit = "%.2f" % profit
        const_lg.profit = profit
        during = 0 
        win_str = 0
        lose_str = 0
        for game in const_game:
            during = during + game.during
            if game.game_result == 'Win':
                win_str +=1
            else:
                lose_str +=1
        result_st = str(win_str) + '-' + str(lose_str)
        const_lg.during = during
        const_lg.result = result_st
        const_lg.win = win_str
        const_lg.lose = lose_str
        const_lg.save()
        #form.save()
        #mailto = form.cleaned_data.get('mailto')
        #resp = genjob_form(form)
        return render(request,'battle_lg_detail.html',context)    

    return render(request,'battle_lg_detail.html',context)

@login_required(login_url='/admin/login/')
def battle_history(request):
    
    #form = ConstructLeagueForm(request.POST or None)
    #
    #
    lg_list = []
    for lg_f in LG_FORMAT:
        for lg_t in LG_TYPE:
            const_lg = ConstructLeague.objects.filter(user='kangli').filter(finish=True).filter(league_format=lg_f).filter(league_type=lg_t).values('deck')
            if len(const_lg) > 0 : 
                f_list = []
                for f in const_lg:
                    f_list.append(f['deck'])
                d_list = set(f_list)
                for de in d_list:
                    const_lg1 = ConstructLeague.objects.filter(user='kangli').filter(finish=True).filter(league_format=lg_f).filter(league_type=lg_t).filter(deck=de)
                    if len(const_lg1) > 0 : 
                        dic_de = {'league_format':lg_f,
                                  'league_type':lg_t,
                                  'deck':de,
                                  'lg_num':0,
                                  'profit':0.0,
                                  'during':0,
                                  'profit_game':0.0,
                                  'profit_hour':0.0,
                                  'minutes_lg':0,
                                  'win':0,
                                  'lose':0,
                                  'id_list':[]
                                  }
                        for lg1 in const_lg1:
                            dic_de['lg_num'] += 1
                            dic_de['profit'] += lg1.profit
                            dic_de['win'] += lg1.win
                            dic_de['lose'] += lg1.lose
                            dic_de['during'] += lg1.during
                            dic_de['id_list'].append(lg1.id)
                        dic_de['profit_game'] = dic_de['profit'] / dic_de['lg_num']
                        dic_de['profit_hour'] = dic_de['profit'] / dic_de['during'] * 60
                        dic_de['minutes_lg'] = dic_de['during'] / dic_de['lg_num']
                        dic_de['profit_game'] = "%.2f" % dic_de['profit_game']
                        dic_de['profit_hour'] = "%.2f" %dic_de['profit_hour']
                        dic_de['minutes_game'] = dic_de['during'] / (dic_de['win'] + dic_de['lose'])
                        dic_de['minutes_game'] = "%.2f" %dic_de['minutes_game']
                        dic_de['minutes_lg'] = "%.2f" %dic_de['minutes_lg'] 
                        dic_de['profit'] = "%.2f"%dic_de['profit']
                        dic_de['id'] = dic_de['id_list'][0]
                        dic_de['rate'] = dic_de['win']/(dic_de['win']+dic_de['lose']) *100
                        dic_de['rate'] = '%.2f'%dic_de['rate']
                        dic_de['rate'] = float(dic_de['rate'])
                        lg_list.append(dic_de)
    print(lg_list)
    context = {'lg_list':lg_list,   
               }   
    return render(request,'battle_history.html',context)  

@login_required(login_url='/admin/login/')
def battle_history_detail(request,id):
    
    #form = ConstructLeagueForm(request.POST or None)
    #
    #
    
    const_lg = ConstructLeague.objects.filter(user='kangli').filter(id=id)
    if len(const_lg) > 0:
        #print(const_lg)
        lg_f = const_lg[0].league_format
        lg_t = const_lg[0].league_type
        de = const_lg[0].deck
    const_lg1 = ConstructLeague.objects.filter(user='kangli').filter(league_format=lg_f).filter(league_type=lg_t).filter(deck=de).filter(finish=True)
    if len(const_lg1) > 0 : 
        dic_de = {'league_format':lg_f,
                  'league_type':lg_t,
                  'deck':de,
                  'lg_num':0,
                  'profit':0.0,
                  'during':0,
                  'profit_game':0.0,
                  'profit_hour':0.0,
                  'minutes_lg':0,
                  'win':0,
                  'lose':0,
                  'id_list':[]
                  }
        for lg1 in const_lg1:
            dic_de['lg_num'] += 1
            dic_de['profit'] += lg1.profit
            dic_de['during'] += lg1.during
            dic_de['win'] += lg1.win
            dic_de['lose'] += lg1.lose
            dic_de['id_list'].append(lg1.id)
        dic_de['profit_game'] = dic_de['profit'] / dic_de['lg_num']
        dic_de['profit_hour'] = dic_de['profit'] / dic_de['during'] * 60
        dic_de['minutes_lg'] = dic_de['during'] / dic_de['lg_num']
        dic_de['win_pct'] = dic_de['win'] / (dic_de['win'] + dic_de['lose']) *100
        dic_de['win_pct_str'] = "%.2f" %dic_de['win_pct'] +'%'
        dic_de['profit_game'] = float("%.2f" % dic_de['profit_game'])
        dic_de['profit_hour'] = float("%.2f" %dic_de['profit_hour'])
        dic_de['minutes_lg'] = "%.2f" %dic_de['minutes_lg'] 
        dic_de['profit'] = float("%.2f"%dic_de['profit'])
        dic_de['id'] = dic_de['id_list'][0]
    
    const_game_list = []
    meta_list = []
    for id in dic_de['id_list']:
        const_game = ConstructGame.objects.filter(lg_id=id).filter(user='kangli')
        for game in const_game:
            const_game_list.append(game) 
    
    #print(const_game_list)
    game_total = len(const_game_list)
    opp_list = []
    for const_game in const_game_list:
        opp_list.append(const_game.opp_deck)
    opp_list = set(opp_list)
    #print(opp_list)
    for opp in opp_list:
        meta_d = {}
        meta_d['opp_deck'] = opp
        meta_d['Win'] = 0
        meta_d['Lose'] = 0
        meta_d['During'] = 0
        for const_game in const_game_list:
            if opp == const_game.opp_deck:
                if const_game.game_result == 'Win':
                    meta_d['Win'] += 1
                else:
                    meta_d['Lose'] += 1
                meta_d['During'] += const_game.during
        meta_d['During_game'] = meta_d['During'] / (meta_d['Win'] + meta_d['Lose'])
        meta_d['During_game'] = '%.2f'%meta_d['During_game']
        meta_d['win_pct'] = meta_d['Win'] / (meta_d['Win'] + meta_d['Lose']) * 100 
        meta_d['win_pct_str'] = '%.2f'%meta_d['win_pct'] + '%'
        meta_d['cnt'] = meta_d['Win'] + meta_d['Lose']
        meta_d['cnt_pct'] = meta_d['cnt'] / game_total * 100
        meta_d['cnt_pct_str'] = '%.2f'%meta_d['cnt_pct'] + '%'
        meta_list.append(meta_d)
    

    
    #print(meta_list)

    context = {'dic_de':dic_de,
               'const_lg':const_lg1,
               'meta_list':meta_list   
               }  

    return render(request,'battle_history_detail.html',context)  

@login_required(login_url='/admin/login/')
def trade_home(request):
    
    form = CardCollectForm(request.POST or None)
    const_lg = CardCollect.objects.filter(user='kangli')
    print(const_lg)


    context = {'form':form ,
               'const_lg':const_lg           
               }
    if form.is_valid():
        #
        #form.user = 'kangli'
        #print(form.cleaned_data)
        a = form.save(commit=False)
        a.user = 'kangli'
        a.save()
        #form.save()
        #mailto = form.cleaned_data.get('mailto')
        #resp = genjob_form(form)
        return render(request,'battle_home.html',context)    
    

    #print(context)      
    
    return render(request,'battle_home.html',context)
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from io import BytesIO
from modules.margin_report.builtin_functions import *
import datetime

def starting_page(request):
    title = 'Strategic_plain'
    return render(request, "strateg_plain/index.html", context={'title': title})


# Прием файлов и расчет
@csrf_exempt
def upload_files(request):
    # try:
    #     a = 1/0
    #     # raise TypeError('hi')
    # except Exception as e:
    #     return HttpResponse(e.args,status=500)

    if request.method == 'POST':
        # print(request.FILES)
        df_ukpf = request.FILES['ukpf']
        df_ukpf_cx = request.FILES['ukpf_cx']

    year = 2021

    # какие месяца по дням а какие по месяцам
    params = {'days': [8], 'month': [9, 10, 11, 12]}

    # Сколько с градации брать на разделку

    dict_ = {'0,500-0,600': 0,
             '0,600-0,700': 0,
             '0,700-0,800': 0,
             '0,800-0,900': 0,
             '0,900-1,000': 0.9,
             '1,000-1,100': 0.9,
             '1,100-1,200': 0.9,
             '1,200-1,300': 0.9,
             '1,300-1,400': 0.6,
             '1,400-1,500': 0.9,
             '1,500-1,600': 0.9,
             '1,600-1,700': 0,
             '1,700-1,800': 0,
             '1,800-1,900': 0,
             '1,900-2,000': 0,
             '2,000-2,100': 0,
             '2,100-2,200': 0,
             '2,200-2,300': 0,
             '2,300-2,400': 0,
             '2,400-2,500': 0,
             '2,500-3,500': 0}

    cols_sub = ['Дата забоя', 'Печень, тн', 'Сердца, тн', 'Желудки, тн', 'Шеи, тн', 'Жир', 'Головы, тн', 'Лапы, тн',
                'Утиль, тн']

    # пропорция по схемам разделки
    dict_sx = {1: 0.2, 2: 0.3, 3: 0.3, 4: 0.1, 5: 0.1}

    # Сколько сделать чахохбили
    target_chakhoh = 6
    ukpf = pd.read_excel(df_ukpf, sheet_name='Забой')
    ukpf_sub = ukpf[cols_sub].copy()
    ukpf = get_po_sto_gr(ukpf)
    chema_r = pd.read_excel(df_ukpf_cx, sheet_name='Лист1')

    # Часть по дням
    df_for_days = ukpf[([True if x.month == params['days'][0] else False for x in ukpf['Дата забоя']]) & (
                ukpf['Дата забоя'].dt.year == year)]
    df_for_days_gr = df_for_days.groupby('Дата забоя').sum().reset_index()
    # для суб
    df_for_days_sub = ukpf_sub[([True if x.month == params['days'][0] else False for x in ukpf_sub['Дата забоя']]) & (
                ukpf_sub['Дата забоя'].dt.year == year)]
    df_for_days_gr_sub = df_for_days_sub.groupby('Дата забоя').sum().reset_index()

    df_for_days = get_cons_arr(df_for_days_gr, dict_, chema_r, dict_sx)

    # Часть по месяцам
    df_for_month = ukpf[ukpf['Дата забоя'].dt.month.isin(params['month']) & (ukpf['Дата забоя'].dt.year == year)]
    df_for_month['Дата забоя'] = [datetime.datetime(x.year, x.month, 1) for x in df_for_month['Дата забоя']]
    df_for_month_gr = df_for_month.groupby('Дата забоя').sum().reset_index()

    # для суб

    df_for_month_sub = ukpf_sub[
        ukpf_sub['Дата забоя'].dt.month.isin(params['month']) & (ukpf_sub['Дата забоя'].dt.year == year)]
    df_for_month_sub['Дата забоя'] = [datetime.datetime(x.year, x.month, 1) for x in df_for_month_sub['Дата забоя']]
    df_for_month_gr_sub = df_for_month_sub.groupby('Дата забоя').sum().reset_index()

    sub_stack_month = df_for_month_gr_sub.set_index('Дата забоя').stack().reset_index()
    sub_stack_days = df_for_days_gr_sub.set_index('Дата забоя').stack().reset_index()
    cons_sub = sub_stack_month.append(sub_stack_days)
    cons_sub.columns = ['Дата забоя', 'Наименование части', 'Объем']

    df_for_month = get_cons_arr(df_for_month_gr, dict_, chema_r, dict_sx)
    cons1 = df_for_days.append(df_for_month)
    cons1 = cons_sub.append(cons1)
    cons1.loc[cons1['Наименование части'] != 'ЦБ', 'Градация'] = ''
    cons2 = pd.pivot_table(cons1, values='Объем', index=['Градация', 'Наименование части'], columns='Дата забоя',
                           aggfunc=np.sum).reset_index().fillna(0)

    # cons2 = calc_dop_chakh(cons2,'Окорочек','Сырье для чахохбили',0.7)
    # cons2 = calc_dop_chakh(cons2,'Грудка','Сырье для чахохбили',0.3)
    cons2 = calc_dop_chakh(cons2, 'Окорочек', 'Сырье для чахохбили', 0.7, target_chakhoh)
    cons2 = calc_dop_chakh(cons2, 'Грудка', 'Сырье для чахохбили', 0.3, target_chakhoh)

    # разделяем
    cons2 = calc_decomp_ch(cons2, 'Окорочек', ['Голень', 'Бедро'], 0.4124)

    cons2 = cons2.groupby(['Градация', 'Наименование части']).sum().reset_index()


    output = BytesIO()

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    cons2.to_excel(writer, sheet_name='Итог')

    writer.save()

    output.seek(0)

    now = datetime.datetime.now()
    date_for_name_file = now.strftime("%d-%m-%Y %H:%M")

    response = StreamingHttpResponse(output,
                                     content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=report ' + date_for_name_file + '.xlsx'

    return response

    return JsonResponse({'status':200})





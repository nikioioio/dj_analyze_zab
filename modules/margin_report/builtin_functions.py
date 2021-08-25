import pandas as pd
import datetime
import numpy as np
import warnings

warnings.filterwarnings('ignore')


# функция для раздулки
def get_razd(sx_razd, v_):
    ch_razd = {}
    #     если это деловая часть
    for ind in sx_razd.index:

        if sx_razd.at[ind, 'Из какой части пром'] == 0:
            v___ = v_ * sx_razd.at[ind, 'Процент разделки']
            #         df_cons = df_cons.append(pd.DataFrame({'Дата забоя':df['Дата забоя'],'Градация':grad,'Наименование части':fff.at[ind,'Часть'],'Объем':v___}))
            ch_razd[sx_razd.at[ind, 'Часть']] = v___

    for ind in sx_razd.index:
        #     для пром
        if sx_razd.at[ind, 'Из какой части пром'] != 0:
            #         print(fff.at[ind,'Из какой части пром'])
            #         Процент вет брака
            pr_vetbr = sx_razd[(sx_razd['Из какой части пром'] == sx_razd.at[ind, 'Из какой части пром']) & (
                        sx_razd['Часть'] == sx_razd.at[ind, 'Часть'])]['Процент разделки'].values
            v_pochasti = ch_razd[sx_razd.at[ind, 'Из какой части пром']]
            it_prom = pr_vetbr * v_pochasti
            ch_razd[sx_razd.at[ind, 'Часть']] = it_prom
            ch_razd[sx_razd.at[ind, 'Из какой части пром']] = ch_razd[sx_razd.at[ind, 'Из какой части пром']] - ch_razd[
                sx_razd.at[ind, 'Часть']]

    #     Выбираем минимальное из деловых частей (там где больше одного элемента)
    for ind in sx_razd.index:
        ch_razd[sx_razd.at[ind, 'Часть']] = min(ch_razd[sx_razd.at[ind, 'Часть']])

    for key___ in ch_razd.keys():
        ch_razd[key___] = ch_razd[key___].sum()
    return ch_razd


# делит по 100 гр
def get_po_sto_gr(inp):
    inp = inp.set_index('Дата забоя')
    df = pd.DataFrame(inp.index)
    df = df.set_index('Дата забоя')
    for ind, col in enumerate(inp.columns):
        #         print(col.split('-')[0]=='2,500')
        try:
            if col.split('-')[0] == '2,500':
                df['2,500-3,500'] = inp['2,500-3,500']
            #                 print(col)

            if ind == 0 or ind % 2 == 0:
                cols = inp.iloc[:, [ind, ind + 1]].columns
                df[cols[0].split('-')[0] + '-' + cols[1].split('-')[1]] = inp.iloc[:, [ind, ind + 1]].sum(axis=1)


        except IndexError:
            pass
    return df.reset_index()


# логика формирования итогового фрейма

def get_cons_arr(df_gr, dict_, chema_r, dict_sx):
    df_cons = pd.DataFrame()
    for date in df_gr['Дата забоя'].unique():

        df = df_gr[df_gr['Дата забоя'] == date]

        for grad in dict_.keys():

            v_razd = df[grad].values * dict_[grad]
            v_cb = df[grad].values * (1 - dict_[grad])

            #         Часть с разделкой
            if v_razd > 0:

                #             print(v_razd)

                #             Иду по пропорции разделки
                for el_sx in dict_sx.keys():

                    #                 Объем по схеме
                    v_ = v_razd * dict_sx[el_sx]
                    #                 print(str(v_razd)+' '+ str(v_))
                    sx_razd = chema_r[chema_r['Номер'] == el_sx]
                    it_chema = get_razd(sx_razd, v_)
                    for key_ in it_chema.keys():
                        df_cons = df_cons.append(pd.DataFrame(
                            {'Дата забоя': df['Дата забоя'], 'Градация': grad, 'Наименование части': key_,
                             'Объем': it_chema[key_]}))
            #                     print(key_)
            #                     break
            #                 break

            #                 print('общий объем'+ str(v_razd) + ' Объем на конкретную схему эту '+str(v_))

            #         Часть ЦБ
            if v_cb > 0:
                df_cons = df_cons.append(pd.DataFrame(
                    {'Дата забоя': df['Дата забоя'], 'Градация': grad, 'Наименование части': 'ЦБ', 'Объем': v_cb}))
    return df_cons


# # разбивает часть по процентц в аргументе
# def calc_division_ch(cons2,from_name,to_name,percent):
#     for_ch_okor = cons2.loc[cons2['Наименование части']==from_name]
#     ost_okor = cons2.loc[cons2['Наименование части']==from_name]

#     for col in for_ch_okor.columns:
#         try:
#             for_ch_okor.loc[:,col] = for_ch_okor.loc[:,col]*percent
#         except TypeError:
#             pass

#     for col in ost_okor.columns:
#         if ost_okor[col].dtype=='float':
#             cons2.loc[cons2['Наименование части']==from_name,col] = ost_okor[col]-for_ch_okor[col]

#     for_ch_okor['Наименование части'] = to_name

#     cons2 = cons2.append(for_ch_okor).reset_index(drop=True)
#     return cons2


# разбивает часть по пропорциям
def calc_decomp_ch(cons2, from_name, to_name, percent):
    for_ch_okor = cons2.loc[cons2['Наименование части'] == from_name]
    ost_okor = cons2.loc[cons2['Наименование части'] == from_name]

    for col in for_ch_okor.columns:
        try:
            for_ch_okor.loc[:, col] = for_ch_okor.loc[:, col] * percent
        except TypeError:
            pass
    for_ch_okor['Наименование части'] = to_name[0]

    for col in ost_okor.columns:
        if ost_okor[col].dtype == 'float':
            cons2.loc[cons2['Наименование части'] == from_name, col] = ost_okor[col] - for_ch_okor[col]

    cons2.loc[cons2['Наименование части'] == from_name, 'Наименование части'] = to_name[1]

    # #     for_ch_okor['Наименование части'] = to_name[1]

    cons2 = cons2.append(for_ch_okor).reset_index(drop=True)
    return cons2


# формирование чахохбили
#

# суммирует значения с фильтром по числовому значению
def total_sum(name_col, value_, df):
    sum_ = 0
    for str_ in df[df[name_col] == value_].sum():
        if isinstance(str_, np.float64):
            sum_ = sum_ + str_

    return sum_


# Формирование чахохбили из объема

"""Параметры : cons2:обрабобатываемый df
               from_name: часть откуда бурем 
               to_name: часть куда транспортируем объем
               percent: процент по анатомии
               tagret_val: целевой объем to_name"""


def calc_dop_chakh(cons2, from_name, to_name, percent, tagret_val):
    target_calc = tagret_val * percent

    for_ch_okor = cons2.loc[cons2['Наименование части'] == from_name]
    ost_okor = cons2.loc[cons2['Наименование части'] == from_name]

    tot_sum = total_sum('Наименование части', from_name, cons2)
    if target_calc >= tot_sum:
        print('Не возможно сделать данный объем ' + to_name + ' из ' + from_name + ', уменьшите его')
        return 0
    for col in for_ch_okor.columns:
        if for_ch_okor[col].dtype == 'float':
            for_ch_okor.loc[cons2['Наименование части'] == from_name, col] = for_ch_okor.loc[cons2[
                                                                                                 'Наименование части'] == from_name, col] / tot_sum * target_calc

    for col in ost_okor.columns:
        if ost_okor[col].dtype == 'float':
            cons2.loc[cons2['Наименование части'] == from_name, col] = ost_okor[col] - for_ch_okor[col]

    for_ch_okor['Наименование части'] = 'Сырье для чахохбили'

    cons2 = cons2.append(for_ch_okor).reset_index(drop=True)

    return cons2
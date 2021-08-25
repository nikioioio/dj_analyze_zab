# # Функция возвращает  производственную часть фабрик
import pandas as pd
import datetime
import calendar
from modules.margin_report.builtin_functions import retype_index,retype_multiindex,get_current_data,dict_keys,rev_to_dict,insert_vpr,input_proc_packaging,restruct_multitindex
import warnings
warnings.filterwarnings('ignore')



# def get_ssmp_ukpf(file_factory, file_mapping, file_coef_cenn, file_ost_nach_g, mon, global_index,filename,year_report): #первоначальный вариант
# def get_ssmp_ukpf(ar,mon, global_index,filename,year_report): # 2 вызова
def get_ssmp_ukpf(*args): # параллельный вызов
    ar = args[0][0]
    mon = args[0][1]
    global_index = args[0][2]
    filename = args[0][3]
    year_report = args[0][4]

    global_index = global_index
    sale_finished_products_UKPF =  ar[0]
    balance_depot_stock_UKPF =  ar[1]
    adm_UKPF =  ar[2]
    PP_UKPF =  ar[3]
    per_3_UKPF =  ar[4]
    per_2_UKPF_meat =  ar[5]
    per_2_UKPF_product =  ar[6]
    per_2_UKPF_losses =  ar[7]
    per_1_UKPF =  ar[8]
    NZ_UKPF =  ar[9]
    UIS_UKPF =  ar[10]
    DATA_upload =  ar[11]
    Production_output =  ar[12]
    mmo = ar[13]
    mapping =  ar[14]
    koef_ef =  ar[15]
    ost_start_new_form =  ar[16]


    cons_pr = {}
    per_1 = {}
    per_2 = {}
    # sale_finished_products_UKPF = pd.read_excel(directory + filename, sheet_name='Продажи ГП')
    # balance_depot_stock_UKPF = pd.read_excel(directory + filename, sheet_name='Остатки')
    # adm_UKPF = pd.read_excel(directory + filename, sheet_name='Адм')
    # PP_UKPF = pd.read_excel(directory + filename, sheet_name='РР')
    # per_3_UKPF = pd.read_excel(directory + filename, sheet_name='3 передел')
    # per_2_UKPF_meat = pd.read_excel(directory + filename, sheet_name='2 передел мясо')
    # per_2_UKPF_product = pd.read_excel(directory + filename, sheet_name='2 передел гп')
    # per_2_UKPF_losses = pd.read_excel(directory + filename, sheet_name='2 передел потери')
    # per_1_UKPF = pd.read_excel(directory + filename, sheet_name='1 передел')
    # NZ_UKPF = pd.read_excel(directory + filename, sheet_name='Накладные затраты', header=[0, 1, 2])
    # UIS_UKPF = pd.read_excel(directory + filename, sheet_name='УиС')
    # DATA_upload = pd.read_excel(directory + filename, sheet_name='Общие данные по выходу')
    # Production_output = pd.read_excel(directory + filename, sheet_name='Выпуск ГП')
    # mapping = pd.read_excel(directory + mapping, sheet_name='Mapping', header=[0, 1])
    # koef_ef = pd.read_excel(directory + coef_cenn, sheet_name='Лист1')
    # ost_start_new_form = pd.read_excel(directory + ost_nach_g, sheet_name='Sheet1', index_col=0)
    # mmo = pd.read_excel(directory + filename, sheet_name='ММО', header=[0, 1])
    # Блок типизации данных
    # Блок типизации данных
    dates = [x for x in PP_UKPF.columns if isinstance(x, datetime.datetime)]

    # Изменил тип артикула
    mapping = retype_multiindex(mapping, 'int', 'Артикул', 1)

    # Изменил тип артикула

    per_1_UKPF = retype_index(per_1_UKPF, 'int', 'Артикул')
    per_2_UKPF_meat = retype_index(per_2_UKPF_meat, 'int', 'Артикул')
    per_2_UKPF_product = retype_index(per_2_UKPF_product, 'int', 'Артикул')
    per_2_UKPF_losses = retype_index(per_2_UKPF_losses, 'int', 'Артикул')
    per_3_UKPF = retype_index(per_3_UKPF, 'int', 'Артикул')
    Production_output = retype_index(Production_output, 'int', 'Артикул')
    UIS_UKPF = retype_index(UIS_UKPF, 'int', 'Артикул')
    sale_finished_products_UKPF = retype_index(sale_finished_products_UKPF, 'int', 'Артикул')
    balance_depot_stock_UKPF = retype_index(balance_depot_stock_UKPF, 'int', 'Артикул')
    mmo = restruct_multitindex(mmo)

    iter_months = [datetime.datetime(year_report, x, calendar.monthrange(year_report, x)[1], 0, 0) for x in
                   range(1, 13)]

    for ind___, current_month in enumerate(iter_months):

        #         нужна для формирования таблицы с остатками
        if ind___ > 0:
            prev_month = iter_months[ind___ - 1]

        print(current_month)
        # получил текущие даныные по current_month
        curr_per_1_UKPF = get_current_data(per_1_UKPF, global_index, current_month)
        curr_per_2_UKPF_meat = get_current_data(per_2_UKPF_meat, global_index, current_month)
        curr_per_2_UKPF_product = get_current_data(per_2_UKPF_product, global_index, current_month)
        curr_per_2_UKPF_losses = get_current_data(per_2_UKPF_losses, global_index, current_month)
        curr_per_3_UKPF = get_current_data(per_3_UKPF.set_index(['Артикул', 'Тип продукции']), global_index,
                                           current_month).reset_index()
        curr_Production_output_UKPF = get_current_data(Production_output, global_index, current_month)
        curr_UIS_UKPF = get_current_data(UIS_UKPF, global_index, current_month)
        curr_sale_finished_products_UKPF = get_current_data(sale_finished_products_UKPF, global_index, current_month)
        curr_balance_depot_stock_UKPF = get_current_data(balance_depot_stock_UKPF, global_index, current_month)
        curr_mmo = get_current_data(mmo, global_index, current_month).reset_index()

        # отсекли только то что в соответствующих переделах из справочников mapping

        # Блок получения данных по mapping (Отсекаем только то что есть в mapping)

        key = filename.split('.')[0]
        dict_mapping = {'УКПФ': ['Мэппинг УКПФ 1 передел', 'Мэппинг УКПФ 2 передел', 'Мэппинг УКПФ Затраты'],
                        'МПФ': ['Мэппинг МПФ 1 передел', 'Мэппинг МПФ 2 передел', 'Мэппинг МПФ Затраты']}

        cons_1_per = curr_per_1_UKPF[curr_per_1_UKPF['Артикул'].isin(
            mapping[mapping[dict_mapping[key][0]]['Артикул'] != 0][dict_mapping[key][0]]['Артикул'])].groupby(
            ['Артикул', 'Продукция']).sum().reset_index()
        #         cons_2_per_meat = curr_per_2_UKPF_meat[curr_per_2_UKPF_meat['Артикул'].isin(mapping[mapping[dict_mapping[key][1]]['Артикул']!=0][dict_mapping[key][1]]['Артикул'])].groupby(['Артикул','Продукция']).sum().reset_index()
        cons_2_per_meat = curr_per_2_UKPF_meat.copy()
        cons_2_per_product = curr_per_2_UKPF_product[curr_per_2_UKPF_product['Артикул'].isin(
            mapping[mapping[dict_mapping[key][1]]['Артикул'] != 0][dict_mapping[key][1]]['Артикул'])].groupby(
            ['Артикул', 'Продукция']).sum().reset_index()
        cons_2_per_losses = curr_per_2_UKPF_losses[
            ~curr_per_2_UKPF_losses['Артикул'].apply(lambda x: isinstance(x, str))]

        dict_chast_1 = rev_to_dict(dict_keys(dict_mapping[key][0], mapping)['Артикул'],
                                   dict_keys(dict_mapping[key][0], mapping)['Часть'])
        # Присваем части
        cons_1_per['часть'] = cons_1_per.apply(lambda x: insert_vpr(x['Артикул'], dict_chast_1, 'Часть'),
                                               axis=1).astype('str')

        # 2 передел для анализа

        dict_chast_2 = rev_to_dict(dict_keys(dict_mapping[key][1], mapping)['Артикул'],
                                   dict_keys(dict_mapping[key][1], mapping)['Часть'])

        curr_per_2_UKPF_meat['часть'] = curr_per_2_UKPF_meat.apply(
            lambda x: insert_vpr(x['Артикул'], dict_chast_2, 'Часть'), axis=1).astype('str')
        cons_2_per_product['часть'] = cons_2_per_product.apply(
            lambda x: insert_vpr(x['Артикул'], dict_chast_2, 'Часть'), axis=1).astype('str')
        cons_2_per_losses['часть'] = cons_2_per_losses.apply(lambda x: insert_vpr(x['Артикул'], dict_chast_2, 'Часть'),
                                                             axis=1).astype('str')
        curr_per_3_UKPF['часть'] = curr_per_3_UKPF.apply(lambda x: insert_vpr(x['Артикул'], dict_chast_2, 'Часть'),
                                                         axis=1).astype('str')
        # 3 передел для анализа
        #         curr_per_3_UKPF = get_type_product(curr_per_3_UKPF)

        dict_chast_3 = rev_to_dict(dict_keys(dict_mapping[key][2], mapping)['Артикул'],
                                   dict_keys(dict_mapping[key][2], mapping)['Часть'])
        # Выпуск ГП для анализа
        curr_Production_output_UKPF['часть'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_chast_3, 'Часть'), axis=1).astype('str')

        # группировка по частям
        # Первый передел по частям УКПФ
        part_1_cons_1_per = cons_1_per[['часть', current_month]].groupby('часть').sum().reset_index()

        # объем живка
        V_zhivka = DATA_upload[DATA_upload['Наименование'] == 'Объем живка, кг'].loc[:, current_month].values[0]
        # объем первого передела
        V_1_peredel = cons_1_per[current_month].sum()
        # С/с 1 передела
        SS_1_zperedel_without_amort = \
        DATA_upload[DATA_upload['Наименование'] == 'Сырье (живая птица) без амортизации'].loc[:, current_month].values[
            0] / 1000
        # Средняя с/с 1 передела, без амортизации
        Mean_SS_1_zperedel_without_amort = SS_1_zperedel_without_amort / V_1_peredel * 1000

        part_1_cons_1_per['%%от тушки'] = part_1_cons_1_per.apply(lambda x: x[current_month] / V_zhivka, axis=1)

        dict_koef_ef = rev_to_dict(koef_ef[koef_ef['Признак'] == 'убой']['Продукция'],
                                   koef_ef[koef_ef['Признак'] == 'убой']['Коэффициент'])
        part_1_cons_1_per['Доля стоимости 1 передела'] = part_1_cons_1_per.apply(
            lambda x: insert_vpr(x['часть'], dict_koef_ef, 'Коэффициент'), axis=1).astype('str')

        part_1_cons_1_per['усл.ед.'] = part_1_cons_1_per['Доля стоимости 1 передела'].astype('float64') * \
                                       part_1_cons_1_per['%%от тушки']

        part_1_cons_1_per['Распределение с/с 1 передела'] = part_1_cons_1_per.apply(
            lambda x: SS_1_zperedel_without_amort * x['усл.ед.'] / part_1_cons_1_per['усл.ед.'].sum(), axis=1)

        part_1_cons_1_per['С/с 1 передела'] = part_1_cons_1_per.apply(
            lambda x: 0 if x[current_month] == 0 else x['Распределение с/с 1 передела'] / x[current_month] * 1000,
            axis=1)

        # Конец первого передела

        # Начало второго передела
        #         part_1_cons_2_per_meat = cons_2_per_meat[['часть',current_month]].groupby('часть').sum().reset_index()

        part_1_cons_2_per_product = cons_2_per_product[['часть', current_month]].groupby('часть').sum().reset_index()

        # Объем на разделку без потерь
        V_raz_without_losses = cons_2_per_meat[current_month].sum()

        # С/с тушки, без амортизации

        SS_tushki_without_amort = part_1_cons_1_per[part_1_cons_1_per['часть'] == 'Тушка']['С/с 1 передела'].values[0]

        # С/с 2 передела, без амортизации
        Mean_SS_1_zperedel_without_amort = V_raz_without_losses * SS_tushki_without_amort / 1000

        part_1_cons_2_per_product['%%от тушки'] = part_1_cons_2_per_product.apply(
            lambda x: x[current_month] / V_raz_without_losses, axis=1)

        dict_koef_ef = rev_to_dict(koef_ef[koef_ef['Признак'] == 'обвалка']['Продукция'],
                                   koef_ef[koef_ef['Признак'] == 'обвалка']['Коэффициент'])
        part_1_cons_2_per_product['Доля стоимости 2 передела'] = part_1_cons_2_per_product.apply(
            lambda x: insert_vpr(x['часть'], dict_koef_ef, 'Коэффициент'), axis=1)

        part_1_cons_2_per_product['усл.ед.'] = part_1_cons_2_per_product['Доля стоимости 2 передела'].astype(
            'float64') * part_1_cons_2_per_product['%%от тушки']

        part_1_cons_2_per_product['Распределение с/с 2 передела'] = part_1_cons_2_per_product.apply(
            lambda x: Mean_SS_1_zperedel_without_amort * x['усл.ед.'] / part_1_cons_2_per_product['усл.ед.'].sum(),
            axis=1)

        part_1_cons_2_per_product['С/с 2 передела'] = part_1_cons_2_per_product.apply(
            lambda x: 0 if x[current_month] == 0 else x['Распределение с/с 2 передела'] / x[current_month] * 1000,
            axis=1)

        #         if ind___+1==1:
        #             return curr_Production_output_UKPF
        #             return part_1_cons_1_per,part_1_cons_2_per_product

        # логика по чахохбили df2 = данные со второго передела df3 данные с 3 передела

        def get_chahoh(df_2, df_3):
            if key == 'УКПФ':
                return (df_2[df_2['часть'] == 'грудка']['С/с 2 передела'].sum() *
                        df_3[df_3['Продукция'] == 'Грудка ЦБ'][current_month].sum() + \
                        df_2[df_2['часть'] == 'окорочок']['С/с 2 передела'].sum() *
                        df_3[df_3['Продукция'] == 'Окорочок ЦБ'][current_month].sum()) / \
                       (df_3[df_3['Продукция'] == 'Грудка ЦБ'][current_month].sum() +
                        df_3[df_3['Продукция'] == 'Окорочок ЦБ'][current_month].sum())
            elif key == 'МПФ':

                return (df_2[df_2['часть'] == 'грудка']['С/с 2 передела'].sum() *
                        df_3[df_3['Продукция'] == 'Грудка ЦБ в групповой упаковке в оборотной таре (охл.)'][
                            current_month].sum() + \
                        df_2[df_2['часть'] == 'окорочок']['С/с 2 передела'].sum() *
                        df_3[df_3['Продукция'] == 'Окорочок ЦБ в групповой упаковке в оборотной таре (охл.)'][
                            current_month].sum()) / \
                       (df_3[df_3['Продукция'] == 'Окорочок ЦБ в групповой упаковке в оборотной таре (охл.)'][
                            current_month].sum() +
                        df_3[df_3['Продукция'] == 'Грудка ЦБ в групповой упаковке в оборотной таре (охл.)'][
                            current_month].sum())

        # логика по ммо df1 это текущие данные ммо(исходник), df2 это рассчитанные данные по второму переделу
        #         if ind___+1==1:
        #             return get_chahoh(part_1_cons_2_per_product,curr_per_3_UKPF)
        df_for_mo_mapping = pd.concat([curr_per_1_UKPF,
                                       curr_per_2_UKPF_meat,
                                       curr_per_2_UKPF_product,
                                       curr_per_2_UKPF_losses,
                                       curr_per_3_UKPF])[['Артикул', current_month]]

        def get_mmo(df, df_for_mo_mapping):
            df = df.set_index('Артикул')[current_month].reset_index()
            df['часть'] = df.apply(lambda x: insert_vpr(x['Артикул'], dict_chast_2, 'Часть'), axis=1).astype('str')

            df['данные по переделам'] = df.apply(
                lambda x: df_for_mo_mapping[df_for_mo_mapping['Артикул'] == x['Артикул']][current_month].sum(), axis=1)

            vals_for_mmo = part_1_cons_1_per.rename(columns={'С/с 1 передела': 'С/с 2 передела'})[
                ['часть', 'С/с 2 передела']]. \
                append(part_1_cons_2_per_product[['часть', 'С/с 2 передела']])

            vals_ = rev_to_dict(vals_for_mmo['часть'], vals_for_mmo['С/с 2 передела'])

            df['стоимость с/с'] = df.apply(lambda x: insert_vpr(x['часть'], vals_, 'С/с 2 передела'), axis=1)

            df['С/с Птицеводства, тыс. тг'] = df['Объем затрат'] * df['стоимость с/с'] / 1000

            val_mmo = curr_Production_output_UKPF[curr_Production_output_UKPF['Артикул'] == 117][current_month].sum()

            return df['С/с Птицеводства, тыс. тг'].sum() / val_mmo * 1000

        part_1_cons_2_per_product = part_1_cons_2_per_product.append(pd.DataFrame(columns=['часть', 'С/с 2 передела'],
                                                                                  data={'часть': ['Чахохбили'],
                                                                                        'С/с 2 передела': [get_chahoh(
                                                                                            part_1_cons_2_per_product,
                                                                                            curr_per_3_UKPF)]}))
        part_1_cons_2_per_product = part_1_cons_2_per_product.append(pd.DataFrame(columns=['часть', 'С/с 2 передела'],
                                                                                  data={'часть': ['ММО'],
                                                                                        'С/с 2 передела': [
                                                                                            get_mmo(curr_mmo,
                                                                                                    df_for_mo_mapping)]}))

        #         ///////////////////////////////////////////////////////////////////////

        #         if ind___+1==1:
        #             return part_1_cons_2_per_product
        # #             return get_mmo(curr_mmo,df_for_mo_mapping)

        per_1[current_month] = part_1_cons_1_per
        per_2[current_month] = part_1_cons_2_per_product

        #  -----------------------

        # ПГ_CC МП

        def func(x, col, per1, per2_1, per2_2, per2_3, per3):
            filter_ = 'Артикул'
            if per3[(per3[filter_] == x[filter_]) & (per3['Тип продукции'] == 'основная продукция')][col].sum() > 0:
                return per3[(per3[filter_] == x[filter_]) & (per3['Тип продукции'] == 'основная продукция')][col].sum()
            else:
                return x[current_month]

        #             sum_ = per1[per1[filter_] == x[filter_]][col].sum() + \
        #                 per2_1[per2_1[filter_] == x[filter_]][col].sum() + \
        #                 per2_2[per2_2[filter_] == x[filter_]][col].sum()+ \
        #                 per2_3[per2_3[filter_] == x[filter_]][col].sum()+ \
        #                 per3[(per3[filter_] == x[filter_])&(per3['Тип продукции'] == 'основная продукция')][col].sum()
        #             return sum_ if sum_>0 else x[col]

        curr_Production_output_UKPF['Объем мяса  (без воды и специй),кг'] = \
            curr_Production_output_UKPF.apply(
                lambda x: func(x, current_month, cons_1_per, cons_2_per_meat, cons_2_per_product, \
                               cons_2_per_losses, curr_per_3_UKPF), axis=1)

        #         if ind___+1==1:
        #             return curr_Production_output_UKPF

        # ------------------------------

        df_sebes_group = part_1_cons_2_per_product[['часть', 'С/с 2 передела']].rename(
            columns={'С/с 2 передела': 'Себес'}). \
            append(part_1_cons_1_per[['часть', 'С/с 1 передела']].rename(columns={'С/с 1 передела': 'Себес'})). \
            groupby('часть').sum().reset_index()

        dict_sebes = rev_to_dict(df_sebes_group['часть'], df_sebes_group['Себес'])
        curr_Production_output_UKPF['Мясосырье, Птицевосдтво, тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['часть'], dict_sebes, 'Себес'), axis=1)

        # ------------------------------

        curr_Production_output_UKPF['C/c мясосырья, Птицеводство тыс. тг'] = curr_Production_output_UKPF.apply(
            lambda x: x['Объем мяса  (без воды и специй),кг'] * \
                      x['Мясосырье, Птицевосдтво, тг/кг'] / 1000, axis=1)

        # ------------------------------

        curr_Production_output_UKPF['C/c мясосырья, Птицеводство тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['C/c мясосырья, Птицеводство тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # ------------------------------

        def func(x, col, uis, mask):
            filter_ = 'Артикул'
            sum_ = uis[(uis[filter_] == x[filter_]) & (uis['Номенклатура'] == mask)][col].sum()
            return sum_ / 1000

        curr_Production_output_UKPF['Специи, добавки тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x, current_month, curr_UIS_UKPF, 'Специи, добавки'),
                                              axis=1)

        # ------------------------------

        curr_Production_output_UKPF['Специи, добавки тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Специи, добавки тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # ------------------------------

        if key == 'УКПФ':

            curr_Production_output_UKPF['Упаковочный материал тыс. тг'] = \
                curr_Production_output_UKPF.apply(
                    lambda x: func(x, current_month, curr_UIS_UKPF, 'Упаковочный материал'), axis=1)

        elif key == 'МПФ':

            all_zat = curr_UIS_UKPF[curr_UIS_UKPF['Номенклатура'] == 'Упаковочный материал'][current_month].sum()
            curr_UIS_UKPF['mapping'] = curr_UIS_UKPF.apply(lambda x: "ГП"
            if curr_Production_output_UKPF[curr_Production_output_UKPF['Артикул'] == x['Артикул']][
                   current_month].sum() > 0
            else "промпереработка", axis=1)

            sum_up_map_prom = curr_UIS_UKPF[(curr_UIS_UKPF['Номенклатура'] == 'Упаковочный материал') &
                                            (curr_UIS_UKPF['mapping'] == 'промпереработка')][current_month].sum()

            po_gp = all_zat - sum_up_map_prom

            curr_UIS_UKPF['расп уп мат'] = curr_UIS_UKPF.apply(lambda x: x[current_month] / po_gp * all_zat
            if x['Номенклатура'] == 'Упаковочный материал' and x['mapping'] != 'промпереработка'
            else 0, axis=1)

            curr_Production_output_UKPF['Упаковочный материал тыс. тг'] = \
                curr_Production_output_UKPF.apply(
                    lambda x: func(x, 'расп уп мат', curr_UIS_UKPF, 'Упаковочный материал'), axis=1)

        # ------------------------------

        #         if ind___+1==2:
        #             return curr_Production_output_UKPF

        curr_Production_output_UKPF['Упаковочный материал тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Упаковочный материал тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # ------------------------------

        curr_Production_output_UKPF['Итого с/c с прямыми расходами тыс. тг'] = curr_Production_output_UKPF[
                                                                                   'C/c мясосырья, Птицеводство тыс. тг'] + \
                                                                               curr_Production_output_UKPF[
                                                                                   'Специи, добавки тыс. тг'] + \
                                                                               curr_Production_output_UKPF[
                                                                                   'Упаковочный материал тыс. тг']

        # ------------------------------

        curr_Production_output_UKPF['Итого с/c с прямыми расходами тг/кг'] = curr_Production_output_UKPF[
                                                                                 'C/c мясосырья, Птицеводство тг/кг'] + \
                                                                             curr_Production_output_UKPF[
                                                                                 'Специи, добавки тг/кг'] + \
                                                                             curr_Production_output_UKPF[
                                                                                 'Упаковочный материал тг/кг']

        # ------------------------------

        dict_slaughter_costs = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                           mapping['Мэппинг ' + key + ' Затраты']['Upstream'])
        curr_Production_output_UKPF['Затраты на убой и потрошение, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_slaughter_costs, 'Upstream'), axis=1).astype('str')

        # ------------------------------

        def func(x, col, df, df1, filter_):
            sum_ = df[df[filter_] == "да"][col].sum()

            if x[filter_] == 'да':
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['upstream']['УиП']['всего'].sum() / 1000
            else:
                return 0
            return

        curr_Production_output_UKPF['Затраты на убой и потрошение тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x, current_month, curr_Production_output_UKPF, NZ_UKPF,
                                                             'Затраты на убой и потрошение, признак'), axis=1)

        # ------------------------------

        curr_Production_output_UKPF['Затраты на убой и потрошение тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на убой и потрошение тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # ------------------------------

        dict_cutting_up = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                      mapping['Мэппинг ' + key + ' Затраты']['Разделка'])
        curr_Production_output_UKPF['Затраты на разделку, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_cutting_up, 'Разделка'), axis=1).astype('str')

        # ------------------------------

        def func(x, col, df, df1, filter_):

            if x[filter_] == 'да':
                sum_ = df[df[filter_] == "да"][col].sum()
                return x[current_month] / sum_ * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['ОиР'][
                           'остальное'].sum() / 1000
            elif x[filter_] == 'KFC':
                sum_ = df[df[filter_] == "KFC"][col].sum()
                return x[current_month] / sum_ * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['ОиР']['KFC'].sum() / 1000
            else:
                return 0

        curr_Production_output_UKPF['Затраты на разделку тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на разделку, признак'
                                                             ), axis=1)

        # -------------------------------

        curr_Production_output_UKPF['Затраты на разделку тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на разделку тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # -------------------------------

        dict_cooling_down = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                        mapping['Мэппинг ' + key + ' Затраты']['Охлаждение'])
        curr_Production_output_UKPF['Затраты на охлаждение, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_cooling_down, 'Охлаждение'), axis=1).astype('str')

        # -------------------------------

        def func(x, col, df, df1, filter_):
            sum_ = df[df[filter_] == "да"][col].sum()

            if x[filter_] == 'да':
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['охлаждение'][
                           'охл'].sum() / 1000
            else:
                return 0
            return

        curr_Production_output_UKPF['Затраты на охлаждение тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на охлаждение, признак'
                                                             ), axis=1)

        # -------------------------------

        curr_Production_output_UKPF['Затраты на охлаждение тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на охлаждение тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # -------------------------------

        dict_freezing = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                    mapping['Мэппинг ' + key + ' Затраты']['Заморозка'])
        curr_Production_output_UKPF['Затраты на заморозку, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_freezing, 'Заморозка'), axis=1).astype('str')

        # -------------------------------

        def func(x, col, df, df1, filter_):
            sum_ = df[df[filter_] == "да"][col].sum()

            if x[filter_] == 'да':
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['охлаждение'][
                           'зам'].sum() / 1000
            else:
                return 0
            return

        curr_Production_output_UKPF['Затраты на заморозку тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на заморозку, признак'
                                                             ), axis=1)

        # --------------------------------

        curr_Production_output_UKPF['Затраты на заморозку тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на заморозку тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # --------------------------------

        dict_individual_pacts = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                            mapping['Мэппинг ' + key + ' Затраты']['индив. пакет'])
        curr_Production_output_UKPF['Затраты на Индив. пакет, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_individual_pacts, 'индив. пакет'), axis=1).astype('str')

        # --------------------------------

        dict_background = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                      mapping['Мэппинг ' + key + ' Затраты']['подложка'])
        curr_Production_output_UKPF['Затраты на Подложку, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_background, 'подложка'), axis=1).astype('str')

        # --------------------------------

        dict_group_package = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                         mapping['Мэппинг ' + key + ' Затраты']['групповой пакет'])
        curr_Production_output_UKPF['Затраты на Групп. Пакет, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_group_package, 'групповой пакет'), axis=1).astype('str')

        # --------------------------------

        NZ_UKPF = input_proc_packaging(curr_Production_output_UKPF,
                                       ['Затраты на Индив. пакет, признак', \
                                        'Затраты на Подложку, признак', \
                                        'Затраты на Групп. Пакет, признак'],
                                       current_month,
                                       'Норма упаковки, кг/чел*час',
                                       NZ_UKPF,
                                       ['индив. пакет', 'подложка', 'групповой пакет'],
                                       'Участок фасовки и упаковки '
                                       )

        # --------------------------------

        def func(x, col, df, df1, filter_):
            sum_ = df[df[filter_] == "да"][col].sum()

            if x[filter_] == 'да':
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['Упак'][
                           'индив. пакет'].sum() / 1000
            else:
                return 0
            return

        curr_Production_output_UKPF['Затраты на Индив. пакет тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на Индив. пакет, признак'
                                                             ), axis=1)

        # --------------------------------

        curr_Production_output_UKPF['Затраты на Индив. пакет тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на Индив. пакет тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # --------------------------------

        def func(x, col, df, df1, filter_):
            sum_ = df[df[filter_] == "да"][col].sum()

            if x[filter_] == 'да':
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['Упак'][
                           'подложка'].sum() / 1000
            else:
                return 0
            return

        curr_Production_output_UKPF['Затраты на Подложку тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на Подложку, признак'
                                                             ), axis=1)

        #         if ind___+1==2:
        #             return part_1_cons_2_per_product

        # --------------------------------

        curr_Production_output_UKPF['Затраты на Подложку тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на Подложку тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # --------------------------------

        def func(x, col, df, df1, filter_):
            sum_ = df[df[filter_] == "да"][col].sum()

            if x[filter_] == 'да':
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['Упак'][
                           'групповой пакет'].sum() / 1000
            else:
                return 0
            return

        curr_Production_output_UKPF['Затраты на Групп. Пакет тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на Групп. Пакет, признак'
                                                             ), axis=1)

        # --------------------------------

        curr_Production_output_UKPF['Затраты на Групп. Пакет тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на Групп. Пакет тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # --------------------------------

        dict_marinate = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                    mapping['Мэппинг ' + key + ' Затраты']['маринация'])
        curr_Production_output_UKPF['Затраты на Маринацию, признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_marinate, 'маринация'), axis=1).astype('str')

        # --------------------------------

        def func(x, col, df, df1, filter_):

            if x[filter_] == 'да':
                sum_ = df[df[filter_] == "да"][col].sum()
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['Маринады'][
                           'остальное'].sum() / 1000
            elif x[filter_] == 'KFC':
                sum_ = df[df[filter_] == "KFC"][col].sum()
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['Маринады'][
                           'KFC'].sum() / 1000
            else:
                return 0

        curr_Production_output_UKPF['Затраты на Маринацию тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на Маринацию, признак'
                                                             ), axis=1)

        # --------------------------------

        curr_Production_output_UKPF['Затраты на Маринацию тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на Маринацию тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        # --------------------------------

        dict_pressing = rev_to_dict(mapping['Мэппинг ' + key + ' Затраты']['Артикул'],
                                    mapping['Мэппинг ' + key + ' Затраты']['Прессование'])
        curr_Production_output_UKPF['Затраты на Прессование признак'] = curr_Production_output_UKPF.apply(
            lambda x: insert_vpr(x['Артикул'], dict_pressing, 'Прессование'), axis=1).astype('str')

        # --------------------------------

        def func(x, col, df, df1, filter_):
            sum_ = df[df[filter_] == "да"][col].sum()

            if x[filter_] == 'да':
                return (x[current_month] / sum_) * \
                       df1[df1['Месяц']['Месяц']['Месяц'] == current_month]['downstream']['прессование'][
                           'всего'].sum() / 1000
            else:
                return 0
            return

        curr_Production_output_UKPF['Затраты на Прессование тыс. тг'] = \
            curr_Production_output_UKPF.apply(lambda x: func(x,
                                                             current_month,
                                                             curr_Production_output_UKPF,
                                                             NZ_UKPF,
                                                             'Затраты на Прессование признак'
                                                             ), axis=1)

        # --------------------------------

        curr_Production_output_UKPF['Затраты на Прессование тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Затраты на Прессование тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        #         if ind___+1==1:
        #             return curr_Production_output_UKPF
        # --------------------------------

        curr_Production_output_UKPF['Итого накладная с/с тыс. тг'] = curr_Production_output_UKPF[
                                                                         'Затраты на убой и потрошение тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на охлаждение тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на заморозку тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на Индив. пакет тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на Групп. Пакет тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на Маринацию тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на Прессование тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на разделку тыс. тг'] + \
                                                                     curr_Production_output_UKPF[
                                                                         'Затраты на Подложку тыс. тг']

        curr_Production_output_UKPF['Итого накладная с/с тг/кг'] = curr_Production_output_UKPF[
                                                                       'Затраты на убой и потрошение тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на охлаждение тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на заморозку тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на Индив. пакет тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на Групп. Пакет тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на Маринацию тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на Прессование тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на разделку тг/кг'] + \
                                                                   curr_Production_output_UKPF[
                                                                       'Затраты на Подложку тг/кг']

        curr_Production_output_UKPF['Итого с/c тыс. тг'] = curr_Production_output_UKPF[
                                                               'Итого с/c с прямыми расходами тыс. тг'] + \
                                                           curr_Production_output_UKPF['Итого накладная с/с тыс. тг']

        curr_Production_output_UKPF['Итого с/c тг/кг'] = curr_Production_output_UKPF.apply(
            lambda x: 0 if x[current_month] == 0 else x['Итого с/c тыс. тг'] / \
                                                      x[current_month] * 1000, axis=1)

        #         if ind___+1==1:
        #             return curr_Production_output_UKPF

        #    Записали в словарь
        cons_pr[current_month] = curr_Production_output_UKPF

        # таблица с остатками
        # для новой формы остатков
        cols_join = [x for x in curr_Production_output_UKPF.rename(columns={current_month: 'Объем кг'}).columns if
                     x.find('тг/кг') != -1]

        cols_join.extend(['Объем кг'])

        if current_month.month == 1:

            start_date = datetime.datetime(year_report - 1, 12, 31, 0, 0)

            f_prt = pd.DataFrame(ost_start_new_form.index)
            # общий список из остатков , производства и продаж гп
            arr_ost = f_prt.append(curr_Production_output_UKPF[['Артикул']]).append(
                curr_sale_finished_products_UKPF[['Артикул']]).drop_duplicates(subset=['Артикул'])

            arr_ost = arr_ost.set_index('Артикул')
            curr_Production_output_UKPF = curr_Production_output_UKPF.set_index('Артикул')

            arr_ost = arr_ost[~arr_ost.index.duplicated(keep='first')]

            # # Берем начальные остатки
            # ost_start.columns = [x[1] for x in ost_start.columns]

            cons_ost_start = pd.concat([ost_start_new_form[cols_join], arr_ost], axis=1)

            ml = pd.MultiIndex.from_tuples([('Остаток', start_date, x) for x in cons_ost_start.columns])

            cons_ost_start.columns = ml

            path_ost_nach = ('Остаток', start_date)
            path_pr = ('Приход', current_month)
            path_r = ('Расход', current_month)
            path_ost_kon = ('Остаток', current_month)

            # приход для объединения с остатками
            production_for_join_ost = curr_Production_output_UKPF.rename(columns={current_month: 'Объем кг'})[cols_join]

            # приход рассчитан ранее , поэтому просто их joinim с остатками
            ml = pd.MultiIndex.from_tuples([('Приход', current_month, x) for x in production_for_join_ost.columns])
            production_for_join_ost.columns = ml

            # production_for_join_ost блок с выпуском (он будет актуальным)

            it = pd.concat([cons_ost_start, production_for_join_ost], axis=1)


        else:
            path_ost_nach = ('Остаток', prev_month)
            path_pr = ('Приход', current_month)
            path_r = ('Расход', current_month)
            path_ost_kon = ('Остаток', current_month)

            # приход для объединения с остатками
            curr_Production_output_UKPF = curr_Production_output_UKPF.set_index('Артикул')
            production_for_join_ost = curr_Production_output_UKPF.rename(columns={current_month: 'Объем кг'})[cols_join]
            #

            ml = pd.MultiIndex.from_tuples([('Приход', current_month, x) for x in production_for_join_ost.columns])

            production_for_join_ost.columns = ml

            it = pd.concat([it.set_index('Артикул'), production_for_join_ost], axis=1)

        #             it = it.set_index('Артикул')

        # формируем расходную часть

        ml = pd.MultiIndex.from_tuples([('Расход', current_month, x[2]) for x in production_for_join_ost.columns])
        arr_pash = arr_ost.copy()
        arr_pash = pd.DataFrame(columns=ml, index=arr_pash.index)

        it = pd.concat([it, arr_pash], axis=1)

        it = it.reset_index()

        it.fillna(0, inplace=True)

        # -----------------------------------

        def func(x, df, filter_, col):
            return df[df['Артикул'] == x['Артикул'][0]][col].sum()

        it.loc[:, (path_r[0], path_r[1], 'Объем кг')] = it.apply(lambda x: func(x,
                                                                                curr_sale_finished_products_UKPF,
                                                                                'Артикул',
                                                                                current_month
                                                                                ), axis=1)

        # -----------------------------------

        items = ['C/c мясосырья, Птицеводство тг/кг', 'Специи, добавки тг/кг', 'Упаковочный материал тг/кг',
                 'Затраты на убой и потрошение тг/кг',
                 'Затраты на разделку тг/кг', 'Затраты на охлаждение тг/кг', 'Затраты на заморозку тг/кг',
                 'Затраты на Индив. пакет тг/кг',
                 'Затраты на Подложку тг/кг', 'Затраты на Групп. Пакет тг/кг', 'Затраты на Маринацию тг/кг',
                 'Затраты на Прессование тг/кг']

        for item in items:
            it.loc[:, (path_r[0], path_r[1], item)] = (it.loc[:, (path_ost_nach[0], path_ost_nach[1], 'Объем кг')] * \
                                                       it.loc[:, (path_ost_nach[0], path_ost_nach[1], item)] + \
                                                       it.loc[:, (path_pr[0], path_pr[1], 'Объем кг')] * \
                                                       it.loc[:, (path_pr[0], path_pr[1], item)]) / \
                                                      (it.loc[:,
                                                       (path_ost_nach[0], path_ost_nach[1], 'Объем кг')] + it.loc[:, (
                                                                                                                     path_pr[
                                                                                                                         0],
                                                                                                                     path_pr[
                                                                                                                         1],
                                                                                                                     'Объем кг')])

        # -----------------------------------

        it.loc[:, (path_r[0], path_r[1], 'Итого с/c с прямыми расходами тг/кг')] = it.loc[:, (path_r[0], path_r[1],
                                                                                              'C/c мясосырья, Птицеводство тг/кг')] + \
                                                                                   it.loc[:, (path_r[0], path_r[1],
                                                                                              'Специи, добавки тг/кг')] + \
                                                                                   it.loc[:, (path_r[0], path_r[1],
                                                                                              'Упаковочный материал тг/кг')]

        # -----------------------------------

        it.loc[:, (path_r[0], path_r[1], 'Итого накладная с/с тг/кг')] = it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на убой и потрошение тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на разделку тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на охлаждение тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на заморозку тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на Индив. пакет тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на Подложку тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на Групп. Пакет тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на Маринацию тг/кг')] + \
                                                                         it.loc[:, (path_r[0], path_r[1],
                                                                                    'Затраты на Прессование тг/кг')]

        # -----------------------------------

        it.loc[:, (path_r[0], path_r[1], 'Итого с/c тг/кг')] = it.loc[:,
                                                               (path_r[0], path_r[1], 'Итого накладная с/с тг/кг')] + \
                                                               it.loc[:, (path_r[0], path_r[1],
                                                                          'Итого с/c с прямыми расходами тг/кг')]

        # Блок остатки на конец периода

        ml = pd.MultiIndex.from_tuples([('Остаток', current_month, x[2]) for x in production_for_join_ost.columns])
        arr_ost_kon = arr_ost.copy()
        arr_ost_kon = pd.DataFrame(columns=ml, index=arr_ost_kon.index)
        it = it.set_index('Артикул')
        it = pd.concat([it, arr_ost_kon], axis=1)
        it = it.reset_index()

        # -----------------------------------

        def func(x, df, filter_, col):
            return df[df['Артикул'] == x['Артикул'][0]][col].sum()

        it.loc[:, (path_ost_kon[0], path_ost_kon[1], 'Объем кг')] = it.apply(lambda x: func(x,
                                                                                            curr_balance_depot_stock_UKPF,
                                                                                            'Артикул',
                                                                                            current_month
                                                                                            ), axis=1)

        # -----------------------------------

        for item in items:
            it.loc[:, (path_ost_kon[0], path_ost_kon[1], item)] = (it.loc[:,
                                                                   (path_ost_nach[0], path_ost_nach[1], 'Объем кг')] * \
                                                                   it.loc[:,
                                                                   (path_ost_nach[0], path_ost_nach[1], item)] + \
                                                                   it.loc[:, (path_pr[0], path_pr[1], 'Объем кг')] * \
                                                                   it.loc[:, (path_pr[0], path_pr[1], item)] - \
                                                                   it.loc[:, (path_r[0], path_r[1], 'Объем кг')] * \
                                                                   it.loc[:, (path_r[0], path_r[1], item)]) / \
                                                                  (it.loc[:, (path_ost_nach[0], path_ost_nach[1],
                                                                              'Объем кг')] + it.loc[:, (path_pr[0],
                                                                                                        path_pr[1],
                                                                                                        'Объем кг')] - it.loc[
                                                                                                                       :,
                                                                                                                       (
                                                                                                                       path_r[
                                                                                                                           0],
                                                                                                                       path_r[
                                                                                                                           1],
                                                                                                                       'Объем кг')])

        # -----------------------------------

        it.loc[:, (path_ost_kon[0], path_ost_kon[1], 'Итого с/c с прямыми расходами тг/кг')] = it.loc[:, (path_ost_kon[
                                                                                                              0],
                                                                                                          path_ost_kon[
                                                                                                              1],
                                                                                                          'C/c мясосырья, Птицеводство тг/кг')] + \
                                                                                               it.loc[:, (path_ost_kon[
                                                                                                              0],
                                                                                                          path_ost_kon[
                                                                                                              1],
                                                                                                          'Специи, добавки тг/кг')] + \
                                                                                               it.loc[:, (path_ost_kon[
                                                                                                              0],
                                                                                                          path_ost_kon[
                                                                                                              1],
                                                                                                          'Упаковочный материал тг/кг')]

        # -----------------------------------

        it.loc[:, (path_ost_kon[0], path_ost_kon[1], 'Итого накладная с/с тг/кг')] = it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на убой и потрошение тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на разделку тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на охлаждение тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на заморозку тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на Индив. пакет тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на Подложку тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на Групп. Пакет тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на Маринацию тг/кг')] + \
                                                                                     it.loc[:, (path_ost_kon[0],
                                                                                                path_ost_kon[1],
                                                                                                'Затраты на Прессование тг/кг')]

        # ------------------------------------

        it.loc[:, (path_ost_kon[0], path_ost_kon[1], 'Итого с/c тг/кг')] = it.loc[:, (path_ost_kon[0], path_ost_kon[1],
                                                                                      'Итого накладная с/с тг/кг')] + \
                                                                           it.loc[:, (path_ost_kon[0], path_ost_kon[1],
                                                                                      'Итого с/c с прямыми расходами тг/кг')]

        if ind___ + 1 == mon:
            return cons_pr, it, per_1, per_2

    return cons_pr, it


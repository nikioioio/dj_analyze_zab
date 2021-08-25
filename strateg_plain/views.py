from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import pandas as pd


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
        df_amp_and_amd = request.FILES['amp_and_amd']
        df = pd.read_excel(df_amp_and_amd,sheet_name='Забой')
        # print(df)




    return JsonResponse({'status':200})





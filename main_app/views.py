from django.shortcuts import render

# Create your views here.
def starting_page(request):
    title = "Reports AKZ"
    return render(request, "main_app/main.html",context={'title':title})
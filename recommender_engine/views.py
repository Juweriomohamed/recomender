from django.shortcuts import render
def HomepageView(request):
    return render(request, 'design/home.html')
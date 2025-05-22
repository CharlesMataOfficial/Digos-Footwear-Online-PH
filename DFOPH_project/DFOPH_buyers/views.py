from django.shortcuts import render

def buyers_dashboard(request):
    return render(request, 'addtocart.html')


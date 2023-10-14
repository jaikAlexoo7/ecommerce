from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
# Create your views here.
def searchresult(request):
    query=""
    products=None
    if(request.method=="POST"):
        query=request.POST['q']
        if query:
            products=Product.objects.filter(Q(pname__icontains=query) | Q(description__icontains=query))

    return render(request,'search.html',{'p':products,'q':query})
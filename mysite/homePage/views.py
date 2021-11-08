from django.shortcuts import render

# from pathlib import Path
# import sys
  
# # directory reach
# directory = Path(__file__).resolve()
  
# # setting path
# sys.path.append(directory.parent.parent)
  
# importing
# import models
# from ..models import *
  
# using
from .models import Stock   


def homepage_view(request):
    if request.POST['submit'] == 'searchKeyword':
            keyword = request.POST['keyword']
            queryset = models.Stock.objects.get(stockname__contains = keyword)
            context = {'queryset': queryset}
            return render(request, 'homepage/homePage.html', context)


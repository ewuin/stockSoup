# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import json
#from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View  #class based views inherit from View
from django.views.generic.base import TemplateView #needed for class-view templates
from django.contrib import messages
from dal import autocomplete
import time
#from urllib.request import urlopen
import urllib2
from bs4 import BeautifulSoup as bsoup
import re
from .models import *
from .forms import *

from .cnbc_crawler import cnbc_crawler
from .bloomberg_crawler import bb_crawler
from .sentiment_script_custom import clean_article , sentiment_analysis


def landing(request):
    dow_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=DJI&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min'
    sp500_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=INX&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min'
    nasdaq_url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IXIC&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min'
    #test="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=TJ86LY8QFCFMQ44Z&datatype=json&interval=15min"

    form=searchStockForm
    context={'form':form}


    return render(request,'stockSite/landing.html',context)

def stockCrawlCNBC(request):
    stock=request.POST['stock'].strip()
    symbol=request.POST['symbol'].strip()
    print "------Stock Search CNBC -----------"
    stock_formatted=stock.replace(' ','%20')
    print stock_formatted
    html=urllib2.urlopen("https://search.cnbc.com/rs/search/view.html?source=CNBC.com&categories=exclude&partnerId=2000&pubtime=0&keywords="+stock_formatted)
    bsObj=bsoup(html,'html.parser')
    cnbc_data=cnbc_crawler(bsObj)

    return JsonResponse(cnbc_data,safe=False)


def stockCrawlBB(request):
    stock=request.POST['stock'].strip()
    symbol=request.POST['symbol'].strip()
    print "------Stock Search Bloomberg -----------"
    stock_formatted=stock.replace(' ','%20')
    print stock_formatted
    html=urllib2.urlopen("https://www.bloomberg.com/search?query="+stock_formatted)
    bsObj=bsoup(html,'html.parser')
    bb_data=bb_crawler(bsObj)

    return JsonResponse(bb_data,safe=False)

def customText(request):
    print "custom text entered"
    #print request.POST['customText']
    customText=request.POST['customText']
    clean_text=clean_article(customText)
    #print article_html has trouble printing ascii character
    article_in_array=[clean_text]
    sentiment={'sentiment':sentiment_analysis(article_in_array)}
    result=json.dumps(sentiment)
    #sentiment="test sentiment result"
    return JsonResponse(result,safe=False)

class stockSearchAutocomplete(autocomplete.Select2QuerySetView,TemplateView):
    #template_name='stockSite/landing.html'
    model=all_stock_names
    form_class=searchStockForm

    def get_queryset(self):
        qs=all_stock_names.objects.all()
        if self.q:    # responds to format http://localhost:5000/search/?q=apple
            qs=qs.filter(name__istartswith=self.q).order_by('-marketCap')
            print type(qs)
            return qs

    def post(self,request):
        try:
            print "autocomplete View POST invoked",request.POST['name']
            stockID=request.POST['name']
            stock=all_stock_names.objects.get(id=stockID)
            print stock.name
            context={'stock':stock.name, 'symbol':stock.symbol}
            return render(request,'stockSite/crawl.html',context)
        except:
            messages.add_message(request, messages.INFO, 'Please choose a valid stock.')
            return redirect('/')

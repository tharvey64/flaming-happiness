import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.base import View
from quandl.models import Quandl,Google
from markit.models import Markit

def get_variables(query_dict):
    variables = dict(code=query_dict.get('code'),
            source_code=query_dict.get('source_code'),
            start_date=query_dict.get('start date'),
            company_name=query_dict.get('company_name'))
    if not all(variables.values()):
        variables['error'] = 'Missing Input'
    return variables

class QuandlHistoryView(View):

    def get(self, request):
        # These 6 lines Check Input NOT DRY
        # Could Try all(request.GET.values())
        query_dict = get_variables(request.GET)
        if 'error' in query_dict:
            return JsonResponse(dict(error='Missing Input'))

        start_date = datetime.datetime.strptime(query_dict['start_date'], "%Y-%m-%d").date()
        stock_history = Quandl.get_dataset(query_dict['source_code'],query_dict['code'],str(start_date))
        if stock_history['error']:
            return JsonResponse(stock_history)
        else:
            return JsonResponse(dict(symbol=stock_history['symbol'],close=processed_data[::-1]))

# Todays Prices Only
class IntraDayView(View):

    def get(self,request):
        ticker = request.GET.get("ticker")
        # Find New Source
        prices = Google.get_intra_day_prices(60,1,ticker)
        return JsonResponse(prices)

# start date to current minute prices
class FullRangeView(View):
    def get(self, request):
        #######################
        #######################
        # XX CLEAN UP CSS
        # PRELOAD STOCK SEARCH WITH RESULTS
        # ADD CELERY AND RABBIT MQ TO PING TWITTER FOR TWEETS
        # DOWNLOAD THE QUANDL LIBRARY
        # DELETE MARKIT APP RENAME QUANDL APP
        #######################
        #######################
        # GET DIFF FROM PREVIOUS PRICE AND % CHANGE FROM PREVIOUS TRY TO PLOT CHANGES IN MOMENTUM 
        # DIFF, RDIFF, MOVING AVG
        # These 6 lines Check Input NOT DRY
        # THESE SHOULD ALL GO IN AS DIFFERENT HEIGHTS
        # THIS WILL BE THE FIRST IMPLEMENTATION OF THE GRAPH OPTIONS
        # PERCENT CHANGE BETWEEN 1 AND -1
        # Could Try all(request.GET.values())
        query_dict = get_variables(request.GET)
        if 'error' in query_dict:
            return JsonResponse(dict(error='Missing Input'))

        start_date = datetime.datetime.strptime(query_dict['start_date'], "%Y-%m-%d").date()
        stock_history = Quandl.get_dataset(query_dict['source_code'],query_dict['code'],str(start_date))
        
        if stock_history['error']:
             return JsonResponse(stock_history)

        daily = Google.get_intra_day_prices(60,1,stock_history['symbol'])
        if daily['error']:
            close = stock_history['prices'][::-1]
        else:
            close = stock_history['prices'][::-1]+[daily['prices'][0]]+daily['prices']
        return JsonResponse(dict(symbol=stock_history['symbol'],close=close))
from django.http import HttpResponse
from django.views import View
import json
from django.shortcuts import render
from django.http import HttpResponse
from Main import Main

def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def calcolaPeriodicityNew(probe,defaultStart,defaultEnd,defaultMeasurement):
    main=Main(probe,defaultStart,defaultEnd,defaultMeasurement)
    periodicityJSON=main.getPeriodicities()
    return HttpResponse(json.dumps(periodicityJSON), content_type="application/json")



def errorMessage():
    response_json = {}

    response_json["message"] = "Input error. Please provide valid parameters."
    return HttpResponse(json.dumps(response_json), content_type="application/json")

def errorMessageWeek():
    response_json = {}

    response_json["message"] = "Input error. Please, provide a valid time interval (no longer than a week)."
    return HttpResponse(json.dumps(response_json), content_type="application/json")



class PeriodicityIndex(View):
    def get(self,request):
        return HttpResponse("ciao")


class PeriodicityAnalyzer(View):
    def get(self, request):
        try:
            probe = int(request.GET.get('probe', None).strip())
            defaultStart=int(request.GET.get('start', None).strip())
            defaultEnd=int(request.GET.get('stop', None).strip())
            defaultMeasurement=int(request.GET.get('measurement', None).strip())
            if(defaultEnd-defaultStart<(1000+7*24*60*60)):
                outputJson=calcolaPeriodicityNew(probe,defaultStart,defaultEnd,defaultMeasurement)
            else:
                return HttpResponse(errorMessageWeek())

        except:
            return HttpResponse(errorMessage())

        return HttpResponse(outputJson)

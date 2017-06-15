from django.http import HttpResponse
from django.views import View
import json
from django.shortcuts import render
from django.http import HttpResponse

def visualize(request):
	try:
		exampleID = int(request.GET.get('exampleID', None).strip())

		if(exampleID==1):
			return render(request, 'example1.html')
		if(exampleID==2):
			return render(request, 'example2.html')
		if(exampleID==3):
			return render(request, 'example3.html')
	except:
		return HttpResponse(errorMessage())

	return HttpResponse(errorMessage())




def errorMessage():
    response_json = {}

    response_json["message"] = "Input error. Please provide valid parameters."
    return HttpResponse(json.dumps(response_json), content_type="application/json")
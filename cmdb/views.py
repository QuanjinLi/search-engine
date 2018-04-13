from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
# Create your views here.
from cmdb import models
from django.template import Context
from unit.indexing import *


invertedindex = read_index('unit/index.txt')


@csrf_exempt
def webSearch(request):
    print(request)
    search = request.POST['search']
    result = {}
    result['out'] = output(search, invertedindex)
    return_json = {"data":result}
    # return HttpResponse(json.dumps(return_json), content_type='application/json')
    return render(request, "webSearch.html", result)

@csrf_exempt
def home(request):
    return render(request, "home.html")


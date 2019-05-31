from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
import blog.tool as tool
import blog.models as models


def test(request):
    return render(request, 'test.html')


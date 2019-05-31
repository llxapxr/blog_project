from django.shortcuts import render
from django.http.response import JsonResponse
import blog.tool as tool


def message(request):
    return render(request, 'message.html')

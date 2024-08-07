# from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views import View
import cv2
import numpy as np
from wsgiref.util import FileWrapper
from .models import Query
from django.template import loader


def index(request):
    #Query.objects.all().delete()
    search_query = request.GET.get('text')
    if search_query is None:
        query_list = Query.objects.all()
        template = loader.get_template("ticker/index.html")
        context = {
            "query_list": query_list,
        }
        return HttpResponse(template.render(context, request))


    new_query = Query(query_text=search_query)
    new_query.save()
    create_ticker(search_query)
    return FileResponse(open('ticker.mp4', 'rb'), as_attachment=True)

def querylist(request):
    query_list = Query.objects.all()
    template = loader.get_template("ticker/index.html")
    context = {
        "query_list": query_list,
    }
    return HttpResponse(template.render(context, request))


def create_ticker(string):
    width, height = 100, 100
    time = 3
    frame_per_second = 24
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("ticker.mp4", fourcc, frame_per_second, (width, height))
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    font_scale = 1
    font_thickness = 1
    font_color = 0
    font = cv2.QT_FONT_NORMAL
    message_size = cv2.getTextSize(string, font, font_scale, font_thickness)
    x, y = width, height // 2

    while x + message_size[0][0] > 0:
        x -= (width + message_size[0][0]) // time // frame_per_second
        frame.fill(255)
        cv2.putText(frame, string, (x, y), font, font_scale, font_color, font_thickness)
        out.write(frame)
    out.release()

# Create your views here.

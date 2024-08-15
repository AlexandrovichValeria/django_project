# from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views import View
import cv2
import numpy as np
from wsgiref.util import FileWrapper
from .models import Query
from django.template import loader
from PIL import ImageFont, ImageDraw, Image


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


def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)


def create_ticker(string):
    width, height = 100, 100
    time = 3
    frames_per_second = 24
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("ticker.mp4", fourcc, frames_per_second, (width, height))
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_frame = Image.fromarray(frame)

    font = ImageFont.truetype("./arial.ttf", 25)
    draw = ImageDraw.Draw(pil_frame)
    message_size = get_text_dimensions(string, font)
    x, y = width, (height - message_size[1]) // 2

    while x + message_size[0] > 0:
        x -= (width + message_size[0]) / (time * frames_per_second)
        draw.rectangle([(0,0), (width, height)], fill=(255, 255, 255))
        draw.text((x, y), string, fill=(0, 0, 0), font=font)
        frame = np.asarray(pil_frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

    out.release()

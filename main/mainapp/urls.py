from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import path, reverse
from django.shortcuts import render


import random
from collections import defaultdict
import os
from django.shortcuts import redirect

import io
import logging
import json
from geopy import distance


from .forms import UploadForm


SHORT_DIST_DELIVERY = 10
LONG_DIST_DELIVERY = 1500

with open("../coord_reserch/i2c", "r") as f:
    index2coord = json.load(f)

with open("../coord_reserch/p2a", "r") as f:
    index2addr = json.load(f)

suggest = {
    0: "Использовать услугу быстрой доставки",
    1: "Использовать услугу 'ускоренное'",
    2: "Использовать услугу 'sms для получателя'",
    3: "Использовать услугу 'Онлайн оплата наложенного платежа'",
    4: "Выставить галочку 'Отправлять посылку с наложенным платежом только с описью'",
    5: "Нету предложений"
}


def check_type_short(delivery_data):
    """Check short distance delivery"""
    index_from = delivery_data["индекс отправителя"]
    index_to = delivery_data["индекс получателя"]
    try:
        coord_from = index2coord[index_from][::-1]
        coord_to = index2coord[index_to][::-1]
        dist = distance.distance(coord_from, coord_to).km
        return dist <= SHORT_DIST_DELIVERY
    except:
        return False


def check_type_long(delivery_data):
    """Check long distance delivery"""
    index_from = delivery_data["индекс отправителя"]
    index_to = delivery_data["индекс получателя"]
    try:
        coord_from = index2coord[index_from][::-1]
        coord_to = index2coord[index_to][::-1]
        dist = distance.distance(coord_from, coord_to).km
        return dist >= LONG_DIST_DELIVERY
    except:
        return False


def check_oc(delivery_data):
    try:
        oc = delivery_data["сумма ОЦ (руб)"]
        return oc > 0
    except:
        return False


def check_np(delivery_data):
    try:
        np = delivery_data["сумма НП (руб)"]
        return np > 0
    except:
        return False


def sms_rec(delivery_data):
    try:
        sms = delivery_data["sms для получателя"]
        return sms == True
    except:
        return False


def check_save(delivery_data):
    try:
        save = delivery_data["отметка 'Осторожно'"]
        return save == True
    except:
        return False


def check_fast(delivery_data):
    try:
        fast = delivery_data["ускоренное"]
        return fast == True
    except:
        return False


def check_weight(delivery_data):
    try:
        weight = delivery_data["ускоренное"]
        return weight
    except:
        return 0


def check_opis(delivery_data):
    try:
        opis = delivery_data["с описью вложений"]
        return opis
    except:
        return False


def full_choise(delivery_data):
    return {
        "check_type_short": check_type_short(delivery_data),
        "check_type_long": check_type_long(delivery_data),
        "check_oc": check_oc(delivery_data),
        "check_np": check_np(delivery_data),
        "sms_rec": sms_rec(delivery_data),
        "check_save": check_save(delivery_data),
        "check_fast": check_fast(delivery_data),
        "check_weight": check_weight(delivery_data),
        "check_opis": check_opis(delivery_data),
    }


def get_suggest(delivery_data):
    ans_suggest = []
    choise = full_choise(delivery_data)
    if choise["check_type_short"]:
        ans_suggest.append(suggest[0])
    elif choise["check_type_long"]:
        if not choise["sms_rec"]:
            ans_suggest.append(suggest[2])
        if not choise["check_fast"]:
            ans_suggest.append(suggest[1])
    elif choise["check_np"]:
        ans_suggest.append(suggest[3], suggest[4])
    if not ans_suggest:
        ans_suggest.append(suggest[5])
    return ans_suggest


def upload_data(request):
    if request.method == "POST":
        try:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                data = json.load(io.BytesIO(request.FILES['file'].read()))
                logging.info("Succes upload")
        except BaseException as e:
            logging.error(f"Exception {e}")
            redirect("/")
        ans = {}
        for index, delivery_data in data.items():
            ans[index] = get_suggest(delivery_data)
        return render(request, "suggest.html", ans)
    else:
        form = UploadForm
        return render(request, "upload_data.html", {"form": form})
    return redirect("/")


def about_us(request):
    return render(request, "about_us.html")

urlpatterns = [
    path("", upload_data, name="upload_data"),
    path("about_us", about_us, name="about_us")
]

from email.headerregistry import Address
from importlib import resources
from multiprocessing import context
from operator import truediv
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import date, datetime, timedelta
import json
# Create your views here.

today = date.today().strftime("%d/%m/%Y")
# today = "13/03/2022"
seven_days_before = date.today() - timedelta(days=7)


def hello(request):
    return HttpResponse('hello')


def total(request):
    sum_of_unit_in_use = 0
    sum_of_unit_available = 0
    response1_sum_of_qurantine = 0
    data_consistent =False
    data_inconsistent =False
    try:
        response1 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
            {"resource": "http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv", "section": 1, "format": "json", "filters": [[1, "eq", [today]]]})}).json()
        response1_access_endpoint = True
        for i in response1:
            sum_of_unit_in_use += i["Current unit in use"]
            sum_of_unit_available += i["Ready to be used (unit)"]
            response1_sum_of_qurantine += i["Current person in use"]
    except:
        response1_access_endpoint = False
    try:
        response2 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
        {"resource": "http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv", "section": 1, "format": "json", "sorts": [[8, "desc"]], "filters": [[1, "eq", ["13/03/2022"]]]})}).json()
        centre1_name= response2[0]["Quarantine centres"]
        centre1_units_avalable = response2[0]["Ready to be used (unit)"]
        centre2_name= response2[1]["Quarantine centres"]
        centre2_units_avalable = response2[1]["Ready to be used (unit)"]
        centre3_name= response2[2]["Quarantine centres"]
        centre3_units_avalable = response2[2]["Ready to be used (unit)"]
    except:
        centre1_name= None
        centre1_units_avalable = 0
        centre2_name= None
        centre2_units_avalable = 0
        centre3_name= None
        centre3_units_avalable = 0
    try:
        response3 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
            {"resource": "http://www.chp.gov.hk/files/misc/no_of_confines_by_types_in_quarantine_centres_eng.csv", "section": 1, "format": "json", "filters": [[1, "eq", [today]]]})}).json()
        response3_access_endpoint = True
        number_of_close_contact=response3[0]["Current number of close contacts of confirmed cases"]
        number_of_non_close_contact = response3[0]["Current number of non-close contacts"]
    except:
        response3_access_endpoint = False
        number_of_close_contact= 0
        number_of_non_close_contact = 0
    response4 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
        {"resource": "http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv", "section": 1, "format": "json", "filters": [[1, "eq", [seven_days_before.strftime("%d/%m/%Y")]]]})}).json()
    response5 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
        {"resource": "http://www.chp.gov.hk/files/misc/no_of_confines_by_types_in_quarantine_centres_eng.csv", "section": 1, "format": "json", "filters": [[1, "eq", [seven_days_before.strftime("%d/%m/%Y")]]]})}).json()
    # print(response4)
    # print(response2[0]["Quarantine centres"])
    if not response4 and not response5:
        seven_days_alert = True
    else:
        seven_days_alert = False
    if not (response1_access_endpoint and response3_access_endpoint):
        access_endpoint_alert = True
    else:
        access_endpoint_alert = False
    if access_endpoint_alert == False:
        if (response3[0]["Current number of close contacts of confirmed cases"] + response3[0]["Current number of non-close contacts"]) == response1_sum_of_qurantine:
            data_consistent =True
        else:
            data_inconsistent= True
    print(access_endpoint_alert)
    # print(sum_of_unit_available)
    context = {"quarantine": [
    {
        "today":today
    },
    {
        "sum_of_unit_in_use": sum_of_unit_in_use
    },
    {
        "sum_of_unit_available": sum_of_unit_available
    },
    {
        "centre1_name": centre1_name,
        "centre1_units_avalable": centre1_units_avalable
    },
    {
        "centre2_name": centre2_name,
        "centre2_units_avalable": centre2_units_avalable
    },
    {
        "centre3_name": centre3_name,
        "centre3_units_avalable": centre3_units_avalable
    },
    {
        "response3_sum_of_quarantine": number_of_close_contact,
        "total_non_close_contacts": number_of_non_close_contact
    },
    {
        "data_consistent": data_consistent,
        "data_inconsistent": data_inconsistent
    },
    {
        "seven_days_alert": seven_days_alert
    },
    {
        "access_endpoint_alert": access_endpoint_alert
    }]}
    # print(context)
    return render(request, 'view_all.html', context=context)

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
seven_days_before =  date.today() - timedelta(days=7)

def hello(request):
    return HttpResponse('hello')


def total(request):
    response1 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
        {"resource": "http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv", "section": 1, "format": "json", "filters": [[1, "eq", [today]]]})}).json()
    response2 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
        {"resource":"http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv","section":1,"format":"json","sorts":[[8,"desc"]],"filters":[[1,"eq",["13/03/2022"]]]})}).json()
    response3 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps({"resource":"http://www.chp.gov.hk/files/misc/no_of_confines_by_types_in_quarantine_centres_eng.csv","section":1,"format":"json","filters":[[1,"eq",[today]]]})}).json()
    response4 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps(
        {"resource": "http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv", "section": 1, "format": "json", "filters": [[1, "eq", [seven_days_before.strftime("%d/%m/%Y")]]]})}).json()
    response5 = requests.get('https://api.data.gov.hk/v2/filter', params={'q': json.dumps({"resource":"http://www.chp.gov.hk/files/misc/no_of_confines_by_types_in_quarantine_centres_eng.csv","section":1,"format":"json","filters":[[1,"eq",[seven_days_before.strftime("%d/%m/%Y")]]]})}).json()
    sum_of_unit_in_use = 0
    sum_of_unit_available = 0
    response1_sum_of_qurantine = 0
    # print(response4)
    # print(response2[0]["Quarantine centres"])
    for i in response1:
        sum_of_unit_in_use += i["Current unit in use"]
        sum_of_unit_available += i["Ready to be used (unit)"]
        response1_sum_of_qurantine += i["Current person in use"]
    if (response3[0]["Current number of close contacts of confirmed cases"]+ response3[0]["Current number of non-close contacts"])==response1_sum_of_qurantine :
        data_consistent =True
    else:
        data_consistent= False
    if not response4 and not response5:
        seven_days_alert = True
    else:
        seven_days_alert = False
    if not response1 and not response3:
        access_endpoint_alert = True
    else:
        access_endpoint_alert = False
    # print(sum_of_unit_in_use)
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
        "centre1_name": response2[0]["Quarantine centres"],
        "centre1_units_avalable": response2[0]["Ready to be used (unit)"]
    },
    {
        "centre2_name": response2[1]["Quarantine centres"],
        "centre2_units_avalable": response2[1]["Ready to be used (unit)"]
    },
    {
        "centre3_name": response2[2]["Quarantine centres"],
        "centre3_units_avalable": response2[2]["Ready to be used (unit)"]
    },
    {
        "response3_sum_of_quarantine": response3[0]["Current number of close contacts of confirmed cases"],
        "total_non_close_contacts": response3[0]["Current number of non-close contacts"]
    },
    {
        "data_consistent": data_consistent
    },
    {
        "seven_days_alert": seven_days_alert
    },
    {
        "access_endpoint_alert": access_endpoint_alert
    }]}
    # print(context)
    return render(request, 'view_all.html', context=context)

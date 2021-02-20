import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection

def complete_orders(request):
    if request.method = 'GET':

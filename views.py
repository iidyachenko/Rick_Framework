import datetime
from framework import render


def main_view(request):
    secret = request.get('secret_key', None)
    date = datetime.datetime.today()
    return '200 OK', render('index.html', data=date.strftime("%A %d %B %Y"))


def about_view(request):
    return '200 OK', render('contacts.html')

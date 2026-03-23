from django.http import HttpResponse
import datetime

def greeting(request):
    return HttpResponse(f"Hello, its a note app. Now: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
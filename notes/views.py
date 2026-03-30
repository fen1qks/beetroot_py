from django.http import HttpResponse

from django.shortcuts import render

from notes.models import Categories

def show_headers(request):
    headers = request.META
    html = "<h1>HTTP-заголовки запиту</h1><table border='1'>"
    html += "<tr><th>Заголовок</th><th>Значення</th></tr>"

    for key, value in headers.items():
        if key.startswith("HTTP_"):
            header_name = key[5:].replace('_', '-').title()
            html += f"<tr><td>{header_name}</td><td>{value}</td></tr>"
    html += "</table>"
    return HttpResponse(html)


def notes_list(request):
    notes = [
        {
            'name': 'Name 1',
            'time': "10.03.2026",
            'description': 'Description 1'
        },
        {
            'name': 'Name 2',
            'time': '11.03.2026',
            'description': 'Description 2'
        }
    ]
    return render(request, 'index.html', {'notes': notes})

def notes_from_db(request):
    categories = Categories.objects.prefetch_related('notes').all()
    return render(request, 'notes.html', {'categories': categories})
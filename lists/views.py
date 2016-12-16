from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST':
        return HttpResponse(request,
                            'home.html',
                            {'new_item_text': request.POST['item_text']}
                            )
    return render(request, 'home.html')

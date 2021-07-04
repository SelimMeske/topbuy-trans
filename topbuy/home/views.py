from django.shortcuts import render
from topbuy.translate_script import Translator_Jomi
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home/home.html')


def translate(request):

    if request.method == 'POST':
        print(request.POST['original_text'])

        ts = Translator_Jomi(request.POST['original_text'], "hr")

        ts.clean_a()
        ts.clean_strong()
        ts.translations()

        translated = ts.text

        return JsonResponse({'data': translated})

    # return render(request, 'home/translate.html', {'translated_response': translated, 'original_response': original})
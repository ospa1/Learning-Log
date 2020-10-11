from django.shortcuts import render


# Create your views here.
def index(request):
    """ Hompage """
    return render(request, 'learning_logs/index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# register a new user
def register(request):

    # gets a new form with no data
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        # process the completed form
        form = UserCreationForm(data=request.POST)

        # if its valid save it
        if form.is_valid():
            new_user: UserCreationForm = form.save()

            # login the user and return to home screen
            login(request, new_user)
            return redirect('learning_logs:index')

    # display the blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)

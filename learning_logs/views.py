from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from learning_logs.models import Topic
from .forms import TopicForm, EntryForm
from .models import Topic, Entry


def index(request):
    """ Hompage """
    return render(request, 'learning_logs/index.html')


# shows all topics
@login_required
def topics(request):

    all_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': all_topics}
    return render(request, 'learning_logs/topics.html', context)


# shows entries for a topic
@login_required
def topic(request, topic_id):

    a_topic = Topic.objects.get(id=topic_id)

    # Make sure the topic belongs to the current user.
    if a_topic.owner != request.user:
        raise Http404

    entries = a_topic.entry_set.order_by('-date_added')
    context = {'topic': a_topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


# adds a new topic
@login_required
def new_topic(request):

    # returns a blank form if its a GET or other request
    if request.method != 'POST':
        form = TopicForm()
    # if its a POST request
    else:
        form = TopicForm(data=request.POST)
        # checks if the data is valid (text length < 200 from models.py)
        if form.is_valid():
            # assign an owner first then save to database
            a_new_topic = form.save(commit=False)
            a_new_topic.owner = request.user
            a_new_topic.save()  # write to database
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


# adds a new entry for a topic
@login_required
def new_entry(request, topic_id):

    a_topic = Topic.objects.get(id=topic_id)

    # if no data is submitted return blank form
    if request.method != 'POST':
        form = EntryForm()
    # process data from POST
    else:
        form = EntryForm(data=request.POST)
        # if its valid save it
        if form.is_valid():
            """ create a new entry object without saving it to the database
                so we can set the topic. then we call the save function again
                to store it in the database.
            """
            new_entry_object = form.save(commit=False)
            new_entry_object.topic = a_topic
            new_entry_object.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # display blank or invalid form
    context = {'topic': a_topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


# edit a specific entry
@login_required
def edit_entry(request, entry_id):

    print("editing entry")
    # get the entry fro the database
    entry = Entry.objects.get(id=entry_id)
    entry_topic = entry.topic

    # Make sure the topic belongs to the current user.
    if entry_topic.owner != request.user:
        raise Http404

    print(request)
    if request.method != 'POST':
        # fill the form with the current entry
        print('not in post')
        form = EntryForm(instance=entry)
    else:
        """
            These arguments tell django to create a form instance based on the
            information associated with the existing entry object, 
            updated with any relevant data from request.POST
        """
        print('in post')
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect('learning_logs:topic', topic_id=entry_topic.id)
        else:
            print('form is not valid')

    context = {'entry': entry, 'topic': entry_topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

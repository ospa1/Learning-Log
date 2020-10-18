from django.shortcuts import render, redirect

# Create your views here.
from learning_logs.models import Topic
from .forms import TopicForm, EntryForm


def index(request):
    """ Hompage """
    return render(request, 'learning_logs/index.html')


# shows all topics
def topics(request):

    all_topics = Topic.objects.order_by('date_added')
    context = {'topics': all_topics}
    return render(request, 'learning_logs/topics.html', context)


# shows entries for a topic
def topic(request, topic_id):

    topic = Topic.objects.get(id=topic_id)  # todo rename variable so it doesnt collide with function name
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


# adds a new topic
def new_topic(request):

    # returns a blank form if its a GET or other request
    if request.method != 'POST':
        form = TopicForm()
    # if its a POST request
    else:
        form = TopicForm(data=request.POST)
        # checks if the data is valid (text length < 200 from models.py)
        if form.is_valid():
            form.save()  # write to database
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


# adds a new entry for a topic
def new_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)

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
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # display blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

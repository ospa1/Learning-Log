from django.shortcuts import render


# Create your views here.
from learning_logs.models import Topic


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

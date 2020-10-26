from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Topic(models.Model):

    """ A topic a user is learning about """

    # Create text and date field
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    # if a user is deleted all of user's topic will be deleted
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):

    """ Specifically learned about a topic"""

    # on_delete=models.CASCADE arg will  delete all entries when a topic is deleted
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    # Create text and date field
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # Tells Django to use Entries when it needs to refer to more than one entry
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        # will only show the first 50 chars of an entry
        # ellipsis clarifies that we are not always displaying the entire entry
        return f"{self.text[:50]}..."

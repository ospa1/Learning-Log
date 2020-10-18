from django import forms
from .models import Topic, Entry


# creates a form for users to add a topic
class TopicForm(forms.ModelForm):
    # tells django which model to base the form on and which fields to include in the form
    class Meta:

        # build form from the Topic model
        model = Topic

        # only has a text field
        fields = ['text']

        # no label for the text field
        labels = {'text': ''}


# creates a form for users to add an entry
class EntryForm(forms.ModelForm):
    # tells django which model to base the form on and which fields to include in the form
    class Meta:
        # build from the Entry model
        model = Entry
        fields = ['text']

        # entry label for the text field
        labels = {'text': 'Entry:'}

        # text area with 80 columns - default is 40
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

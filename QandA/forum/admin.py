from django.contrib import admin
from .models import Question, Answer, Vote, Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Tag)
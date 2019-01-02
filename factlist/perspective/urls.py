from django.urls import path

from .views import ListAndCreateTopicView, TopicView, CreateLinkView, TagLinkView, ListTagsOfTopic, \
    RemoveTagFromLinkView

urlpatterns = [
    path('topics/', ListAndCreateTopicView.as_view()),
    path('topics/<int:pk>/', TopicView.as_view()),
    path('topics/<int:pk>/links/', CreateLinkView.as_view()),
    path('topics/<int:topic_pk>/links/<int:pk>/tags/', TagLinkView.as_view()),
    path('topics/<int:pk>/tags/', ListTagsOfTopic.as_view()),
    path('topics/<int:topic_pk>/links/<int:link_pk>/tags/<int:tag_pk>/', RemoveTagFromLinkView.as_view()),
]
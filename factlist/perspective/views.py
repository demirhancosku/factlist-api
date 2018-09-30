from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from factlist.claims.models import Link
from .serializers import TopicSerializer, CreateTopicSerializer, TitleSerializer, TagSerializer, LinkSerializer
from .models import Topic, TopicLink, Tag, LinkTag


class ListAndCreateTopicView(ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        # Returning topics that contains links
        topic_ids = list(TopicLink.objects.filter().values_list('topic_id', flat=True))
        return Topic.objects.filter(id__in=topic_ids).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TopicSerializer
        else:
            return CreateTopicSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateTopicSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            topic = Topic.objects.create(
                user=user,
                title=serializer.data["title"],
            )
            if "link" in serializer.data:
                link_object = Link.objects.create(link=serializer.data["link"], user=self.request.user)
                TopicLink.objects.create(link=link_object, topic=topic)
            return Response(TopicSerializer(topic).data, status=status.HTTP_201_CREATED)


class TopicView(RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        if self.request.method == "GET":
            return Topic.objects.filter(id=self.kwargs["pk"])
        else:
            return Topic.objects.filter(id=self.kwargs["pk"], user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TopicSerializer
        else:
            return CreateTopicSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TitleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if "title" in serializer.data:
                instance.title = serializer.data["title"]
                instance.updated_at = timezone.now()
                instance.save()
            return Response(TopicSerializer(instance).data, status=status.HTTP_200_OK)


class CreateLinkView(ListCreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        TopicLink.objects.create(topic_id=self.kwargs["pk"], link_id=serializer.data["id"])

    def get_queryset(self):
        link_ids = list(TopicLink.objects.filter(topic_id=self.kwargs["pk"]).values_list("link_id", flat=True))
        return Link.objects.filter(id__in=link_ids)


class TagLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TitleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.data['title']
            tags = Tag.objects.filter(title=title)
            if tags.exists():
                tags = tags.first()
            else:
                tags = Tag.objects.create(title=title, topic_id=self.kwargs['topic_pk'])
            LinkTag.objects.create(link_id=self.kwargs['pk'], tag=tags)
            return Response(TagSerializer(tags).data, status=status.HTTP_201_CREATED)


class ListTagsOfTopic(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(topic_id=self.kwargs['pk'])


class RemoveTagFromLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        link = Link.objects.filter(id=self.kwargs['link_pk'])
        if link.exists():
            if link.first().user != self.request.user:
                return Response({'Not found'}, status=status.HTTP_404_NOT_FOUND)
        linktag = LinkTag.objects.filter(link_id=self.kwargs['link_pk'], tag_id=self.kwargs['tag_pk'])
        if linktag.exists():
            linktag.delete()
            return Response({'Tag removed successfully'}, status=status.HTTP_200_OK)
        return Response({'Not found'}, status=status.HTTP_404_NOT_FOUND)

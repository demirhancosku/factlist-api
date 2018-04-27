from ast import literal_eval

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
from django.core.validators import URLValidator

from factlist.users.serializers import SimpleUserSerializer
from .models import Claim, Evidence, File, Link


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('file', 'id')


class LinkSerializer(serializers.ModelSerializer):
    embed = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ('link', 'embed')

    def get_embed(self, link):
        return cache.get(link.link)


class CreateEvidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evidence
        fields = (
            'id',
            'text',
            'status',
        )

    def create(self, validated_data):
        request = self.context['request']
        if not 'links' in request.POST and not "files" in request.FILES:
            raise ValidationError("Claim must contain at least a file or link")
        evidence = Evidence()
        if "text" in validated_data:
            evidence.text = validated_data.pop("text")
        if "status" in validated_data:
            evidence.status = validated_data.pop("status")
        claim_id = self.context['claim_id']
        evidence.user = request.user
        evidence.claim_id = claim_id
        evidence.save()
        if 'links' in request.POST:
            links = literal_eval(request.POST['links'])
            for link in links:
                try:
                    validate = URLValidator()
                    validate(link)
                except:
                    raise ValidationError({"links": "Invalid link"})
                link_object = Link.objects.create(link=link)
                evidence.links.add(link_object)
        if 'files' in request.FILES:
            files = request.FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                evidence.files.add(file_object.id)
        else:
            pass
        evidence.save()
        return evidence

    def update(self, instance, validated_data):
        request = self.context["request"]
        if "text" in validated_data:
            instance.text = validated_data.pop("text")
        if "status" in validated_data:
            instance.status = validated_data.pop("status")
        if 'links' in request.POST:
            instance.links.all().delete()
            links = literal_eval(request.POST['links'])
            for link in links:
                link_object = Link.objects.create(link=link)
                instance.links.add(link_object)
        if 'files' in request.FILES:
            instance.files.all().delete()
            files = request.FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                instance.files.add(file_object.id)
        instance.save()
        return instance


class EvidenceSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    files = FileSerializer(many=True)
    links = LinkSerializer(many=True)

    class Meta:
        model = Evidence
        fields = (
            'id',
            'text',
            'status',
            'created_at',
            'updated_at',
            'deleted_at',
            'user',
            'links',
            'files',
        )


class CreateClaimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        fields = (
            'id',
            'text',
        )

    def create(self, validated_data):
        claim = Claim.objects.create(**validated_data)
        request = self.context["request"]
        if not 'links' in request.POST and not "files" in request.FILES:
            raise ValidationError("Claim must contain at least a file or link")
        if 'links' in request.POST:
            links = literal_eval(request.POST['links'])
            for link in links:
                try:
                    validate = URLValidator()
                    validate(link)
                except:
                    raise ValidationError({"links": "Invalid link"})
                link_object = Link.objects.create(link=link)
                claim.links.add(link_object)
        if 'files' in request.FILES:
            files = request.FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                claim.files.add(file_object.id)
        claim.save()
        return claim

    def update(self, instance, validated_data):
        if "text" in validated_data:
            instance.text = validated_data.pop("text")

        request = self.context['request']
        if 'links' in request.POST:
            instance.links.all().delete()
            links = literal_eval(request.POST['links'])
            for link in links:
                link_object = Link.objects.create(link=link)
                instance.links.add(link_object)
        if 'files' in request.FILES:
            instance.files.all().delete()
            files = request.FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                instance.files.add(file_object.id)
        instance.save()
        return instance


class ClaimSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    files = FileSerializer(many=True)
    links = LinkSerializer(many=True)
    evidences = EvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Claim
        fields = (
            'id',
            'text',
            'user',
            'created_at',
            'updated_at',
            'deleted_at',
            'evidences',
            'links',
            'files',
            'true_count',
            'false_count',
            'inconclusive_count'
        )

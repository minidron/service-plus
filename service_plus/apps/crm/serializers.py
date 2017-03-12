from rest_framework import serializers

from crm.models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('title', 'price')

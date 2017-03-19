from rest_framework import serializers

from crm.models import Job, SparePart, SparePartCount


class SparePartSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('field_count')

    class Meta:
        model = SparePart
        fields = (
            'id',
            'title',
            'brand_id',
            'model_id',
            'purchase_price',
            'retail_price',
            'count',
        )

    def field_count(self, obj):
        return obj.spare_part_counts.count()


class SparePartCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePartCount
        fields = (
            'id',
            'booking_id',
            'spare_part_id',
            'title',
            'brand_id',
            'model_id',
            'purchase_price',
            'retail_price',
        )


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job

        fields = (
            'id',
            'title',
            'price',
        )

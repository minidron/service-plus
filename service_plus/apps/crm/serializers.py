from rest_framework import serializers

from crm.models import Guarantee, Job, SparePart, SparePartCount


class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = (
            'id',
            'title',
        )


class SparePartSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('field_count')
    guarantee = GuaranteeSerializer()

    class Meta:
        model = SparePart
        fields = (
            'id',
            'title',
            'brand_id',
            'model_id',
            'purchase_price',
            'retail_price',
            'guarantee',
            'count',
        )

    def field_count(self, obj):
        return obj.spare_part_counts.count()


class SparePartCountSerializer(serializers.ModelSerializer):
    guarantee = GuaranteeSerializer()

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
            'guarantee',
        )


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job

        fields = (
            'id',
            'title',
            'price',
        )

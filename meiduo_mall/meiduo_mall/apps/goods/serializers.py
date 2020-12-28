from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer

from .search_indexes import SKUIndex
from .models import SKU


class SKUSerializer(serializers.ModelSerializer):
    """
    SKU 序列化器
    """

    class Meta:
        model = SKU
        fields = [
            'id', 'name', 'price', 'default_image_url', 'comments'
        ]



class SKUIndexSerializer(HaystackSerializer):
    """
    haystack使用的序列化器 , SKU索引结果数据序列化器
    """
    # object = SKUSerializer(read_only=True)

    class Meta:
        index_classes = [SKUIndex]
        fields = ('text', 'id', 'name', 'price', 'default_image_url', 'comments')
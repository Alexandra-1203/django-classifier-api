from rest_framework import serializers
from .models import Category, Brand, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']
    def validate(self, data):
        if self.instance and data.get('parent') and data['parent'].id == self.instance.id:
            raise serializers.ValidationError("Нельзя сделать категорию родителем самой себя")
        return data

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
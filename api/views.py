from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        """Удалить категорию с переподвешиванием потомков"""
        category = self.get_object()
        parent = category.parent
        
        with transaction.atomic():
            # Переподвешиваем всех детей к родителю удаляемой категории
            category.children.update(parent=parent)
            # Удаляем категорию
            category.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def descendants(self, request, pk=None):
        """Все потомки (с уровнями вложенности)"""
        category = self.get_object()
        descendants = self._get_descendants_with_level(category)
        return Response(descendants)

    @action(detail=True, methods=['get'])
    def parents(self, request, pk=None):
        """Все предки"""
        category = self.get_object()
        parents = []
        while category.parent:
            parents.append(category.parent)
            category = category.parent
        serializer = CategorySerializer(parents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def change_parent(self, request, pk=None):
        """Переместить к новому родителю с проверкой на циклы"""
        category = self.get_object()
        new_parent_id = request.data.get('parent')
        
        if new_parent_id is None:
            return Response({'error': 'parent is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(new_parent_id) == category.id:
            return Response({'error': 'Cannot set parent to itself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверка на циклы
        if self._would_create_cycle(category.id, int(new_parent_id)):
            return Response({'error': 'This move would create a cycle'}, status=status.HTTP_400_BAD_REQUEST)
        
        category.parent_id = new_parent_id
        category.save()
        return Response({'status': 'ok'})

    @action(detail=True, methods=['get'])
    def terminals(self, request, pk=None):
        """Все листовые категории в поддереве"""
        terminals = self._get_terminals(self.get_object())
        serializer = CategorySerializer(terminals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Все продукты в этой категории"""
        products = Product.objects.filter(category_id=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # ---------- вспомогательные методы ----------
    def _get_descendants_with_level(self, category, level=0):
        result = [{'id': category.id, 'name': category.name, 'level': level}]
        for child in category.children.all():
            result.extend(self._get_descendants_with_level(child, level + 1))
        return result

    def _get_terminals(self, category):
        if not category.children.exists():
            return [category]
        terminals = []
        for child in category.children.all():
            terminals.extend(self._get_terminals(child))
        return terminals

    def _would_create_cycle(self, category_id, new_parent_id):
        """Проверка, не создаст ли перемещение цикла"""
        current = Category.objects.get(id=new_parent_id)
        while current.parent:
            if current.parent.id == category_id:
                return True
            current = current.parent
        return False

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def parents(self, request, pk=None):
        """Получить всех предков (категории) продукта"""
        product = self.get_object()
        category = product.category
        parents = []
        while category:
            parents.append(category)
            category = category.parent
        serializer = CategorySerializer(parents, many=True)
        return Response(serializer.data)
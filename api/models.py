from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100, db_column='название')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='родитель_id',
        related_name='children'
    )

    def delete(self, *args, **kwargs):
        # Переназначить все продукты текущей категории её родителю
        if self.parent:
            Product.objects.filter(category=self).update(category=self.parent)
        else:
            # Если родителя нет, обнулить категорию (или можно оставить как есть)
            Product.objects.filter(category=self).update(category=None)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'категория'
        managed = False
    
    

class Brand(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_марка')
    name = models.CharField(max_length=100, db_column='марка')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'марка'
        managed = False


class Product(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_продукт')
    name = models.CharField(max_length=200, db_column='название')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='цена')
    unit = models.CharField(max_length=20, db_column='ед_измерения')
    status = models.CharField(max_length=50, db_column='состояние')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column='id_марка')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_категория')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'продукт'
        managed = False
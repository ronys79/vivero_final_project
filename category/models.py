from django.db import models

class Category(models.Model):
    category_name   = models.CharField(max_length=50, unique=True)
    slug            = models.SlugField(max_length=100, unique=True)
    description     = models.TextField(max_length=300, blank=True)
    cat_image      = models.ImageField(upload_to='photos/categories', blank=True)

# Changes on admin panel categorys to categories, spelling fixer and adjuster for admin panel.
# If change anything dont forget to migrate it to db

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


from django.db import models

# Create your models here.


from django.db import models
from django.conf import settings

from django.contrib.auth.models import User


class allergenlist(models.Model):
    id = models.AutoField(primary_key=True)  # Using AutoField for primary key
    allergen = models.TextField(null=True, blank=True)  # TextField for text
    ingredientList = models.TextField(null=True, blank=True)  # JSONField for array of text

    def __str__(self):
        return self.allergen

    class Meta:
        db_table = 'allergenlist' 
# class CustomUser(AbstractUser):
#     allergens = models.ManyToManyField(allergenlist, blank=True)
class UserAllergen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allergen = models.ForeignKey(allergenlist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'allergen')

class recipe(models.Model):
    id = models.AutoField(primary_key=True)  # Using AutoField for primary key
    item_name = models.TextField(null=True, blank=True)  # TextField for text
    ingredient = models.TextField(null=True, blank=True)  # JSONField for array of text
    diet = models.TextField(null=True, blank=True)  # TextField for text
    flavour = models.TextField(null=True, blank=True)  # TextField for text
    state = models.TextField(null=True, blank=True)  # TextField for text
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.item_name

    class Meta:
        db_table = 'recipe'



class stateNames(models.Model):
    id = models.AutoField(primary_key=True)
    states = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.states

    class Meta:
        db_table = 'stateNames'








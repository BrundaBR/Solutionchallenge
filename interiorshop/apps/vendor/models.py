from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from PIL import Image
from django.dispatch import receiver

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)



    class Meta: 
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='vendor/profile_pics')
#     userpaypal=models.CharField(max_length=30)


#     def __str__(self):
#         return f'{self.user.username} Profile'

#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         super().save(force_insert, force_update, using, update_fields)

#         img = Image.open(self.image.path)

#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

    

# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         created,user_profile = Profile.objects.create(user=kwargs['instance'])
#         pass

# post_save.connect(create_profile, sender=User)

class User_location(models.Model):
    lat=models.IntegerField()
    long=models.IntegerField()
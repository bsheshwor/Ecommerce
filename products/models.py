from django.db import models 
from django.urls import reverse
import random
import os
from django.db.models.signals import pre_save,post_save
from .utils import unique_slug_generator

# Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance,filename):
    new_filename = random.randit(1,39102938273)
    name,ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)
    
    def all(self):
        return self.get_queryset().active()
    
    def featured(self):
        return self.filter(featured=True,active = True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using = self._db)
    def features(self):
        return self.get_queryset().featured()
    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None




class Product(models.Model):
    title = models.CharField(max_length = 120)
    slug = models.SlugField(blank = True,unique=True)
    description =models.TextField()
    price = models.DecimalField(max_digits = 10,decimal_places = 2,default = 344)
    image =models.ImageField(upload_to="products" ,null=True,blank = True)
    featured = models.BooleanField(default =False )
    active = models.BooleanField(default = True )
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail",kwargs={"slug":self.slug})

    def __str__(self):
        return self.title 
    
    def __unicode__(self):
        return self.title

def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver,sender = Product)    



    


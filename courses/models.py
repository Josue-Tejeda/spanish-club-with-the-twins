from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User

class Subject(models.Model):
    title = models.CharField(max_length=255)
    
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
        )
    
    subject = models.ForeignKey(
        Subject,
        related_name='courses_created',
        on_delete=models.CASCADE
        )
    
    title = models.CharField(max_length=255)
    
    slug = models.SlugField(max_length=255, unique=True)
    
    overview = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE
        )
    
    title = models.CharField(max_length=255)
    
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
    
    
class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
        )
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': (
                'text',
                'video',
                'image',
                'file'
            )
        }
        )
    
    object_id = models.PositiveIntegerField()
    
    item = GenericForeignKey('content_type', 'object_id')
    
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
        

class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
        )
    
    title = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()

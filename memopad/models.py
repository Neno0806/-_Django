from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save

import sys
sys.path.append('../')
from accounts.models import Profile

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name
    
class Memo(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'メモのデータ'

@receiver(post_delete,sender=Memo)#postがdeleteされたらdelete_mypostが実行される
def delete_mypost(sender,instance,**kwargs):
    profile1 = Profile.objects.get(pk=instance.user.id)
    profile1.mypost1.remove(str(instance.pk))
    profile1.save()

@receiver(post_save,sender=Memo)
def append_mypost(sender,instance,created,**kwargs):
    profile1 = Profile.objects.get(pk=instance.user.id)
    if created:
        if instance.item.pk == 1:
            profile1.mypost1.insert(0,str(instance.pk))
        profile1.save()
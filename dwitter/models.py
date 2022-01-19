from django.db import models
from django.contrib.auth.models import User # genişletmek istediğimiz user modelini içe aktardık
from django.db.models.signals import post_save
from django.dispatch import receiver




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True) 
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        #user_profile = Profile(user=instance, follows=[instance]) # çoktan çoğa bir kümenin ön tarafına doğrudan atama yasaktır. bunun yerine Follow.set() kullan.
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile) 
        user_profile.save()

#post_save.connect(create_profile, sender=User)



class Dweet(models.Model):
    user = models.ForeignKey(User, related_name='dweets', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (
            f'{self.user}'
            f'({self.created_ad:%Y-%m-%d %H:%M}):'
            f'{self.body[:30]}...'
        )















"""
Her kullanıcının her zaman kendisiyle ilişkilendirilmiş bir profili olmasını istediğiniz için, Django'yu bu görevi sizin için yapacak şekilde ayarlayabilirsiniz.
Her yeni kullanıcı oluşturduğunuzda, Django uygun kullanıcı profilini de otomatik olarak oluşturmalıdır.
Ayrıca, hemen o kullanıcı ile ilişkilendirilmelidir. Bunu bir sinyalmodels.py kullanarak uygulayabilirsiniz .
"""
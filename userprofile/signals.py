from django.db.models import signals
from django.contrib.auth.models import User
from userprofile.models import UserProfile

def createProfile(sender, **kwargs):
  user = kwargs["instance"]
  if kwargs["created"]:
    profile = UserProfile(user=user, displayname=user.username)
    profile.save()

signals.post_save.connect(createProfile, sender=User, dispatch_uid="users-profilecreation-signal")

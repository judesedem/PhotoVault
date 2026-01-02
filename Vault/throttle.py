from django.core.cache import cache
from rest_framework.throttling import UserRateThrottle

class PhotoRequestThrottle(UserRateThrottle):
   scope='photo'



    
   
from rest_framework import throttling
from django.core.cache import cache

class PhotoRequestThrottle(throttling.BaseThrottle):
   
    
    def allow_request(self, request, view):
      
        if 'photo' not in request.path.lower():
            return True
        
       
        if request.user and request.user.is_authenticated:
            user_id = f"photo_throttle_user_{request.user.id}"
        else:
            user_id = f"photo_throttle_ip_{self.get_ident(request)}"
        
       
        request_count = cache.get(user_id, 0)
        
       
        if request_count >= 3:
            return False
        
       
        cache.set(user_id, request_count + 1, timeout=None)
        
        return True
    
    def wait(self):
       
        return 15
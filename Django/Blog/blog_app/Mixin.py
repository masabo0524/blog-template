from django.contrib.auth.mixins import UserPassesTestMixin

class OnlySuperUserMixin(UserPassesTestMixin):
    raise_exception = True
    
    def test_func(self):
        return self.request.user.is_superuser

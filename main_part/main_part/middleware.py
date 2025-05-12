from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, request):
        #if check authenticated is here
        if request.user.is_authenticated:
            #path doesn't here that user
            paths_to_redirect=[reverse('blog:register'),reverse('blog:login')]

            if request.path in paths_to_redirect:
                return redirect(reverse('blog:index')) #redirect to index is authendiated user
        response=self.get_response(request)
        return response
    

#if unAuthenticated redirect to login
class RestrictUnauthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        restrict_paths=[reverse('blog:dashboard')]

        if not request.user.is_authenticated and request.path in restrict_paths:
            return redirect(reverse('blog:login'))
    
        response=self.get_response(request)
        return response

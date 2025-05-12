from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
# logging
import logging
from django.contrib.auth.models import User

from django.http import Http404
from django.core.paginator import Paginator
from . forms import PostForm, contact_form,registerForm,loginForm,forgotPassword,ResetPsswordForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
#token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required,permission_required

#grups and permissions
from django.contrib.auth.models import Group


            # static data using demo
# posts=[
#         {'id':1,'title':'post1','content':'this is post 1'},
#         {'id':2,'title':'post2','content':'this is post 2'},
#         {'id':3,'title':'post3','content':'this is post 3'},
#         {'id':4,'title':'post4','content':'this is post 4'},
#     ]

# Create your views here.

def index(request):
    all_posts=Post.objects.filter(is_published=True)
    #pagination
    paginator=Paginator(all_posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'index.html',{'page_obj':page_obj})

def detail(request,slug):
    #static data
    # post=next((item for item in posts if item['id']==int(post_id)),None)

    #permission checks
    if request.user and not request.user.has_perm('sub_part.view_post'):
        messages.error(request,'you have no permission to view the Post')
        return redirect('blog:index')
    #handling the error
    try:
        #getting data in model by post id
        post=Post.objects.get(slug=slug)
        # showing related category post
        related_post=Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("this page doesn't exists")
    
#    debuging line check 
    # logger=logging.getLogger("TESTING")
    # logger.debug(f'post variable is {post}')
    return  render(request,"detail.html",{'post':post,'related_post':related_post})

def old_url(request):
    return redirect("new_page_url")

def new_url(request):
    return HttpResponse("this is new url page")

def contact_view(request):
    if request.method=="POST":
        form=contact_form(request.POST)
        logger=logging.getLogger("TESTING")
        #to set template VALUE
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')

        if form.is_valid():
            #debuging line check 
            logger.debug(f'post contact is {form.cleaned_data['name']}{form.cleaned_data['email']}{form.cleaned_data['message']}')
            # messages.error(request,"form sent Successfully!",extra_tags='success')
            message_sent="Form sent successfully"
            return render(request,'contact.html',{'message_sent':message_sent})

        else:
            logger.debug("contact validation failed")
        return render(request,'contact.html',{'form':form,'name':name,'email':email,'message':message})
    return render(request,'contact.html')

def about_view(request):
    about_content=aboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content="content not Available"
    else:
        about_content=about_content.content
    return render(request,'about.html',{'about_content':about_content})

def register(request):
    form=registerForm()
    if request.method=='POST':
        form=registerForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) #prevent before save data into database
            user.set_password(form.cleaned_data['password']) #password Hashing
            user.save()
            #add user default to groups 
            readers_group,created=Group.objects.get_or_create(name='Readers')
            user.groups.add(readers_group)
            print('user added the roup successfully')

            # print("register data success")
            messages.error(request,"Register success ! you can Login")
            return redirect('/login')
    return render(request,'register.html',{'form':form})

def login(request):
    form=loginForm()
    if request.method=="POST":
        form=loginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                print("user login success")
                return redirect('/dashboard')
            # print("data sent login form")

    return render(request,'login.html',{'form':form})

def dashsboard(request):
    blog_title="My Posts"
    all_posts=Post.objects.filter(user=request.user)
      #pagination
    paginator=Paginator(all_posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'dashboard.html',{'blog_title':blog_title,'all_posts':all_posts,'page_obj':page_obj})

def logout(request):
    auth_logout(request)
    return redirect("/")

def forgot_password(request):
    form=forgotPassword()
    if request.method=="POST":
        form=forgotPassword(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            current_site=get_current_site(request)
            domain=current_site.domain
            subject="RESET PASSWORD REQUESTED"
            message=render_to_string('reset_password_email.html',{
                'domain':domain,
                'uid':uid,
                'token':token
            })
            send_mail(subject,message,"noreply@ham.com",[email])
            messages.success(request,"email has been sent")

    return render(request,'forgot_password.html',{'form':form})

def reset_password(request,uidb64,token):
    form=ResetPsswordForm()
    if request.method=="POST":
        form=ResetPsswordForm(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(NameError,ValueError,User.DoesNotExist):
                user=None
            if user is  not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,"your new password reset successfully")
                return redirect('blog:login')
            else:
                messages.success(request,"invalid reset password form")
                
    return render(request,'reset_password.html',{'form':form})

@login_required
@permission_required('sub_part.add_post',raise_exception=True)
def new_post(request):
    form=PostForm()
    categories=category.objects.all()
    if request.method=="POST":
        print("POST entered")
        #forms
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            print("form is valid")
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('blog:dashboard')
    return render(request,'new_post.html',{'categories':categories,'form':form})

@login_required
@permission_required('sub_part.change_post',raise_exception=True)
def edit_post(request, post_id):
    categories=category.objects.all()
    post=get_object_or_404(Post,id=post_id)
    # form
    form=PostForm(request.POST,request.FILES,instance=post)
    if request.method=="POST":
        if form.is_valid():
            post.save()
            messages.success(request,"your post edited succesfully!")
            return redirect('blog:dashboard')
    return render(request,'edit_post.html',{'categories':categories,'post':post})

@login_required
@permission_required('sub_part.delete_post',raise_exception=True)
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.delete()
    messages.success(request,"your post deleted succesfully!")
    return redirect('blog:dashboard')

@login_required
@permission_required('sub_part.can_publish',raise_exception=True)
def publish_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.is_published=True
    post.save()
    messages.success(request,'Post Published Successfully')
    return redirect('blog:dashboard') 
    



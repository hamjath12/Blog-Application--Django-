from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


#categories
class category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    img_url=models.ImageField(null=True,upload_to="posts/images")
    created_at=models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    is_published=models.BooleanField(default=False)

    # def save(self, *args,**kwargs): 
    #     self.slug=slugify(self.title)
    #     super().save(*args,**kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not already set
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    # img url http or static folder works
    @property
    def formatted_img_url(self):
        url=self.img_url if self.img_url.__str__().startswith(("http://","https://")) else self.img_url.url
        return url


    def __str__(self):
        return self.title

class aboutUs(models.Model):
    content=models.TextField()
  
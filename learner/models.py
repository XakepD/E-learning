from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models import Avg
from ckeditor_uploader.fields import RichTextUploadingField 
import secrets


from .paystack import PayStack
# Create your models here.

"""
class Post(models.Model):
    header = models.CharField(max_length=100, default="Header")
    text = models.TextField()

    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.header}: {self.average_rating()}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.header}: {self.rating}"
# Create your models here.
"""
class Dp(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture= models.ImageField(upload_to='media/profile_pic',null=True,blank=True)
    
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture= models.ImageField(upload_to='media/profile_pic',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    Company = models.CharField(max_length=100,null=False, blank=True)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = True, null=True)
    title = models.CharField(max_length=100) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=True)
    logo = models.ImageField(upload_to='media/catlogo', blank=True, null=True, help_text='Optional')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title

    def post_count(self):
        return self.courses.all().count()    

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])    
    
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField(null=True)
    descrption = models.TextField(max_length=500, null=True)
    learning_objective_1 = models.CharField(max_length=500)
    learning_objective_2 = models.CharField(max_length=500)
    learning_objective_3 = models.CharField(max_length=500)
    display_image = models.ImageField(upload_to='media/courseimage', blank=True, null=True, help_text='Optional', default='media/avi.png')
    @property
    def display_image_url(self):
        if self.display_image and hasattr(self.display_image, 'url'):
            return self.display_image.url
    def average_rating(self) -> float:
        return Rating.objects.filter(course=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.title}: {self.average_rating()}"
    
    
    def __str__(self):
        return self.title
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course.title}: {self.rating}"
class Section(models.Model):
    course =  models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
class CourseContent(models.Model):
    section= models.ForeignKey(Section, on_delete=models.CASCADE)
    lesson= models.CharField(max_length=200) 
    video = models.FileField(upload_to='media/coursevideo', blank=True)
    article = RichTextUploadingField(blank=True)
    def __str__(self):
        return self.section.name
    @property
    def html_stripped(self):
       from django.utils.html import strip_tags
       return strip_tags(self.article)

    
class promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount = models.FloatField()
    active = models.BooleanField()

    def __str__(self):
        return self.code
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def totalcost(self):
        return self.course.price
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
class CourseAnnoucement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    announcement = RichTextField()
    def __str__(self) :
        return self.course.title 
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review = models.TextField()


class Payment(models.Model):
    
    amount = models.PositiveIntegerField()
    email = models.EmailField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            self.paystack_response = result
            if result["amount"] / 100 == self.amount:
                self.completed = True
            self.save()
            return True
        return False
class Testimonials(models.Model):
    full_name = models.CharField(max_length=200)
    testimonial = models.TextField()
    image = models.ImageField(upload_to='media/testimonials')
    bio = models.CharField(max_length=300)
    def __str__(self):
        return self.full_name
class Coupon(models.Model):
    code = models.CharField(max_length=100)
    percent_off = models.PositiveIntegerField()
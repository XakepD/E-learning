from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as loginUser, update_session_auth_hash
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from .forms import *
from django.urls import reverse_lazy
from django.db import transaction
from . forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
import random
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  


"""def signup(request):  
    if request.method == 'POST':  
        form = CreateUserForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('student/activate.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send(fail_silently=False)  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = CreateUserForm()  
    return render(request, 'student/signup.html', {'form': form})  

def activate(request, uidb64, token):  
    user = User()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 

"""
#ALL
def about(request):
    cartitems = 0
    
    latest = Course.objects.all()[6:]
    popular = Course.objects.all()[:8]
    cat = Category.objects.all()
    tstm = Testimonials.objects.all()
    
    if request.user.is_authenticated:
          order = Order.objects.filter(user=request.user)
          cartitems = len(Cart.objects.filter(user= request.user))
          w = len(WishList.objects.filter(user=request.user))
    
    return render(request , 'all/about.html', locals())
def home(request):
    cartitems = 0
    
    latest = Course.objects.all()[6:]
    popular = Course.objects.all()[:8]
    cat = Category.objects.all()
    allc = Course.objects.all()
    num_entities = Course.objects.all().count()
    rand_entities = random.sample(range(num_entities), 3)
    samp = Course.objects.filter(id__in=rand_entities)
    if request.user.is_authenticated:
          order = Order.objects.filter(user=request.user)
          cartitems = len(Cart.objects.filter(user= request.user))
          w = len(WishList.objects.filter(user=request.user))
    
    return render(request , 'all/home.html', locals())
def km(request):
    cartitems = 0
    
    l = len(Course.objects.all())
    latest = Course.objects.all()[l-8:]
    popular = Course.objects.all()[:8]
    allc = Course.objects.all()
    cat = Category.objects.all()
    
    if request.user.is_authenticated:
          order = Order.objects.filter(user=request.user)
          cartitems = len(Cart.objects.filter(user= request.user))
          w = len(WishList.objects.filter(user=request.user))
    
    return render(request , 'all/km.html', locals())
def signup(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('studentlogin')
			

		context = {'form':form}
		return render(request, 'student/signup.html', context)

	

def signin(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="student/login.html", context={"login_form":form})
def cat(request):
     cat = Category.objects.all()
     return render(request, 'all/header.html', {'cat':cat})
def Courseview(request):
        cartitems = 0
        
        cat = Category.objects.all()
        if request.user.is_authenticated:
          cartitems = len(Cart.objects.filter(user= request.user))
          w = len(WishList.objects.filter(user=request.user))
        courses = Course.objects.all()
        context = {'courses':courses, 'cartitems':cartitems, 'cat':cat}
        return render(request, 'all/courses.html', context)
class Coursedetail(View):
    
    def get(self, request, pk):
       cartitems = 0
       
       cat= Category.objects.all
       order = Order.objects.filter(user=request.user)
       ordr = Order.objects.filter(course_id=pk)
       for orders in order:
            if orders.course.id == pk:
                 a = 'in'
            else:
                 a = 'out'
       
       if request.user.is_authenticated:
          cartitems = len(Cart.objects.filter(user= request.user))
          w = len(WishList.objects.filter(user=request.user))
       course = Course.objects.get(pk=pk)

       return render (request, 'all/details.html', locals())
class Filter(View):
      def get(self, request):
            cat = Category.objects.all()
            search = request.GET['search']
            courses = Course.objects.filter(title__contains = search ) | Course.objects.filter(categories__title__contains = search )
            return render(request, 'all/filter.html', locals())

@login_required(login_url='studentlogin')
def addtocart(request):
      user= request.user
      course_id = request.GET.get('course_id')
      course = Course.objects.get(id = course_id)
      cart = Cart.objects.filter(user=user)
      
      if course.price == 0 :
        Order(user=user, course=course).save()
        return redirect('home')
      else:
           if Cart.objects.filter(id=course_id).exists():
                return redirect('cart')
           else:
                Cart(user=user, course=course).save()
                return redirect('cart')

           
     
@login_required(login_url='studentlogin')
def showcart(request):
      cartitems = 0
      
      cat = Category.objects.all()
      if request.user.is_authenticated:
          cartitems = len(Cart.objects.filter(user= request.user))
          w = len(WishList.objects.filter(user=request.user))
      user = request.user
      items = Cart.objects.filter(user=user)
      tprice = 0
      for p in items:
            value = p.course.price
            tprice = tprice + value
      return render(request, 'student/cart.html', locals())
def addcoupon(request):
     coupon_code= "FgBn"
     code = Coupon.objects.all()
     if coupon_code in code:
          a = "hdhdh"
          return redirect('cart')
     

def removeitem(request):
      if request.method == "GET":
            course_id = request.GET.get('course_id')
            c = Cart.objects.filter(Q(course = course_id) & Q(user = request.
						user))
            c.delete()
            user = request.user
            items= Cart.objects.filter(user=user)
            tprice = 0
            for p in items:
                  value = p.course.price
                  tprice = tprice+value
            data={
                  'tprice':tprice
						}
            return JsonResponse(data)
@login_required(login_url='studentlogin')
def Takecourse(request, pk):
            
            course= Course.objects.get(pk=pk)
            allcourses = get_object_or_404(Course, pk=pk)
            section = Section.objects.filter(course = course)
            section1 =  Section.objects.filter(pk = pk)
            content =  CourseContent.objects.filter(section__course = course)
            review = Review.objects.filter(course=course)
            announcement = CourseAnnoucement.objects.filter(course=course)
            artic = CourseContent.objects.filter(section__course = course)[:1]
            
            return render(request, 'student/lesson.html', locals())
def Tutorial(request, pk):
            content = CourseContent.objects.get(pk=pk)
            sections = Section.objects.get(id = content.section.id)
            course = Course.objects.get(id=sections.course.id) 
            review = Review.objects.filter(course=course)
            section = Section.objects.filter(course=course)
            announcement = CourseAnnoucement.objects.filter(course=course)
            contents = CourseContent.objects.filter(section__course= course)
            a = 0
            
            return render(request, 'student/tutorial.html', locals())
def Reviews( request, pk):
      
      course = Course.objects.get(pk=pk)
      user = request.user
      form = ReviewForm(initial={'user':user, 'course':course})
      if request.method =="POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                  form.save()
                  return redirect('home')
      return render(request, 'student/review.html', locals())
#TUTOR


def tutorboard(request):
    user = request.user
    course = Course.objects.filter(user=user)
    lcourse = len(course)
    return render(request , 'tutor/dashboard.html', locals())

def index(request: HttpRequest) -> HttpResponse:
    courses = Course.objects.all()
    for course in courses:
        rating = Rating.objects.filter(course=course, user=request.user).first()
        course.user_rating = rating.rating if rating else 0
    return render(request, "all/index.html", {"courses": courses})

def rate(request: HttpRequest, course_id: int, rating: int) -> HttpResponse:
    course = Course.objects.get(id=course_id)
    Rating.objects.filter(course=course, user=request.user).delete()
    course.rating_set.create(user=request.user, rating=rating)
    return index(request)
def courseupload(request):
    user=request.user
    course= CourseForm(initial={'user':request.user})
    if request.method=='POST':
        course =CourseForm(request.POST, request.FILES)
        if course.is_valid():
            course .save()
        messages.success(request, "course  Added Sucessfully !!")    
        return redirect('tutorcourses')
    return render(request, "tutor/courseupload.html", {'course':course, 'user': user})
def courseedit(request,pk):
    cours= Course.objects.get(pk=pk)
    course = CourseForm(instance=cours)
    if request.method=='POST':
        course =CourseForm(request.POST, request.FILES, instance=cours)
        if course.is_valid():
            course.save()
        messages.success(request, "course  Added Sucessfully !!")    
        return redirect('tutorcourses')
    return render(request, "tutor/courseupload.html", {'course':course})
            

      
def review(request):
     user = request.user
     course = Course.objects.filter(user=user)
     context = {'course':course}
     for l in course:
          lrating = len(Rating.objects.filter(course=l))
          lreview = len(Review.objects.filter(course=l))
     return render(request, 'tutor/review.html', locals())
def tutorprofileedit(request):
      profile = User.objects.get(username=request.user)
      form = ProfileForm(instance=profile)
      dp = DpForm(initial={'user':request.user})
      user = request.user
      if request.method =='POST':
            
            form = ProfileForm(request.POST or None , instance=profile)
            dp = DpForm(request.POST)
            if form.is_valid() | dp.is_valid():
                  form.save()
                  
                  
                  return redirect('tutor-edit')
      return render(request, 'tutor/editprofile.html', locals())


def announcement(request):
      form = AnnouncementForm()
      if request.method == "POST":
            form = AnnouncementForm()
            if form.is_valid():
                  form.save()
                  messages.success(request, "Announcement  Added Sucessfully !!")
            return redirect('announcements')

      return render(request, 'tutor/announcement.html', {'form':form})
def announcements(request):
      user = request.user
      course = Course.objects.filter(user=user)
      announce = CourseAnnoucement.objects.all()
      return render(request, 'tutor/announcements.html', locals())
def TutorCourseview(request):
        user= request.user
        courses = Course.objects.filter(user=user)
        context = {'courses':courses}
        return render(request, 'tutor/courses.html', context)
def content(request,pk):
      cours =  Course.objects.get(pk=pk)
      course = CourseForm(instance=cours)
      formset = ContentFormSet(request.POST or None)
      if request.method=='POST':
            if formset.is_valid():
                  formset.instance = cours
                  formset.save()
                  return redirect('content')
      return render(request, 'tutor/content.html', locals())
def sectionadd(request,pk):
      course = Course.objects.get(pk=pk)
      section = Section.objects.filter(course=course)
      content = CourseContent.objects.filter(section__course=course)
      sectionl1 = len(section) 
      sectionl2 = sectionl1 + 1
      form = SectionForm(initial={"course":course})
      if request.method == "POST":
            form = SectionForm(request.POST)
            if form.is_valid():
                  form.save()
            return redirect('sections' , pk=pk)
      return render(request,'tutor/sections.html', locals())
class SectionInline():
    form_class = SectionForm
    model = Section
    template_name = "tutor/content.html"
    frm = AnnouncementForm()
    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('tutorcourses')

    def formset_content_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        contents = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for content in contents:
            content.section = self.object
            content.save()



class SectionCreate(SectionInline, CreateView):
    

    def get_context_data(self, **kwargs):
        ctx = super(SectionCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'contents': ContentFormSet(prefix='contents'),
                
            }
        else:
            return {
                'contents': ContentFormSet(self.request.POST or None, self.request.FILES or None, prefix='contents'),
                
            }

    
class SectionUpdate(SectionInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(SectionUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'contents': ContentFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='contents'),
            
        }




def delete_content(request, pk):
    try:
        content = CourseContent.objects.get(id=pk)
    except CourseContent.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('section', pk=content.section.id)

    content.delete()
    messages.success(
            request, 'content deleted successfully'
            )
    return redirect('content', pk=content.section.id)

def tutorprofile(request):
     return render(request, 'tutor/profile.html')


#STUDENT
def profileedit(request):
      profile = User.objects.get(username=request.user)
      form = ProfileForm(instance=profile)
      dp = DpForm()
      user = request.user
      if request.method =='POST':
            
            form = ProfileForm(request.POST or None , instance=profile)
            dp = DpForm(request.POST)
            if form.is_valid() & dp.is_valid():
                  form.save()
                  dp.save()
                  
                  return redirect('tutorboard')
                  
      return render(request, 'student/editprofile.html', locals())

def deletecourse(request, pk):
    course = get_object_or_404(Course, pk=pk).delete()
    return redirect('tutorcourses')



"""class SectionList(ListView):
    model = Section
class Contentadd(CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'tutor/content.html'
    success_url = reverse_lazy('sections')

    def get_context_data(self, **kwargs):
        data = super(Contentadd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contents'] = ContentFormSet(self.request.POST)
        else:
            data['contents'] = ContentFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        contents = context['contents']
        with transaction.atomic():
            self.object = form.save()

            if contents.is_valid():
                contents.instance = self.object
                contents.save()
        return super(Contentadd, self).form_valid(form)
"""

def studentprofile(request):
     return render(request, 'student/profile.html')
def studentcourses(request):
     order = Order.objects.filter(user=request.user)
     return render(request, 'student/courses.html', locals())

def addtowish(request):
      user= request.user
      course_id = request.GET.get('course_id')
      course = Course.objects.get(id = course_id)
      
     
      WishList(user=user, course=course).save()
      return redirect('details', pk=course_id)

def wishlist(request):
     latest = WishList.objects.filter(user=request.user)
     return render(request, 'student/wishlist.html', locals())
def studentdashboard(request):
     return render(request, 'student/dashboard.html')
def catg(request,cslug):
     cat = Category.objects.all()
     catg = Category.objects.get(slug=cslug)
     catuse = get_object_or_404(Category, slug=cslug)
     courses = Course.objects.filter(categories=catuse)
     return render(request,'all/catg.html', locals())
def initiate_payment(request: HttpRequest) -> HttpResponse:
    cartitems = 0
    
    if request.user.is_authenticated:
          cartitems = len(Cart.objects.filter(user= request.user))
          w = len(WishList.objects.filter(user=request.user))
          user = request.user
          items = Cart.objects.filter(user=user)
          tprice = 0
          for p in items:
            value = p.course.price
            tprice = tprice + value
    payment_form = PaymentForm(initial={"amount":tprice})

    form = ContentForm()
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment: Payment = payment_form.save()
            return render(request, 'student/make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = PaymentForm(initial={"amount":tprice , "email": user.email})
    return render(request, "student/initiate_payment.html", {"payment_form": payment_form, "form": form, "items": items, "tprice": tprice})

def verify_payment(request, ref: str):
    trxref = request.GET["trxref"]
    if trxref != ref:
        messages.error(
            request,
            "The transaction reference passed was different from the actual reference. Please do not modify data during transactions",
        )
    payment: Payment = get_object_or_404(Payment, ref=ref)
    if payment.verify_payment():
        messages.success(
            request, f"Payment Completed Successfully, NGN {payment.amount}."
        )
        messages.success(
            request, f"Your new credit balance is GNGN {payment.user.credit}."
        )
    else:
        messages.warning(request, "Sorry, your payment could not be confirmed.")
    return redirect("initiate-payment")

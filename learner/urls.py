from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import views as auth_view
from .views import *
from .forms import *
urlpatterns = [
    path('home', views.home, name ="home"),
    path('about', views.about, name ="about"),
    path('km', views.km, name ="km"),
    path('courses', views.Courseview, name ="courses"),
    path('cart', views.showcart, name='cart'),
    path('rate/<int:post_id>/<int:rating>/', views.rate),
    path('index', views.index),
    path('sections/<int:pk>', views.sectionadd, name='sections'), 
    path('catg/<slug:cslug>', views.catg, name='catg'), 
    path('delete/<int:pk>', views.deletecourse, name='delete'),
    path('search', views.Filter.as_view(), name ="search"),
    path('delete-content/<int:pk>/', delete_content, name='delete_content'),
    path('details/<int:pk>', views.Coursedetail.as_view(), name='details'),
    path('add-to-cart/', views.addtocart,name='add-to-cart'),
    path('add-to-wish/', views.addtowish,name='add-to-wish'),
    path('remove-item',views.removeitem),
    path('review/<int:pk>', views.Reviews, name='review'), 
path('wishlist/', views.wishlist,name='wishlist'),

    path('tutor/courses', views.TutorCourseview, name ="tutorcourses"),
    path('tutor-dashboard', views.tutorboard, name ="tutorboard"),
    path('tutor/course-edit/<int:pk>', views.courseedit, name ="courseedit"),
    path('tutor/announcement', views.announcement, name ="announcement"),
    path('tutor/announcements', views.announcements, name ="announcements"),
    path('tutor/profile', views.tutorprofile, name ="tprofile"),
    path('tutor/content/<int:pk>/', SectionUpdate.as_view(), name='content'),
    path('tutor/course-upload', views.courseupload, name ="courseupload"),
    path('tutor/reviews', views.review, name='reviews'), 
    path('tutor/profile-edit', views.tutorprofileedit, name ="tutor-edit"),
    path('student/profile-edit', views.profileedit, name ="profile-edit"),
    path('lessons/<int:pk>', views.Tutorial , name='lessons'),
   
    path('student/lesson/<int:pk>', views.Takecourse, name ="lesson"),
    path('student/profile', views.studentprofile, name ="sprofile"),
    path('student/courses', views.studentcourses, name ="scourses"),
    path('student/dashboard', views.studentdashboard, name ="sdashboard"),
    
    
    
    
    #path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  activate, name='activate'),

    path('register', views.signup, name ="studentsignup"),
    path('login', views.signin, name ="studentlogin"),
    path('logout', LogoutView.as_view(template_name='all/logout.html'),name='logout'),
    path('password-change', auth_view.PasswordChangeView.as_view(template_name='all/pswdchange.html', form_class= PasswordChangeForm, success_url='/password-change/complete'),name='pswdchange'),
    path('tutor/password-change', auth_view.PasswordChangeView.as_view(template_name='tutor/pswdchange.html', form_class= PasswordChangeForm, success_url='tutor/password-change/complete'),name='tpswdchange'),
    path('tutor/password-change/complete', auth_view.PasswordChangeDoneView.as_view(template_name='tutor/pswdc.html'),name='tpswdchangedone'),
    path('password-reset', auth_view.PasswordResetView.as_view(template_name='all/pswdreset.html', form_class= PasswordResetForm),name='pswdreset'),
    path('password-reset/done', auth_view.PasswordResetDoneView.as_view(template_name='all/pswddone.html'),name='pswddone'),
    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='all/pswdconfirm.html', form_class = SetMyPasswordForm),name='pswdconfirm'),
    path('password-reset-complete', auth_view.PasswordResetCompleteView.as_view(template_name='all/pswdcomplete.html'),name='pswdcomplete'),
    path('', views.initiate_payment, name="initiate-payment"),
    path('<str:ref>/', views.verify_payment, name="verify-payment"),
    
]
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
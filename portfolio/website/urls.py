from django.urls import path
from django.contrib.sitemaps.views import sitemap

from website import views
from website.sitemaps import PortfolioSitemap, BlogSitemap


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('resume/', views.resume, name='resume'),
    path('experience/', views.experience, name='experience'),
    path('education/', views.education, name='education'),
    path('certifications/', views.certifications, name='certifications'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('sitemap.xml', sitemap, {'sitemaps': {'portfolio': PortfolioSitemap, 'blog': BlogSitemap}}, name='sitemap'),
]

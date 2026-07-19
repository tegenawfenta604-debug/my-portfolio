from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from website.models import (
    Profile, SocialLink, Skill, Service, Category, Project, Experience,
    Education, Certification, Testimonial, BlogCategory, Tag, Post,
    Comment, Contact, FAQ,
)
from website.forms import ContactForm, CommentForm


def home(request):
    profile = Profile.objects.select_related('user').first()
    featured_projects = Project.objects.filter(featured=True)[:3]
    skills = Skill.objects.all()
    services = Service.objects.all()[:6]
    testimonials = Testimonial.objects.all()[:6]
    recent_posts = Post.objects.filter(published=True)[:3]
    stats = {
        'projects': Project.objects.count(),
        'experience': Experience.objects.count(),
        'clients': Testimonial.objects.count(),
        'certifications': Certification.objects.count(),
    }
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'skills': skills,
        'services': services,
        'testimonials': testimonials,
        'recent_posts': recent_posts,
        'stats': stats,
    }
    return render(request, 'website/home.html', context)


def about(request):
    profile = Profile.objects.select_related('user').first()
    skills = Skill.objects.all()
    return render(request, 'website/about.html', {'profile': profile, 'skills': skills})


def skills(request):
    skills = Skill.objects.all()
    return render(request, 'website/skills.html', {'skills': skills})


def services(request):
    services = Service.objects.all()
    return render(request, 'website/services.html', {'services': services})


def projects(request):
    category_slug = request.GET.get('category')
    queryset = Project.objects.all()
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        queryset = queryset.filter(category=active_category)
    projects = queryset
    return render(request, 'website/projects.html', {
        'projects': projects,
        'active_category': active_category,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    return render(request, 'website/project_detail.html', {'project': project, 'related': related})


def resume(request):
    profile = Profile.objects.select_related('user').first()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    certifications = Certification.objects.all()
    skills = Skill.objects.all()
    return render(request, 'website/resume.html', {
        'profile': profile,
        'experiences': experiences,
        'educations': educations,
        'certifications': certifications,
        'skills': skills,
    })


def experience(request):
    experiences = Experience.objects.all()
    return render(request, 'website/experience.html', {'experiences': experiences})


def education(request):
    educations = Education.objects.all()
    return render(request, 'website/education.html', {'educations': educations})


def certifications(request):
    certifications = Certification.objects.all()
    return render(request, 'website/certifications.html', {'certifications': certifications})


def blog(request):
    queryset = Post.objects.filter(published=True).prefetch_related('tags', 'category')
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    query = request.GET.get('q')
    active_category = None
    active_tag = None
    if category_slug:
        active_category = get_object_or_404(BlogCategory, slug=category_slug)
        queryset = queryset.filter(category=active_category)
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags=active_tag)
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query))
    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent = Post.objects.filter(published=True)[:5]
    return render(request, 'website/blog.html', {
        'page_obj': page_obj,
        'recent': recent,
        'active_category': active_category,
        'active_tag': active_tag,
        'query': query,
    })


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    Post.objects.filter(pk=post.pk).update(views=post.views + 1)
    comments = post.comments.filter(approved=True)
    related = Post.objects.filter(published=True, category=post.category).exclude(pk=post.pk)[:3]
    if not related:
        related = Post.objects.filter(published=True).exclude(pk=post.pk)[:3]
    recent = Post.objects.filter(published=True).exclude(pk=post.pk)[:5]
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment is awaiting moderation.')
            return redirect(post.get_absolute_url())
    return render(request, 'website/blog_detail.html', {
        'post': post,
        'comments': comments,
        'related': related,
        'recent': recent,
        'comment_form': comment_form,
    })


def contact(request):
    form = ContactForm(request.POST or None)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        Contact.objects.create(name=cd['name'], email=cd['email'], subject=cd.get('subject', ''), message=cd['message'])
        try:
            send_mail(
                subject=f"New Contact: {cd.get('subject') or cd['name']}",
                message=f"From: {cd['name']} <{cd['email']}>\n\n{cd['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_TO_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        if is_ajax:
            return JsonResponse({'success': True, 'message': 'Thanks! Your message has been sent successfully.'})
        messages.success(request, 'Thanks! Your message has been sent successfully.')
        return redirect('contact')
    if is_ajax and request.method == 'POST':
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return render(request, 'website/contact.html', {'form': form})


def testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'website/testimonials.html', {'testimonials': testimonials})


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'website/faq.html', {'faqs': faqs})


def privacy(request):
    return render(request, 'website/privacy.html', {})


def handler404(request, exception=None):
    return render(request, 'website/404.html', {}, status=404)

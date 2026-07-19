from website.models import (
    Profile, SocialLink, Category, BlogCategory, Service, Skill, FAQ,
)


def site_context(request):
    profile = Profile.objects.select_related('user').first()
    return {
        'site_profile': profile,
        'social_links': SocialLink.objects.all(),
        'hero_socials': SocialLink.objects.filter(
            platform__in=['github', 'linkedin', 'twitter', 'email', 'telegram', 'phone']
        ),
        'project_categories': Category.objects.all(),
        'blog_categories': BlogCategory.objects.all(),
        'nav_services': Service.objects.all()[:6],
        'nav_skills': Skill.objects.values_list('name', flat=True)[:8],
        'faqs': FAQ.objects.all(),
    }

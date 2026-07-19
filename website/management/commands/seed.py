from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from website.models import (
    Profile, SocialLink, Skill, Service, Category, Project, Experience,
    Education, Certification, Testimonial, BlogCategory, Tag, Post, FAQ,
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with demo content.'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username='admin', defaults={'email': 'tegenawfenta604@gmail.com', 'is_staff': True, 'is_superuser': True})
        if not user.check_password('admin12345'):
            user.set_password('admin12345')
            user.save()
        if user.email != 'tegenawfenta604@gmail.com':
            user.email = 'tegenawfenta604@gmail.com'
            user.save()
        if user.first_name != 'Tegenaw' or user.last_name != 'Fenta':
            user.first_name = 'Tegenaw'
            user.last_name = 'Fenta'
            user.save()
        self.stdout.write(self.style.SUCCESS('Superuser ready (admin / admin12345)'))

        profile_bio = (
            'I am a passionate Full Stack and Mobile App Developer from Ethiopia. I build scalable '
            'web applications using Python, Django, JavaScript, Bootstrap, and REST APIs. I also '
            'develop cross-platform mobile applications with Flutter and native Android applications '
            'using Java. I enjoy solving real-world problems through clean, modern, and '
            'user-friendly software solutions.'
        )
        profile, _ = Profile.objects.get_or_create(user=user, defaults={
            'title': 'Full Stack & Mobile App Developer',
            'bio': profile_bio,
            'location': 'Gondar, Ethiopia',
            'phone': '0915292743',
            'available_for_work': True,
        })
        profile.title = 'Full Stack & Mobile App Developer'
        profile.bio = profile_bio
        profile.location = 'Gondar, Ethiopia'
        profile.phone = '0915292743'
        profile.save()

        # Remove platforms explicitly not used on the site (Facebook, Instagram)
        SocialLink.objects.filter(platform__in=['facebook', 'instagram']).delete()

        social_links = [
            ('github', 'GitHub', 'https://github.com/tegenawfenta604-debug', 'bi-github'),
            ('upwork', 'Upwork', 'https://www.upwork.com/freelancers/~01f261d91510fe1105?mp_source=share', 'bi-briefcase'),
            ('linkedin', 'LinkedIn', 'https://linkedin.com/', 'bi-linkedin'),
            ('twitter', 'X', 'https://twitter.com/', 'bi-twitter-x'),
            ('telegram', 'Telegram', 'https://t.me/MAM7735', 'bi-telegram'),
            ('email', 'Email', 'mailto:tegenawfenta604@gmail.com', 'bi-envelope'),
            ('phone', 'Phone', 'tel:0915292743', 'bi-telephone'),
        ]
        for platform, label, url, icon in social_links:
            link, _ = SocialLink.objects.get_or_create(platform=platform, defaults={'label': label, 'url': url, 'icon': icon})
            link.label = label
            link.url = url
            link.icon = icon
            link.save()

        skills = [
            ('HTML5', 'frontend', 95), ('CSS3', 'frontend', 90), ('JavaScript', 'frontend', 88),
            ('Bootstrap', 'frontend', 90), ('Python', 'backend', 92), ('Django', 'backend', 93),
            ('REST API', 'backend', 85), ('PostgreSQL', 'database', 82), ('Git', 'devops', 88),
            ('Docker', 'devops', 75), ('Flutter', 'frontend', 88), ('Android Studio', 'other', 86),
            ('Java', 'backend', 84), ('Kotlin', 'backend', 83),
        ]
        for name, cat, lvl in skills:
            Skill.objects.get_or_create(name=name, defaults={'category': cat, 'level': lvl})

        services = [
            ('Web Development', 'Building responsive, fast, and secure web applications tailored to your needs.', 'bi-code-slash'),
            ('Mobile App Development', 'Cross-platform Flutter apps and native Android apps with Java and Kotlin in Android Studio.', 'bi-phone'),
            ('API Development', 'Designing robust REST APIs with Django REST Framework.', 'bi-server'),
            ('UI/UX Implementation', 'Translating designs into pixel-perfect, accessible interfaces.', 'bi-palette'),
            ('Consulting', 'Code reviews, architecture guidance, and best practices.', 'bi-lightbulb'),
        ]
        for title, desc, icon in services:
            Service.objects.get_or_create(title=title, defaults={'description': desc, 'icon': icon})

        web = Category.objects.get_or_create(name='Web')[0]
        mobile = Category.objects.get_or_create(name='Mobile')[0]
        ml = Category.objects.get_or_create(name='Data')[0]

        projects = [
            ('E-Commerce Platform', web, 'A full-featured online store with cart, payments, and admin dashboard.', True,
             'Django, PostgreSQL, Stripe', 'https://example.com', 'https://github.com/'),
            ('Task Management App', web, 'A collaborative task board with real-time updates.', False,
             'Django, Channels, Redis', 'https://example.com', 'https://github.com/'),
            ('Portfolio Generator', web, 'A SaaS tool that generates personal portfolio sites.', True,
             'Django, Celery, Tailwind', 'https://example.com', 'https://github.com/'),
        ]
        for title, cat, desc, feat, tech, live, gh in projects:
            Project.objects.get_or_create(title=title, defaults={
                'category': cat, 'short_description': desc, 'description': desc,
                'featured': feat, 'technologies': tech, 'live_url': live, 'github_url': gh})

        Experience.objects.get_or_create(role='Senior Django Developer', company='Tech Corp',
            defaults={'start_date': '2022-01-01', 'current': True, 'location': 'Remote',
                      'description': 'Lead backend development of customer-facing products.'})
        Experience.objects.get_or_create(role='Python Developer', company='StartupX',
            defaults={'start_date': '2020-01-01', 'end_date': '2021-12-31',
                      'description': 'Built APIs and data pipelines.'})

        Education.objects.get_or_create(degree='B.Sc. Computer Science', school='State University',
            defaults={'start_date': '2016-09-01', 'end_date': '2020-06-30', 'field': 'Computer Science',
                      'description': 'Graduated with honors.'})

        Certification.objects.get_or_create(name='Django for Everybody', issuer='Coursera',
            defaults={'date': '2023-05-01', 'url': 'https://example.com'})
        Certification.objects.get_or_create(name='AWS Certified Developer', issuer='Amazon',
            defaults={'date': '2024-02-01', 'url': 'https://example.com'})

        Testimonial.objects.get_or_create(name='John Doe', defaults={
            'role': 'CTO', 'company': 'Acme', 'quote': 'Delivered an outstanding product ahead of schedule. Highly recommended!', 'rating': 5})

        blog_cat = BlogCategory.objects.get_or_create(name='Tutorials')[0]
        Tag.objects.get_or_create(name='Django')
        Tag.objects.get_or_create(name='Python')
        Tag.objects.get_or_create(name='Web')

        post, _ = Post.objects.get_or_create(title='Getting Started with Django', defaults={
            'author': user, 'category': blog_cat, 'excerpt': 'A beginner-friendly introduction to Django.',
            'content': 'Django is a high-level Python web framework that encourages rapid development.\n\n'
                       'In this post we cover models, views, and templates to get you building fast.'})
        post.tags.add(*Tag.objects.all())

        FAQ.objects.get_or_create(question='What services do you offer?',
            defaults={'answer': 'I offer web development, API development, and consulting services.'})
        FAQ.objects.get_or_create(question='How can I contact you?',
            defaults={'answer': 'Use the contact form on the Contact page and I will reply within 48 hours.'})

        self.stdout.write(self.style.SUCCESS('Demo content seeded successfully.'))

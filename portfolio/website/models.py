from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Client'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


def unique_slug(sender_instance, slug_source_field, slug_field='slug', max_length=100):
    base = slugify(getattr(sender_instance, slug_source_field))[:max_length]
    slug = base or 'item'
    Model = sender_instance.__class__
    i = 1
    qs = Model.objects.filter(**{slug_field: slug})
    if sender_instance.pk:
        qs = qs.exclude(pk=sender_instance.pk)
    while qs.exists():
        slug = f"{base}-{i}"
        qs = Model.objects.filter(**{slug_field: slug})
        if sender_instance.pk:
            qs = qs.exclude(pk=sender_instance.pk)
        i += 1
    return slug


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=120, help_text="e.g. Full Stack Developer")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    birthday = models.DateField(blank=True, null=True)
    available_for_work = models.BooleanField(default=True)
    resume_summary = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('upwork', 'Upwork'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter / X'),
        ('telegram', 'Telegram'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('website', 'Website'),
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='github')
    label = models.CharField(max_length=60, blank=True)
    url = models.URLField(max_length=300)
    icon = models.CharField(max_length=60, blank=True, help_text="Bootstrap icon class, e.g. bi-github")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label or self.platform


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='frontend')
    level = models.PositiveIntegerField(default=80, help_text="Proficiency 0-100")
    icon = models.CharField(max_length=60, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=60, blank=True, help_text="Bootstrap icon class")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, 'name', max_length=100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('projects')}?category={self.slug}"


class Project(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    github_url = models.URLField(max_length=300, blank=True)
    live_url = models.URLField(max_length=300, blank=True)
    client = models.CharField(max_length=120, blank=True)
    date = models.DateField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, 'title', max_length=180)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Experience(models.Model):
    role = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty if current")
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Education(models.Model):
    school = models.CharField(max_length=160)
    degree = models.CharField(max_length=160)
    field = models.CharField(max_length=160, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'

    def __str__(self):
        return f"{self.degree} - {self.school}"


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=160)
    date = models.DateField()
    credential_id = models.CharField(max_length=160, blank=True)
    url = models.URLField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return f"{self.name} - {self.issuer}"


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, 'name', max_length=100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('blog')}?category={self.slug}"


class Tag(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, 'name', max_length=80)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('blog')}?tag={self.slug}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField(help_text="Supports plain text; line breaks are preserved")
    published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, 'title', max_length=220)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=120)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.name}"


class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} <{self.email}>"


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question

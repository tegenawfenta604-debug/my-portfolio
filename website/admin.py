from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from website.models import (
    User, Profile, SocialLink, Skill, Service, Category, Project,
    Experience, Education, Certification, Testimonial, BlogCategory,
    Tag, Post, Comment, Contact, FAQ,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (('Role', {'fields': ('role',)}),)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'location', 'available_for_work')
    readonly_fields = ('preview_photo',)

    def preview_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:200px;max-width:200px;border-radius:12px;" />',
                obj.photo.url,
            )
        return '(no photo uploaded)'

    preview_photo.short_description = 'Photo Preview'

    fieldsets = (
        (None, {'fields': ('user', 'title', 'bio', 'preview_photo', 'photo', 'cv',
                           'location', 'phone', 'birthday', 'available_for_work',
                           'resume_summary')}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'label', 'url', 'order')
    list_editable = ('order',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'order')
    list_filter = ('category',)
    list_editable = ('order',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'order', 'created_at')
    list_filter = ('category', 'featured')
    list_editable = ('order', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_date', 'current')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'start_date', 'current')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'date')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'order')
    list_editable = ('order',)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published', 'views', 'created_at')
    list_filter = ('published', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'approved', 'created_at')
    list_filter = ('approved',)
    list_editable = ('approved',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'read', 'created_at')
    list_filter = ('read',)
    list_editable = ('read',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

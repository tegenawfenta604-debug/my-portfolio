from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from website.models import Project, Post


class PortfolioSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Project.objects.all()

    def location(self, item):
        return reverse('project_detail', args=[item.slug])


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, item):
        return item.updated_at

    def location(self, item):
        return reverse('blog_detail', args=[item.slug])

import os
import platform

from django import forms
from django.contrib import admin
from django.forms import TextInput, Textarea

from blog.models import Blog, Image, Category, Project


class ImageInline(admin.TabularInline):
    model = Image
    extra = 3


class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('html_content', 'brief_content')


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    inlines = [ImageInline, ]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Project, admin.ModelAdmin)

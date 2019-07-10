#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = 'liao gao xiang'

from django.contrib import admin
from .models import Project, Job, JobParameter, Build, BuildParameter


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "fullDisplayName", "description", "url", "config_xml", "updated_at"]
    search_fields = ["name", "fullDisplayName", "description", "url", "config_xml", "updated_at"]
    list_filter = ["name", "fullDisplayName", "description", "url", "config_xml", "updated_at"]


class JobAdmin(admin.ModelAdmin):
    list_display = ["project", "name", "fullDisplayName", "description", "url", "config_xml", "env",
                    "nextBuildNumber", "updated_at"]
    search_fields = ["project", "name", "fullDisplayName", "description", "url", "config_xml", "env",
                     "nextBuildNumber", "updated_at"]
    list_filter = ["project", "name", "fullDisplayName", "description", "url", "config_xml", "env",
                   "nextBuildNumber", "updated_at"]


class JobParameterAdmin(admin.ModelAdmin):
    list_display = ["job", "name", "type", "value", "description", "updated_at"]
    search_fields = ["job", "name", "type", "value", "description", "updated_at"]
    list_filter = ["job", "name", "type", "value", "description", "updated_at"]


class BuildAdmin(admin.ModelAdmin):
    list_display = ["job", "build_id", "url", "result", "fullDisplayName", "description", "start_time", "duration",
                    "consoleText", "updated_at"]
    search_fields = ["job", "build_id", "url", "result", "fullDisplayName", "description", "start_time", "duration",
                     "consoleText", "updated_at"]
    list_filter = ["job", "build_id", "url", "result", "fullDisplayName", "description", "start_time", "duration",
                   "consoleText", "updated_at"]


class BuildParameterAdmin(admin.ModelAdmin):
    list_display = ["build", "name", "value", "updated_at"]
    search_fields = ["build", "name", "value", "updated_at"]
    list_filter = ["build", "name", "value", "updated_at"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobParameter, JobParameterAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(BuildParameter, BuildParameterAdmin)

admin.site.site_header = 'Jenkins调度平台'
admin.site.site_title = 'Jenkins调度平台'

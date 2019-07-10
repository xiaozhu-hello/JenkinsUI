#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = 'liao gao xiang'

from django.db import models
from django.utils.translation import ugettext_lazy as _


def project_filepath(instance, filename):
    """file will be upload to MEDIA_ROOT/projects/fullName/<filename>"""
    return f"projects/{instance.fullName}/{filename}"


def job_filepath(instance, filename):
    """file will be upload to MEDIA_ROOT/jobs/name/<filename>"""
    return f"jobs/{instance.name}/{filename}"


class Project(models.Model):
    """All projects on Jenkins"""
    name = models.CharField(max_length=255, unique=True, verbose_name=_("英文简称"))  # unique
    fullDisplayName = models.CharField(max_length=255, db_index=True, verbose_name=_("中文全称"))
    description = models.TextField(null=True, blank=True, verbose_name=_("描述"))
    url = models.URLField(max_length=255, unique=True, verbose_name=_("URL地址"))
    config_xml = models.FileField(upload_to=project_filepath, verbose_name=_("config.xml"))
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name
        ordering = ("name", "created_at")

    def __str__(self):
        return self.fullDisplayName


class Job(models.Model):
    """All jobs for each project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="job_project", verbose_name=_("所属项目"))
    name = models.CharField(max_length=255, db_index=True, verbose_name=_("Job名"))  # 不同项目可能同一个Job名
    fullDisplayName = models.CharField(max_length=255, db_index=True, verbose_name=_("中文全称"))
    description = models.TextField(null=True, blank=True, verbose_name=_("描述"))
    url = models.URLField(max_length=255, unique=True, verbose_name=_("URL地址"))
    config_xml = models.FileField(upload_to=job_filepath, verbose_name=_("config.xml"))
    env = models.CharField(max_length=255, default="all", verbose_name=_("环境(组)"))
    nextBuildNumber = models.PositiveIntegerField(verbose_name=_("下次构建ID"))
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = verbose_name
        unique_together = ("project", "name")  # 项目与job名构成联合唯一键
        ordering = ("name", "created_at")

    def __str__(self):
        return f"{self.project.name}_{self.fullDisplayName}"


class JobParameter(models.Model):
    """parameters for jenkins job"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="parameter_job", verbose_name=_("所属Job"))
    name = models.CharField(max_length=255, verbose_name=_("参数名"))
    type = models.CharField(max_length=255, verbose_name=_("参数类型"))
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("参数值"))
    description = models.TextField(null=True, blank=True, verbose_name=_("描述"))
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = "Job参数"
        verbose_name_plural = verbose_name
        unique_together = ("job", "name")  # job名与参数名构成联合唯一键
        ordering = ("name", "created_at")

    def __str__(self):
        return f"{self.job.name}_{self.name}"


class Build(models.Model):
    """build history for jenkins job"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="build_job", verbose_name=_("所属Job"))
    build_id = models.PositiveIntegerField(verbose_name=_("构建ID"))
    url = models.URLField(max_length=255, unique=True, verbose_name=_("URL地址"))
    result = models.CharField(choices=((0, "SUCCESS"), (1, "FAILED")), max_length=1, verbose_name=_("执行结果"))
    fullDisplayName = models.CharField(max_length=255, db_index=True, verbose_name=_("中文全称"))
    description = models.TextField(null=True, blank=True, verbose_name=_("描述"))
    start_time = models.DateTimeField(verbose_name=_("开始时间"))
    duration = models.PositiveSmallIntegerField(verbose_name=_("构建时长"))
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = "构建"
        verbose_name_plural = verbose_name
        unique_together = ("job", "build_id")  # job名与构建ID构成联合唯一键
        ordering = ("name", "created_at")

    def __str__(self):
        return f"{self.job.name}_{self.fullDisplayName}"


class BuildParameter(models.Model):
    """parameters for jenkins job build history"""
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name="parameter_build", verbose_name=_("所属构建"))
    name = models.CharField(max_length=255, verbose_name=_("参数名"))
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("参数值"))
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = "构建参数"
        verbose_name_plural = verbose_name
        unique_together = ("build", "name")  # 构建ID与参数名构成联合唯一键
        ordering = ("name", "created_at")

    def __str__(self):
        return f"{self.build.fullDisplayName}_{self.name}"

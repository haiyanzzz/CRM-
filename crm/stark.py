#!usr/bin/env python
# -*- coding:utf-8 -*-
from crm import models
from crm.config.classlist import ClassListConfig
from crm.config.consultrecord import ConsultRecordConfig
from crm.config.course import CourseConfig
from crm.config.courserrecord import CourseRecordConfig
from crm.config.customer import CustomerConfig
from crm.config.department import DepartmentConfig
from crm.config.school import SchoolConfig
from crm.config.student import StudentConfig
from crm.config.studyrecord import StudyRecordConfig
from crm.config.userinfo import UserInfoConfig
from stark.service import v1

v1.site.register(models.Department,DepartmentConfig)
v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Course,CourseConfig)
v1.site.register(models.School,SchoolConfig)
v1.site.register(models.ClassList,ClassListConfig)
v1.site.register(models.Customer, CustomerConfig)
v1.site.register(models.ConsultRecord,ConsultRecordConfig)
v1.site.register(models.CourseRecord,CourseRecordConfig)
v1.site.register(models.StudyRecord,StudyRecordConfig)
v1.site.register(models.Student,StudentConfig)


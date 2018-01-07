from stark.service import v1
from crm.permissions.school import SchoolPermission
class SchoolConfig(SchoolPermission,v1.StarkConfig):
    list_display = ["title"]
    edit_link = ["title"]
from django.contrib import admin
from .models import Question, Choice, LeaveRequest, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],'classes':
                              ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('leave_requester', 'leave_start_date', 'leave_end_date', 'leave_days', 'leave_request_status', 'leave_approver')
    
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Leave Quota Information'
    fk_name = 'user'

class CustomizedUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomizedUserAdmin, self).get_inline_instances(request, obj)
    

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)


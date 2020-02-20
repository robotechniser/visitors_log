from django.contrib import admin

from .models import Member, MemberLoginInstance

class MemberLoginInstanceInline(admin.TabularInline):
    model = MemberLoginInstance
    extra = 0
    fields = ['id', 'login_timestamp', 'logout_timestamp', 'logged_out']
    # readonly_fields = ('id',) # Breaks editing Members

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'hashed_secret_key', 'login_count', 'is_active')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'hashed_secret_key', 'login_count', 'is_active')
        }),
    )
    inlines = [MemberLoginInstanceInline]
    readonly_fields = ('hashed_secret_key',)
    list_per_page = 20

@admin.register(MemberLoginInstance)
class MemberLoginInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'login_timestamp', 'logout_timestamp', 'logged_out')
    fields = ['id', 'member', ('login_timestamp', 'logout_timestamp'), 'logged_out']
    list_filter = ('member', 'login_timestamp', 'logout_timestamp', 'logged_out')
    readonly_fields = ('id',)
    list_per_page = 20
from django.contrib import admin
from agora.models import Decision, Vote

class DecisionAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_at', 'modified_at', 'closed_at')

admin.site.register(Decision, DecisionAdmin)

class VoteAdmin(admin.ModelAdmin):
	pass

admin.site.register(Vote, VoteAdmin)

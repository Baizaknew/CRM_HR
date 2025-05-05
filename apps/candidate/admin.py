from django.contrib import admin

from apps.candidate.models import Candidate, CandidateApplication, CandidateApplicationStatus, CandidateTags

admin.site.register(Candidate)
admin.site.register(CandidateApplication)
admin.site.register(CandidateApplicationStatus)
admin.site.register(CandidateTags)

from django.contrib import admin

from apps.candidate.models import Candidate, CandidateApplication, CandidateApplicationStatus, CandidateTag, CandidateSource

admin.site.register(Candidate)
admin.site.register(CandidateApplication)
admin.site.register(CandidateApplicationStatus)
admin.site.register(CandidateTag)
admin.site.register(CandidateSource)


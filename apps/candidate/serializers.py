from rest_framework import serializers

from apps.candidate.models import Candidate, CandidateTag, CandidateSource, CandidateApplication, CandidateNote, \
    CandidateReference
from apps.vacancy.serializers import SimpleVacancySerializer
from apps.vacancy_request.serializers import UserSimpleSerializer


class CandidateUpdateCreateDetailSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=CandidateTag.objects.all(),
        many=True,
        required=False,
    )
    sources = serializers.PrimaryKeyRelatedField(
        queryset=CandidateSource.objects.all(),
        required=False,
        allow_null=True,
    )
    added_by = serializers.PrimaryKeyRelatedField(read_only=True,)

    class Meta:
        model = Candidate
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'city', 'experience', 'sources',
                  'source_type', 'salary_expectation', 'tags', 'cover_letter', 'resume', 'added_by')


class SimpleApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateApplication
        fields = ('id', 'status',)


class CandidateApplicationListSerializerForCandidateListSerializer(serializers.ModelSerializer):
    vacancy = SimpleVacancySerializer(read_only=True)
    application = SimpleApplicationStatusSerializer(read_only=True)

    class Meta:
        model = CandidateApplication
        fields = ('id', 'vacancy', 'application',)


class CandidateListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    applications = CandidateApplicationListSerializerForCandidateListSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = ('id', 'full_name', 'applications', 'created_at', 'source_type')

    def get_full_name(self, obj):
        parts = [obj.last_name, obj.first_name, obj.patronymic]
        return " ".join(filter(None, parts))


class CandidateNoteListSerializer(serializers.ModelSerializer):
    added_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = CandidateNote
        fields = ('id', 'text', 'added_by', 'created_at')


class CandidateNoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateNote
        fields = ('text',)


class CandidateReferencesListSerializer(serializers.ModelSerializer):
    added_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = CandidateNote
        fields = ('id', 'text', 'added_by', 'created_at')


class CandidateReferenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateNote
        fields = ('text',)

from rest_framework import serializers

from apps.candidate.models import Candidate, CandidateTag, CandidateSource, CandidateApplication, CandidateNote, \
    CandidateReference, CandidateApplicationStatus
from apps.vacancy.serializers import SimpleVacancySerializer
from apps.vacancy_request.serializers import UserSimpleSerializer


class CandidateUpdateCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=CandidateTag.objects.all(),
        many=True,
        required=False,
    )
    source = serializers.PrimaryKeyRelatedField(
        queryset=CandidateSource.objects.all(),
        required=False,
        allow_null=True,
    )
    added_by = serializers.PrimaryKeyRelatedField(read_only=True,)

    class Meta:
        model = Candidate
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'city', 'experience', 'source',
                  'source_type', 'salary_expectation', 'tags', 'cover_letter', 'resume', 'added_by')


class SimpleApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateApplicationStatus
        fields = ('id', 'name',)


class CandidateForApplicationCardSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Candidate
        fields = ('id', 'full_name', 'salary_expectation', 'resume')

    def get_full_name(self, obj) -> str:
        parts = [obj.last_name, obj.first_name, obj.patronymic]
        return " ".join(filter(None, parts))


class BriefCandidateApplicationSerializer(serializers.ModelSerializer):
    vacancy = SimpleVacancySerializer(read_only=True)
    status = SimpleApplicationStatusSerializer(read_only=True)

    class Meta:
        model = CandidateApplication
        fields = ('id', 'vacancy', 'status',)


class CandidateListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    applications = BriefCandidateApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = ('id', 'full_name', 'applications', 'created_at', 'source_type')

    def get_full_name(self, obj) -> str:
        parts = [obj.last_name, obj.first_name, obj.patronymic]
        return " ".join(filter(None, parts))


class CandidateNoteListDetailSerializer(serializers.ModelSerializer):
    added_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = CandidateNote
        fields = ('id', 'text', 'added_by', 'created_at')


class CandidateNoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateNote
        fields = ('id', 'candidate', 'text', 'created_at')


class CandidateNoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateNote
        fields = ('id', 'text')


class CandidateReferencesListDetailSerializer(serializers.ModelSerializer):
    added_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = CandidateReference
        fields = ('id', 'text', 'added_by', 'created_at')


class CandidateReferenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateReference
        fields = ('id', 'candidate', 'text', 'created_at')


class CandidateReferenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateReference
        fields = ('id', 'text', 'created_at')


class CandidateApplicationSerializer(serializers.ModelSerializer):
    recruiter = UserSimpleSerializer(read_only=True)

    class Meta:
        model = CandidateApplication
        fields = ('id', 'vacancy', 'candidate', 'recruiter', 'status', 'created_at')


class CandidateApplicationUpdateSerializer(serializers.ModelSerializer):
    recruiter = UserSimpleSerializer(read_only=True)

    class Meta:
        model = CandidateApplication
        fields = ('id', 'status', 'rejected_reason', 'created_at', 'recruiter')

    def validate(self, attrs):
        new_status = attrs.get('status')
        rejected_reason = attrs.get('rejected_reason')

        if new_status and new_status.is_rejected and not rejected_reason:
            raise serializers.ValidationError({'rejected_reason': 'Необходимо указать причину'})

        if new_status and not new_status.is_rejected and rejected_reason:
            raise serializers.ValidationError({'rejected_reason': 'Причина отказа указывается только для статутов отказа'})
        print('>>>>>>>>>>>>>>>>>>>>.', attrs)
        return attrs


class CandidateApplicationForVacancySerializer(serializers.ModelSerializer):
    candidate = CandidateForApplicationCardSerializer(read_only=True)

    class Meta:
        model = CandidateApplication
        fields = ('id', 'candidate', 'status', 'created_at', 'rejected_reason')


class CandidateApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateApplicationStatus
        fields = ('id', 'order', 'name', 'is_default', 'is_rejected', 'is_success')


class CandidateSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSource
        fields = ('id', 'name', 'created_at', 'updated_at')


class CandidateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateTag
        fields = ('id', 'title', 'created_at', 'updated_at')


class CandidateDetailSerializer(serializers.ModelSerializer):
    tags = CandidateTagSerializer(many=True, read_only=True)
    source = CandidateSourceSerializer(read_only=True)
    added_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'city', 'experience', 'source',
        'source_type', 'salary_expectation', 'tags', 'cover_letter', 'resume', 'added_by')

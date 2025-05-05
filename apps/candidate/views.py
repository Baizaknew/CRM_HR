from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.candidate.models import Candidate, CandidateApplication, CandidateNote, CandidateReference
from apps.candidate.permissions import IsHrLeadOrRecruiter
from apps.candidate.serializers import CandidateListSerializer, CandidateUpdateCreateDetailSerializer, \
    CandidateNoteListSerializer, CandidateReferencesListSerializer, CandidateNoteCreateSerializer, \
    CandidateReferenceCreateSerializer


@extend_schema(tags=['candidate'])
class CandidateModelViewSet(ModelViewSet):

    queryset = Candidate.objects.select_related('source', 'added_by').prefetch_related(
        'tags',
        Prefetch(
            'applications',
            queryset=CandidateApplication.objects.select_related('vacancy','status',).order_by('-created_at'),
        )
    )
    permission_classes = (IsAuthenticated, IsHrLeadOrRecruiter,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CandidateListSerializer
        return CandidateUpdateCreateDetailSerializer

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    @extend_schema(responses=CandidateNoteListSerializer(many=True))
    @action(detail=True, methods=['get'], url_path='notes')
    def notes(self, request, pk=None):
        instance = self.get_object()
        notes_qs = CandidateNote.objects.filter(candidate=instance).select_related('added_by').order_by('-created_at')
        serializer = CandidateNoteListSerializer(notes_qs, many=True)
        return Response(serializer.data)

    @extend_schema(responses=CandidateReferencesListSerializer(many=True))
    @action(detail=True, methods=['get'], url_path='references')
    def references(self, request, pk=None):
        instance = self.get_object()
        references_qs = CandidateReference.objects.filter(candidate=instance).select_related('added_by').order_by(
            '-created_at')
        serializer = CandidateReferencesListSerializer(references_qs, many=True)
        return Response(serializer.data)

    @extend_schema(request=CandidateNoteCreateSerializer, responses={201: CandidateNoteListSerializer})
    @action(detail=True, methods=['post'], url_path='notes/create')
    def create_note(self, request, pk=None):
        candidate_instance = self.get_object()
        serializer = CandidateNoteCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            note = serializer.save(candidate=candidate_instance, added_by=request.user)
            response_serializer = CandidateNoteListSerializer(note)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Ошибка создания заметки: {e}"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=CandidateReferenceCreateSerializer, responses={201: CandidateReferencesListSerializer})
    @action(detail=True, methods=['post'], url_path='references/create')
    def create_reference(self, request, pk=None):
        candidate_instance = self.get_object()
        serializer = CandidateReferenceCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            reference = serializer.save(candidate=candidate_instance, added_by=request.user)
            response_serializer = CandidateReferencesListSerializer(reference)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"Ошибка создания обратной связи: {e}"}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from app.models import Evidence, Version
from app.permissions import IsFactory
from app.services.audit import write_audit


class EvidenceCreateView(APIView):
    permission_classes = [IsAuthenticated, IsFactory]

    def post(self, request):
        e = Evidence.objects.create(
            name=request.data['name'],
            doc_type=request.data['docType'],
            expiry=request.data['expiry'],
            notes=request.data.get('notes', ''),
            factory_id=request.user.factory_id,
            created_by=request.user
        )

        v = Version.objects.create(
            evidence=e,
            version_id="v1",
            notes=e.notes,
            expiry=e.expiry
        )

        write_audit(
            actor=request.user,
            action="CREATE_EVIDENCE",
            obj=e,
            metadata={"factoryId": e.factory_id, "docType": e.doc_type}
        )


        return Response({
            "evidenceId": e.id,
            "versionId": v.id
        }, status=201)



class EvidenceVersionCreateView(APIView):
    permission_classes = [IsAuthenticated, IsFactory]

    def post(self, request, evidence_id):
        e = get_object_or_404(
            Evidence,
            id=evidence_id,
            factory_id=request.user.factory_id
        )

        notes = request.data.get('notes')
        expiry = request.data.get('expiry')

        last_version = e.versions.first()
        new_version_id = (
            int(last_version.version_id.lstrip('v')) + 1
            if last_version else 1
        )
        version_id = f'v{new_version_id}'

        v = Version.objects.create(
            evidence=e,
            version_id=version_id,
            notes=notes,
            expiry=expiry
        )

        write_audit(
            actor=request.user,
            action="ADD_VERSION",
            obj=v,
            metadata={
                "factoryId": e.factory_id,
                "evidenceId": e.id, 
                "versionId": v.version_id
            }
        )


        return Response({
            "versionId": v.id
        }, status=201)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from app.permissions import IsFactory, IsBuyer
from app.models.request import Request, RequestItem
from app.models.evidence import Evidence, Version
from app.services.audit import write_audit


class RequestCreateView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]


    def post(self, request):
        r = Request.objects.create(
            factory_id=request.data['factoryId'],
            title=request.data['title'],
            created_by=request.user
        )

        for item in request.data["items"]:
            RequestItem.objects.create(
                request=r,
                doc_type=item['docType']
            )

        write_audit(
            actor=request.user,
            action="CREATE_REQUEST",
            obj=r,
            metadata={"factoryId": r.factory_id, "buyerId": request.user.user_id}
        )

        return Response({
            "requestId": r.id
        }, status=201)




class FactoryRequestListView(APIView):
    permission_classes = [IsAuthenticated, IsFactory]


    def get(self, request):
        qs = Request.objects.filter(
            factory_id=request.user.factory_id,
        )

        return Response([
            {
                "id": r.id,
                "factoryId": r.factory_id,
                "title": r.title,
                "items": [
                    {
                        "id": item.id,
                        "docType": item.doc_type,
                        "fulfilled": item.fulfilled_evidence is not None,
                        "fulfilledEvidence": item.fulfilled_evidence_id,
                        "fulfilledVersion": item.fulfilled_version_id
                    } for item in r.items.all()
                ]
            } for r in qs
        ])


class BuyerRequestListView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]


    def get(self, request):
        qs = Request.objects.filter(
            created_by=request.user,
        )

        return Response([
            {
                "id": r.id,
                "factoryId": r.factory_id,
                "title": r.title,
                "status": "completed" if all(item.fulfilled_evidence for item in r.items.all()) else "pending",
                "items": [
                    {
                        "id": item.id,
                        "docType": item.doc_type,
                        "fulfilled": item.fulfilled_evidence is not None,
                        "fulfilledEvidence": {
                            "id": item.fulfilled_evidence.id,
                            "name": item.fulfilled_evidence.name,
                            "docType": item.fulfilled_evidence.doc_type,
                            "version": item.fulfilled_version.version_id
                        } if item.fulfilled_evidence else None
                    } for item in r.items.all()
                ]
            } for r in qs
        ])



class FulfillItemView(APIView):
    permission_classes = [IsAuthenticated, IsFactory]


    def post(self, request, request_id, item_id):
        r = get_object_or_404(
            Request, id=request_id, factory_id=request.user.factory_id
        )
        item = get_object_or_404(RequestItem, id=item_id, request=r)

        e = get_object_or_404(
            Evidence,
            id=request.data['evidenceId'],
            factory_id=request.user.factory_id
        )

        v = get_object_or_404(
            Version,
            id=request.data['versionId'],
            evidence=e
        )


        item.fulfilled_evidence = e
        item.fulfilled_version = v
        item.save()


        write_audit(
            actor=request.user,
            action="FULFILL_REQUEST_ITEM",
            obj=item,
            metadata={
                "factoryId": request.user.factory_id,
                "docType": item.doc_type,
                "previousStatus": "Pending",
                "newStatus": "Fulfilled"
            }
        )

        return Response({"status": "Fulfilled"})

from src.telus_bulk.models.tmf_645.check_service_qualification_create import (
    CheckServiceQualificationCreate,
)


class TestCheckServiceQualificationCreate:
    def test_svc_create_default_related_party(self):
        to_create_check_service = CheckServiceQualificationCreate.parse_obj(
            {"description": "hello world", "serviceQualificationItem": []}
        )
        assert len(to_create_check_service.related_party) == 1

    def test_svc_create_NON_default_related_party(self):
        to_create_check_service = CheckServiceQualificationCreate.parse_obj(
            {
                "description": "hello world",
                "serviceQualificationItem": [],
                "relatedParty": [
                    {
                        "id": "x244914",
                        "name": "Alejandro Olmedo",
                        "role": "Requestor",
                        "@type": "RelatedParty",
                        "@referredType": "Organization",
                    }
                ],
            }
        )
        assert len(to_create_check_service.related_party) == 1

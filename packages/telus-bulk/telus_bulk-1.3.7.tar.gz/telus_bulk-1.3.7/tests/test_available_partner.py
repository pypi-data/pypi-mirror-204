from telus_bulk.models.available_partners.partners_enum import (
    available_partners_list,
    PartnersEnum,
)


class TestPartnersList:
    def test_partner_list(self):
        assert len(available_partners_list) > 0

    def test_partner_Bell(self):
        print(PartnersEnum.BELL_PARTNER)
        assert "Bell" in available_partners_list

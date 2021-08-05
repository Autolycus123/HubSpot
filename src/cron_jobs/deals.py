from src.external_apis.hubspot.deals import get_deals
from src.models.deal import Deal
from src.utils.decorators import hubspot_session


@hubspot_session
def get_hubspot_deals():
    return get_deals()


deals = get_hubspot_deals()
for deal in deals:
    print(deal)
    Deal.add_deal(deal)

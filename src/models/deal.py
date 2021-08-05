from extensions import db
from src.adapters.deal import DealAdapter


class Deal(DealAdapter, db.Document):
    dealId = db.IntField(required=True)
    name = db.IntField(required=False)
    stage = db.StringField(required=False)
    close_date = db.DateTimeField(rquired=False)
    amount = db.DecimalField(required=False)
    type = db.StringField(required=False)

    @classmethod
    def get_all(cls):
        return cls.to_json(Deal.objects())

    @classmethod
    def get_by_id(cls, deal_id):
        return cls.to_json(Deal.objects({"dealId": deal_id}))

    @classmethod
    def add_deal(cls, body):
        deal = Deal()
        deal.to_object(body)
        deal.save()
        return cls.to_json(deal)

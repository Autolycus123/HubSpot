class DealAdapter:
    @staticmethod
    def to_json(results):
        return [
            {
                'dealId': result.dealId,
                'name': result.name,
                'stage': result.stage,
                'close_date': result.close_date,
                'amount': result.amount,
                'type': result.type
            } for result in results
        ]

    def to_object(self, body):
        for key, value in body.items():
            if hasattr(self, key):
                setattr(self, key, value)

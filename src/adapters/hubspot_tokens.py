class HubSpotTokensAdapter:

    @staticmethod
    def to_json(results):
        if results is None:
            return []
        if not isinstance(results, list):
            results = [results]
        return [
            {
                'id': result.id,
                'access_token': result.access_token,
                'refresh_token': result.refresh_token
            } for result in results
        ]

    def to_object(self, hubspot_tokens):
        for key, value in hubspot_tokens.items():
            if hasattr(self, key):
                setattr(self, key, value)

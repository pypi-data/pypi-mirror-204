import ml
import os


class ChainsawTemplate:
    def __init__(self, oauth2_id, oauth2_secret, is_repository, is_broker, is_broker_rest, is_logger=True):
        self.json_model = ml.load_config(config_filepath=os.path.join(
                os.path.abspath(os.path.join(os.path.dirname(__file__), "template_json")),
                "chainsaw.json"
            ))
        self.oauth2_id = oauth2_id
        self.oauth2_secret = oauth2_secret
        self.json_model["thingId"] = oauth2_id
        self.json_model["policyId"] = oauth2_id
        self.is_repository = is_repository
        self.is_broker = is_broker
        self.is_broker_rest = is_broker_rest
        if is_logger:
            ml.setup_logger(self.json_model["attributes"].get("name", None))
        self.thing = ml.create_thing(
            model_json=self.json_model,
            oauth2_secret=self.oauth2_secret,
            is_repository=self.is_repository,
            is_broker=self.is_broker
        )





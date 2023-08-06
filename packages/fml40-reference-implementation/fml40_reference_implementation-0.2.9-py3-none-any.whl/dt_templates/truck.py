import ml
import os


class TruckTemplate:
    def __init__(self, oauth2_id, oauth2_secret, is_repository, is_broker, is_broker_rest, is_logger=True):
        forest_machine_features = ml.load_config(config_filepath=os.path.join(
                os.path.abspath(os.path.join(os.path.dirname(__file__), "template_json")),
                "forest_machine.json"
            ))["attributes"]["features"]
        self.json_model = ml.load_config(config_filepath=os.path.join(
                os.path.abspath(os.path.join(os.path.dirname(__file__), "template_json")),
                "truck.json"
            ))
        for item in forest_machine_features:
            if item.get("class") == "ml40::Composite":
                for i in range(len(self.json_model["attributes"]["features"])):
                    if self.json_model["attributes"]["features"][i].get("class") == "ml40::Composite":
                        self.json_model["attributes"]["features"][i]["targets"] += item["targets"]
                forest_machine_features.remove(item)
            if item.get("class") == "ml40::Shared":
                for i in range(len(self.json_model["attributes"]["features"])):
                    if self.json_model["attributes"]["features"][i].get("class") == "ml40::Shared":
                        self.json_model["attributes"]["features"][i]["targets"] += item["targets"]
                forest_machine_features.remvoe(item)

        self.json_model["attributes"]["features"] += forest_machine_features
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





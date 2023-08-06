import uuid
import json
from .api_dto import ApiDto


class TwinRegistration(ApiDto):

    def __init__(self, twin_registration_id=None, twin_id=None, template_id=None, properties=None):
        if twin_registration_id is None:
            self.twin_registration_id = uuid.uuid4()
        else:
            self.twin_registration_id = twin_registration_id
        self.twin_id = twin_id
        self.template_id = template_id
        self.properties = properties

    def api_id(self) -> str:
        """
        Id of the TwinRegistrations (twin_registration_id)

        :return: string formatted UUID of the template.
        """
        return str(self.twin_registration_id).upper()

    def endpoint(self) -> str:
        """
        Name of the endpoints used to manipulate templates.
        :return: Endpoint name.
        """
        return "TwinRegistration"

    def from_json(self, obj):
        """
        Load the Registration entity from a dictionary.

        :param obj: Dict version of the Registration.
        """
        if "id" in obj.keys():
            self.twin_registration_id = uuid.UUID(obj["id"])
        if "twinId" in obj.keys() and obj["twinId"] is not None:
            self.twin_id = obj["twinId"]
        if "templateId" in obj.keys() and obj["templateId"] is not None:
            self.template_id = obj["templateId"]
        if "properties" in obj.keys() and obj["properties"] is not None:
            if isinstance(obj["properties"], str):
                self.properties = json.loads(obj["properties"])
            else:
                self.properties = obj["properties"]

    def to_json(self):
        """
        Convert the registration to a dictionary compatible to JSON format.

        :return: dictionary representation of the Registration object.
        """
        obj = {
            "id": str(self.twin_registration_id)
        }
        if self.twin_id is not None:
            obj["twinId"] = str(self.twin_id)
        if self.template_id is not None:
            obj["templateId"] = str(self.template_id)
        if self.properties is not None:
            obj["properties"] = json.dumps(self.properties)
        return obj


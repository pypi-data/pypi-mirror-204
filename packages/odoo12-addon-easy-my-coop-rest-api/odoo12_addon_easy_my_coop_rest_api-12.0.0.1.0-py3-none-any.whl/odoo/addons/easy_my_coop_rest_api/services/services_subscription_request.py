
import json
from . import schemas
from werkzeug.exceptions import BadRequest, NotFound
from odoo.http import Response
from odoo.tools.translate import _
from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError
from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.base_rest_base_structure.models.api_services_utils import(
    APIServicesUtils
)


class SubscriptionRequestService(Component):
    _inherit = "base.rest.private_abstract_service"
    _name = "subscription.request.service"
    _usage = "subscription-request"
    _description = """
        Subscription request Services
    """

    def create(self, **params):
        create_dict = self._prepare_create(params)
        sr = self.env['subscription.request'].create(create_dict)
        return Response(
            json.dumps({
                'message': _("Creation ok"),
                'id': sr.id
            }),
            status=200,
            content_type="application/json"
        )

    def _prepare_create(self, params):
        utils = APIServicesUtils.get_instance()
        attributes = self._get_attributes_list()
        sr_create_values = utils.generate_create_dictionary(params, attributes)
        address = params["address"]
        country = self._get_country(address["country"])
        sr_create_values_address = {
            "address": address["street"],
            "zip_code": address["zip_code"],
            "city": address["city"],
            "country_id": country.id
        }
        return {**sr_create_values, **sr_create_values_address}

    def _validator_create(self):
        return schemas.S_SUBSCRIPTION_REQUEST_CREATE_FIELDS

    def _get_attributes_list(self):
        return [
            "firstname",
            "lastname",
            "email",
            "phone",
            "lang",
            "iban",
            "ordered_parts",
            "share_product_id",
            "vat",
            "is_company",
        ]

    def _get_country(self, code):
        country = self.env["res.country"].search([("code", "=", code)])
        if country:
            return country
        else:
            raise wrapJsonException(BadRequest(
                _("No country for isocode %s") % code))

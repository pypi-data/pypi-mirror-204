# -*- coding: utf-8 -*-
import json
from odoo import api, fields, models
from odoo.tools.translate import _


class CrmSaleOrderLine(models.Model):
    _name = "crm.sale.order.line"

    crm_lead_id = fields.Many2one('crm.lead', string=_("Related lead"))
    product_id = fields.Many2one('product.product', string=_("Product"))
    quantity = fields.Float(string="quantity")
    attach_to_existing_contract = fields.Boolean(
        string=_("Attach to existing contract"))
    # TODO: define dynamic domain based on crm_lead_id.partner_id
    contract_id = fields.Many2one(
        'contract.contract',
        string=_("Related contract")
    )
    contract_date_start_type = fields.Selection([
        (
            'validation_date',
            _("Validation date")
        ),
        (
            'validation_next_month',
            _("First day on next month from validation")
        )],
        string=_("Contract start date"),
        required=True,
        default="validation_date"
    )
    partner_id = fields.Many2one(
        'res.partner',
        compute="_get_partner_id",
        store=False
    )

    @api.depends('crm_lead_id')
    def _get_partner_id(self):
        self.ensure_one()
        if self.crm_lead_id:
            self.partner_id = self.crm_lead_id.id

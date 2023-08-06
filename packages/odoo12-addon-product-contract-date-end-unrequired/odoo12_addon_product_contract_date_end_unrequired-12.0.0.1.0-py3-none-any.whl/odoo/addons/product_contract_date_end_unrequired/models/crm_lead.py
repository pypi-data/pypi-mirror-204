from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo import exceptions


class CrmLead(models.Model):
    _inherit = "crm.lead"

    crm_order_line_ids = fields.One2many(
        "crm.sale.order.line",
        string=_("Order lines"),
        inverse_name="crm_lead_id"
    )
    has_order_lines = fields.Boolean(
        string=_("Has order lines"), compute="_get_has_order_lines", store=False)

    # TODO: create a method to pupulate related_partner from lead
    # If no partner found we might need to create one.
    @api.depends("crm_order_line_ids")
    def _get_has_order_lines(self):
        if self.crm_order_line_ids:
            self.has_order_lines = True
        else:
            self.has_order_lines = False

    def create_quotation_from_order_line_action(self):
        self._validate_create_quotation_from_order_line()
        view_id = self._create_quotation_from_order_line()
        return view_id

    def _validate_create_quotation_from_order_line(self):
        if not self.partner_id:
            raise exceptions.ValidationError(
                _("Client must be defined")
            )
        if self.crm_order_line_ids:
            for order_line in self.crm_order_line_ids:
                if order_line.attach_to_existing_contract:
                    if (
                        self.partner_id.sale_contract_count == 0 or
                        self.partner_id.sale_contract_count > 1
                    ):
                        raise exceptions.ValidationError(
                            _("Trying to attach line to contract but none \
                            or multiple contracts defined for partner.\
                            Please select manually.")
                        )
                    if not order_line.product_id.is_contract:
                        raise exceptions.ValidationError(
                            _("Contract option selected \
                            but product is not a contract")
                        )
        else:
            raise exceptions.ValidationError(
                _("Can't create quotation without order lines selected")
            )

    def _create_quotation_from_order_line(self):
        # TODO: Must validate partner_id exists.
        # Without partner_id cannot create sale.order
        # TODO: Define start date at the begining of month option
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id
        })
        if self.crm_order_line_ids:
            for order_line in self.crm_order_line_ids:
                creation_data = {
                    'product_id': order_line.product_id.id,
                    'product_uom_qty': order_line.quantity,
                    'order_id': sale_order.id
                }
                # contract data
                if order_line.product_id.is_contract:
                    # define date_start
                    now = datetime.now()
                    if (
                        order_line.contract_date_start_type ==
                        'validation_date'
                    ):
                        creation_data['date_start'] = str(now)
                    if (
                        order_line.contract_date_start_type ==
                        'validation_next_month'
                    ):
                        creation_data['date_start'] = str(
                            (
                                now.replace(day=1) +
                                timedelta(days=32)
                            ).replace(day=1)
                        )
                    # auto_renew behaviour
                    if order_line.product_id.is_auto_renew:
                        creation_data['is_auto_renew'] = True
                        creation_data[
                            'auto_renew_interval'
                        ] = order_line.product_id.auto_renew_interval
                        creation_data[
                            'auto_renew_rule_type'
                        ] = order_line.product_id.auto_renew_rule_type
                    # attach to existing contract
                    if order_line.attach_to_existing_contract:
                        if order_line.contract_id:
                            creation_data[
                                'contract_id'
                            ] = order_line.contract_id.id
                        else:
                            if (
                                self.partner_id.contract_ids
                            ):
                                creation_data[
                                    'contract_id'
                                ] = self.partner_id.contract_ids[0].id
                self.env['sale.order.line'].create(
                    creation_data
                )
        self.action_set_won_rainbowman()
        return {
            'name': _('Quotation'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('sale.view_order_form').id,
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'self'
        }

# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools.translate import _


class CrmSaleOrderLine(models.Model):
    _inherit = "crm.sale.order.line"

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
    termination_interval = fields.Integer(
        default=1,
        string='Finish contract after',
        help="Finish contract (Days/Week/Month/Year)",
    )
    termination_rule_type = fields.Selection(
        [
            ('no_end', "Don't finish"),
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)'),
        ],
        default='no_end',
        string='Finish contract unit',
        help="Specify Interval for automatic renewal.",
    )
    invoice_partner_id = fields.Many2one(
        'res.partner',
        string=_("Invoice partner"),
        help="Define contact information for creating invoice"
    )

    @api.onchange('attach_to_existing_contract')
    def _empty_related_contract(self):
        for record in self:
            if not record.attach_to_existing_contract:
                record.contract_id = False

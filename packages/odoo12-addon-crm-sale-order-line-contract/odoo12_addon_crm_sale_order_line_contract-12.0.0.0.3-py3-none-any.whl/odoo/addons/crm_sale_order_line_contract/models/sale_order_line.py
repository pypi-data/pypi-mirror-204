from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    invoice_partner_id = fields.Many2one(
        'res.partner',
        string=_("Invoice partner"),
        help="Define contact information for creating invoice"
    )

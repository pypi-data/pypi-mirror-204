from odoo import models
from odoo.tools.translate import _
from odoo import exceptions


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _validate_invoice_partner(self):
        for order_line in self.order_line:
            if (
                order_line.invoice_partner_id and
                order_line.contract_id
            ):
                raise exceptions.ValidationError(
                    _("We cannot define a invoice_partner \
                    if the line has a related contract defined. \
                    For defining invoice_partner on existing please setup manually \
                    and deselect from the line.")
                )

    def action_confirm(self):
        self._validate_invoice_partner()
        super().action_confirm()
        for order_line in self.order_line:
            if (
                order_line.invoice_partner_id and
                order_line.contract_id
            ):
                order_line.contract_id.write({
                    'invoice_partner_id': order_line.invoice_partner_id.id
                })
        return True

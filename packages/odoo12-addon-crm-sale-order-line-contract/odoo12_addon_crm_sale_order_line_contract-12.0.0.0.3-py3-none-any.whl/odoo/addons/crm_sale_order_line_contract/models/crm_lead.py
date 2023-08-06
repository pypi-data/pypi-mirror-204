from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models
from odoo.tools.translate import _
from odoo import exceptions


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _validate_create_quotation_from_order_line(self):
        super()._validate_create_quotation_from_order_line()
        for order_line in self.crm_order_line_ids:
            if (
                not order_line.attach_to_existing_contract and
                order_line.contract_id
            ):
                raise exceptions.ValidationError(
                    _("If related contract defined \
                    attach to existing contract must be marked.")
                )
            if not order_line.product_id.is_contract:
                if order_line.invoice_partner_id:
                    raise exceptions.ValidationError(
                        _("We cannot define a invoice_partner \
                        on a non-contract product.")
                    )
            else:
                if (
                    order_line.contract_id or
                    order_line.attach_to_existing_contract
                ):
                    if order_line.invoice_partner_id:
                        raise exceptions.ValidationError(
                            _("We cannot define invoice_partner \
                            if we pretend to attach the product \
                            to existing contract.")
                        )
            if order_line.attach_to_existing_contract:
                if (
                    self.partner_id.sale_contract_count > 1 and
                    not order_line.contract_id
                ):
                    raise exceptions.ValidationError(
                        _("Trying to attach line to contract but multiple \
                        contracts defined for partner. \
                        Please select manually.")
                    )
                if not order_line.product_id.is_contract:
                    raise exceptions.ValidationError(
                        _("Contract option selected \
                        but product is not a contract")
                    )

    def _generate_so_order_line(self, sale_order, crm_order_line):
        creation_data = self._get_base_so_order_line_creation_data(
            sale_order,
            crm_order_line
        )
        # invoice_partner
        if crm_order_line.invoice_partner_id:
            creation_data['invoice_partner_id'] = \
                crm_order_line.invoice_partner_id.id
        # contract data
        if crm_order_line.product_id.is_contract:
            # define date_start
            now = datetime.now()
            if (
                crm_order_line.contract_date_start_type ==
                'validation_date'
            ):
                date_start = now
                creation_data['date_start'] = str(
                    date_start
                )
            if (
                crm_order_line.contract_date_start_type ==
                'validation_next_month'
            ):
                date_start = (
                    now.replace(day=1) +
                    timedelta(days=32)
                ).replace(day=1)
                creation_data['date_start'] = str(
                    date_start
                )
            # define termination
            if (
                crm_order_line.termination_rule_type == 'daily'
            ):
                creation_data['date_end'] = str(
                    date_start + relativedelta(
                        days=+crm_order_line.termination_interval
                    )
                )
            if (
                crm_order_line.termination_rule_type == 'weekly'
            ):
                creation_data['date_end'] = str(
                    date_start + relativedelta(
                        weeks=+crm_order_line.termination_interval
                    )
                )
            if (
                crm_order_line.termination_rule_type == 'monthly'
            ):
                creation_data['date_end'] = str(
                    date_start + relativedelta(
                        months=+crm_order_line.termination_interval
                    )
                )
            if (
                crm_order_line.termination_rule_type == 'yearly'
            ):
                creation_data['date_end'] = str(
                    date_start + relativedelta(
                        years=+crm_order_line.termination_interval
                    )
                )
            # invoicing timeframe
            creation_data['recurring_rule_type'] = \
                crm_order_line.product_id.recurring_rule_type

            # auto_renew behaviour
            if crm_order_line.product_id.is_auto_renew:
                creation_data['is_auto_renew'] = True
                creation_data[
                    'auto_renew_interval'
                ] = crm_order_line.product_id.auto_renew_interval
                creation_data[
                    'auto_renew_rule_type'
                ] = crm_order_line.product_id.auto_renew_rule_type
            # attach to existing contract
            if crm_order_line.attach_to_existing_contract:
                if crm_order_line.contract_id:
                    creation_data[
                        'contract_id'
                    ] = crm_order_line.contract_id.id
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

from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    block_days = fields.Float("Blocking Days Limit")
    credit_limit = fields.Float("Credit Amount Limit")
    credit_days = fields.Float("Current Credit Days", compute='_compute_credit_days')
    credit_amount = fields.Float("Current Credit Amount", compute='_compute_credit_amount')

    # @api.onchange('credit_limit')
    @api.depends('credit_amount')
    def _compute_credit_amount(self):
        for data in self:
            data.credit_amount = 0           
            query = """
                WITH x AS (
                    SELECT
                        COALESCE(amount_residual,0) as amount_residual,
                        COALESCE(CURRENT_DATE-invoice_date_due,0) as date_diff
                    FROM
                        account_move
                    WHERE
                        partner_id = {partner_id}
                        AND move_type = 'out_invoice'
                        AND payment_state IN ('not_paid','partial')
                        AND amount_residual > 0
                    ORDER BY invoice_date_due ASC
                    LIMIT 1
                ),
                y AS (
                    SELECT 
                        COALESCE(SUM(amount_residual),0) as amount_residual_total
                    FROM
                        account_move
                    WHERE
                        partner_id = {partner_id}
                        AND move_type = 'out_invoice'
                        AND payment_state IN ('not_paid','partial')
                        AND amount_residual > 0
                )
                SELECT 
                    x.amount_residual,
                    x.date_diff,
                    y.amount_residual_total
                FROM x, y;
            """.format(partner_id=data.id)

            self._cr.execute(query)
            results = self._cr.fetchone()
            if results and results[2]:
                data.credit_amount = results[2]

    @api.depends('credit_days')
    def _compute_credit_days(self):
        for data in self:
            data.credit_days = 0
            query = """
                WITH x AS (
                    SELECT
                        COALESCE(amount_residual,0) as amount_residual,
                        COALESCE(CURRENT_DATE-invoice_date_due,0) as date_diff
                    FROM
                        account_move
                    WHERE
                        partner_id = {partner_id}
                        AND move_type = 'out_invoice'
                        AND payment_state IN ('not_paid','partial')
                        AND amount_residual > 0
                    ORDER BY invoice_date_due ASC
                    LIMIT 1
                ),
                y AS (
                    SELECT 
                        COALESCE(SUM(amount_residual),0) as amount_residual_total
                    FROM
                        account_move
                    WHERE
                        partner_id = {partner_id}
                        AND move_type = 'out_invoice'
                        AND payment_state IN ('not_paid','partial')
                        AND amount_residual > 0
                )
                SELECT 
                    x.amount_residual,
                    x.date_diff,
                    y.amount_residual_total
                FROM x, y;
            """.format(partner_id=data.id)

            self._cr.execute(query)
            results = self._cr.fetchone()
            if results and results[1]:
                data.credit_days = results[1]
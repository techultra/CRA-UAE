from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'purchase.order.line'

    expected_delivery_date = fields.Datetime(string="Expected Deliver Date")
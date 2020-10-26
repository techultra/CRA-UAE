from odoo import fields, models, _


class Contract(models.Model):
    _inherit = 'hr.contract'

    variable = fields.Monetary('Variable', required=True, tracking=True)
    limit = fields.Selection([('limited', 'Limited'),
                              ('unlimited', 'Unlimited')], string="Limit")

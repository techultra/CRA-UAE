from odoo import fields, models, api

class Contract(models.Model):
    _inherit = 'hr.contract'

    fixed_portion = fields.Monetary('Fixed Portion', tracking=True)
    variable = fields.Monetary('Variable', tracking=True)
    limit = fields.Selection([('limited', 'Limited'),
                              ('unlimited', 'Unlimited')], string="Limit")



    @api.onchange('fixed_portion','variable')
    def _onchange_fixed_portion(self):
        for rec in self:
            rec.wage=rec.fixed_portion+rec.variable
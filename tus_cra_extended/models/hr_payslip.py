from odoo import fields, models, _


class HrPayroll(models.Model):
    _inherit = 'hr.payslip'

    over_time = fields.Float(string="Over Time")
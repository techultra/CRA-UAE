from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class HolidaysTypes(models.Model):
    _inherit = 'hr.leave.type'

    is_unpaid = fields.Boolean(string="Is Unpaid")

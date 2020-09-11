from odoo import api, fields, models


class Account(models.Model):
    _inherit = 'account.move'

    def get_delivery_order(self):
        sale_order = self.env['sale.order'].search([('invoice_ids', 'in', self.ids)])
        return ', '.join(sale_order.picking_ids.mapped('name'))

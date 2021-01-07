from odoo import models, fields


class ProjectReport(models.TransientModel):
    _name = 'gratuity.report'
    _description = "Gratuity Report"

    date_from = fields.Date(string='Date Due')

    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_from': self.date_from,
            },
        }
        return self.env.ref('tus_cra_extended.gratuity_report_action').report_action(self, data=data)
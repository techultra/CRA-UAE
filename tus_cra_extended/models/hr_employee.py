from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, _, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Employee(models.Model):
    _inherit = 'hr.employee'

    date_of_join = fields.Date('Joining Date', track_visibility='onchange')
    date_of_leave = fields.Date('Leaving Date', track_visibility='onchange')
    total_service_year = fields.Char(compute='_get_service_year', string="Total Service Year")
    iban_card_number = fields.Char(string='IBAN/RATIBI card number')

    def _get_service_year(self):
        """
            Calculate the total no of years, total no of months.
        """
        for rec in self:
            if rec.date_of_join and datetime.strptime(str(rec.date_of_join), DEFAULT_SERVER_DATE_FORMAT) < datetime.strptime(
                    str(datetime.today().date().strftime(DEFAULT_SERVER_DATE_FORMAT)), DEFAULT_SERVER_DATE_FORMAT):
                if rec.date_of_leave:
                    diff = relativedelta(datetime.strptime(str(rec.date_of_leave), DEFAULT_SERVER_DATE_FORMAT),
                                         datetime.strptime(str(rec.date_of_join), DEFAULT_SERVER_DATE_FORMAT))
                else:
                    diff = relativedelta(datetime.today(),
                                         datetime.strptime(str(rec.date_of_join), DEFAULT_SERVER_DATE_FORMAT))
                rec.total_service_year = " ".join([str(diff.years), 'Years', str(diff.months), "Months", str(diff.days), "Days"])
            else:
                rec.total_service_year = "0 Years 0 Months 0 Days"
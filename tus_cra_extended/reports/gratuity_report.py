from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class EmployeeGratuity(models.AbstractModel):
    _name = 'report.tus_cra_extended.gratuity_report'
    _description = 'Employee Gratuity Report'

    def _get_report_values(self, docids, data=None):
        employee_data = []
        date_from = data['form']['date_from']
        start_date = datetime.strptime(date_from, DATE_FORMAT)
        employees = self.env['hr.employee'].search([])
        for employee in employees:
            if employee.date_of_join and datetime.strptime(str(employee.date_of_join),
                                                           DEFAULT_SERVER_DATE_FORMAT) < datetime.strptime(
                    str(start_date.strftime(DEFAULT_SERVER_DATE_FORMAT)), DEFAULT_SERVER_DATE_FORMAT):
                if employee.date_of_leave:
                    diff = relativedelta(datetime.strptime(str(employee.date_of_leave), DEFAULT_SERVER_DATE_FORMAT),
                                         datetime.strptime(str(employee.date_of_join), DEFAULT_SERVER_DATE_FORMAT))
                else:
                    diff = relativedelta(start_date,
                                         datetime.strptime(str(employee.date_of_join), DEFAULT_SERVER_DATE_FORMAT))
            gratuity = 0.00
            wage = employee.contract_id.wage
            daily_wage = wage / 30
            if employee.contract_id.limit == 'limited':
                if diff.years < 1:
                    gratuity = 0.00
                if diff.years > 1 and diff.years < 5:
                    gratuity = daily_wage * 21 * diff.years
                    if diff.months:
                        gratuity = gratuity + ((wage / 12) * diff.months)
                    if diff.days:
                        gratuity = gratuity + ((wage / 30) * diff.days)
                if diff.years > 5:
                    gratuity = (daily_wage * 21 * 5) + (daily_wage * 30 * (diff.years - 5))
                    if diff.months:
                        gratuity = gratuity + ((wage / 12) * diff.months)
                    if diff.days:
                        gratuity = gratuity + ((wage / 30) * diff.days)
            if employee.contract_id.limit == 'unlimited':
                if diff.years < 1:
                    gratuity = 0.00
                if diff.years > 1 and diff.years < 3:
                    gratuity = daily_wage * 21 * diff.years * (1/3)
                    if diff.months:
                        gratuity = gratuity + ((wage / 12) * diff.months)
                    if diff.days:
                        gratuity = gratuity + ((wage / 30) * diff.days)
                if diff.years > 3 and diff.years < 5:
                    gratuity = daily_wage * 21 * diff.years * (2 / 3)
                    if diff.months:
                        gratuity = gratuity + ((wage / 12) * diff.months)
                    if diff.days:
                        gratuity = gratuity + ((wage / 30) * diff.days)
                if diff.years > 5:
                    gratuity = (daily_wage * 21 * 5) + (daily_wage * 30 * (diff.years - 5))
                    if diff.months:
                        gratuity = gratuity + ((wage / 12) * diff.months)
                    if diff.days:
                        gratuity = gratuity + ((wage / 30) * diff.days)
            if gratuity > wage * 24:
                gratuity = wage * 24
            else:
                gratuity = gratuity
            employee_data.append((employee.name, gratuity))
        return {
            'doc_ids': self.ids,
            'doc_model': 'gratuity.report',
            'data': data,
            'employee_data': employee_data,
            'date': date_from,
        }

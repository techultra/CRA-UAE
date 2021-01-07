from datetime import datetime
import math
from dateutil.relativedelta import relativedelta
from datetime import timedelta
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
        leave_count = 0
        for employee in employees:
            hr_leaves = self.env['hr.leave'].search([('employee_id', '=', employee.id), ('state', '=', 'validate'),
                                                     ('holiday_status_id.is_unpaid', '=', True)])
            if hr_leaves:
                leave_count = int(sum(hr_leaves.mapped('number_of_days')))

            if employee.date_of_join and datetime.strptime(str(employee.date_of_join),
                                                           DEFAULT_SERVER_DATE_FORMAT) < datetime.strptime(
                str(start_date.strftime(DEFAULT_SERVER_DATE_FORMAT)), DEFAULT_SERVER_DATE_FORMAT):
                if employee.date_of_leave:
                    diff = relativedelta(datetime.strptime(str(employee.date_of_leave), DEFAULT_SERVER_DATE_FORMAT),
                                         datetime.strptime(str(employee.date_of_join), DEFAULT_SERVER_DATE_FORMAT))
                    diff -= relativedelta(days=leave_count)
                    days = ((employee.date_of_leave - employee.date_of_join).days) - leave_count
                else:
                    diff = relativedelta(start_date,
                                         datetime.strptime(str(employee.date_of_join), DEFAULT_SERVER_DATE_FORMAT))
                    days = ((start_date.date() - employee.date_of_join).days) - leave_count
                    diff -= relativedelta(days=leave_count)
            gratuity = 0.00
            wage = employee.contract_id.fixed_portion
            daily_wage = wage / 30
            gratuity_termination = 0.00

            '''for Termination'''
            if diff.years < 1:
                gratuity_termination = 0.00
            if diff.years >= 1 and diff.years < 5:
                gratuity_termination = daily_wage * 21 * diff.years

                if diff.months:
                    gratuity_termination = gratuity_termination + ((21) *(daily_wage) * (diff.months/12))
                if diff.days:
                    gratuity_termination = gratuity_termination + ((21) * (daily_wage) * (diff.days/365))
            if diff.years >= 5:
                gratuity_termination = (daily_wage * 21 * 5) + (daily_wage * 30 * (diff.years - 5))
                if diff.months:
                    gratuity_termination = gratuity_termination + ((30) *(daily_wage) * (diff.months/12))
                if diff.days:
                    gratuity_termination = gratuity_termination + (30 * daily_wage * (diff.days/365))

            if employee.contract_id.limit == 'limited':
                '''for resignation'''
                if diff.years < 1:
                    gratuity = 0.00
                if diff.years >= 1 and diff.years < 5:
                    gratuity = daily_wage * 21 * diff.years
                    if diff.months:
                        gratuity = gratuity + ((21) * (daily_wage) * (diff.months / 12))
                    if diff.days:
                        gratuity = gratuity + ((21) * (daily_wage) * (diff.days / 365))
                if diff.years >= 5:
                    gratuity = (daily_wage * 21 * 5) + (daily_wage * 30 * (diff.years - 5))
                    if diff.months:
                        gratuity = gratuity + ((30) * (daily_wage) * (diff.months / 12))
                    if diff.days:
                        gratuity = gratuity + (30 * daily_wage * (diff.days / 365))
            if employee.contract_id.limit == 'unlimited':
                '''for resignation'''
                if diff.years < 1:
                    gratuity = 0.00
                if diff.years >= 1 and diff.years < 3:
                    gratuity = daily_wage * 7 * diff.years
                    if diff.months:
                        gratuity = gratuity + (7 * daily_wage * (diff.months / 12))
                    if diff.days:
                        gratuity = gratuity + (7 * daily_wage * (diff.days / 365))
                if diff.years >= 3 and diff.years < 5:
                    gratuity = daily_wage * (14) * diff.years
                    if diff.months:
                        gratuity = gratuity + ((14) * (daily_wage) * (diff.months / 12))
                    if diff.days:
                        gratuity = gratuity + ((14) * daily_wage * (diff.days / 365))
                if diff.years >= 5:
                    gratuity = (daily_wage * 21 * 5) + (daily_wage * 30 * (diff.years - 5))
                    if diff.months:
                        gratuity = gratuity + (30 * daily_wage * (diff.months / 12))
                    if diff.days:
                        gratuity = gratuity + (30 * daily_wage * (diff.days / 365))
            if gratuity > wage * 24:
                gratuity = math.ceil(wage * 24)
                gratuity_termination = math.ceil(wage * 24)
            else:
                gratuity = math.ceil(gratuity)
                gratuity_termination = math.ceil(gratuity_termination)
            employee_data.append((employee.name, employee.date_of_join, employee.total_service_year, gratuity, gratuity_termination))
        return {
            'doc_ids': self.ids,
            'doc_model': 'gratuity.report',
            'data': data,
            'employee_data': employee_data,
            'date': date_from,
        }

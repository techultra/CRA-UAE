import base64
# from xlsxwriter.workbook import Workbook
# from cStringIO import
from io import BytesIO
from datetime import date
from odoo import models, fields
from odoo.tools.misc import xlwt


class PayslipXlsx(models.TransientModel):

    _name = "payslip.xls"

    report_excel_file = fields.Binary('Download Report Excel')
    report_file_name = fields.Char('Excel File')


class PaySlipReport(models.TransientModel):
    _name = 'payslip.report'
    _description = "Payslip Report"

    month = fields.Selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'),
                              ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'),
                              ('11', 'November'), ('12', 'December')], string="Months")

    def generate_report(self):
        filename = 'Payslip Report.xls'
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet('Payslip Report')
        style = xlwt.easyxf('font:height 200, bold True, name Arial;align: horiz left;')
        style2 = xlwt.easyxf('font:height 200, bold False, name Calibri; align: horiz center; borders: left thin, right thin, top thin, bottom thin;')
        style_main_header = xlwt.easyxf('font: height 230, bold True, color black;\
                                                   borders: left thin, right thin, top thin, bottom thin;\
                                                   pattern: pattern solid, fore_color white; align:  horizontal center, wrap on, vertical center;')
        style_main_bottom = xlwt.easyxf('font: height 230, bold True, color black;\
                                                           borders: left thin, right thin, top thin, bottom thin;\
                                                           pattern: pattern solid, fore_color white; align:  horizontal right, wrap on, vertical center;')
        worksheet.row(0).height = 320
        worksheet.col(0).width = 4000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 5000
        worksheet.col(6).width = 5000
        worksheet.col(7).width = 5000
        worksheet.col(8).width = 5000
        worksheet.col(9).width = 5000
        worksheet.col(10).width = 5000
        worksheet.col(11).width = 5000
        worksheet.col(12).width = 5000
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.MEDIUM
        border_style = xlwt.XFStyle()  # Create Style
        border_style.borders = borders

        worksheet.write_merge(0, 1, 0, 0, 'SI.No', style_main_header)
        worksheet.write_merge(0, 1, 1, 1, 'NAME OF THE EMPLOYEE', style_main_header)
        worksheet.write_merge(0, 1, 2, 2, 'WORK PERMIT NO (8 DIGIT NO)', style_main_header)
        worksheet.write_merge(0, 1, 3, 3, 'PERSONAL NO (14 DIGIT NO)', style_main_header)
        worksheet.write_merge(0, 1, 4, 4, 'BANK NAME', style_main_header)
        worksheet.write_merge(0, 1, 5, 5, 'IBAN /RATIBI CARD NUMBER', style_main_header)
        worksheet.write_merge(0, 1, 6, 6, 'NO OF DAYS ABSENT', style_main_header)
        worksheet.write_merge(0, 1, 7, 7, 'FIXED PORTION', style_main_header)
        worksheet.write_merge(0, 1, 8, 8, 'VARIABLE', style_main_header)
        worksheet.write_merge(0, 1, 9, 9, 'OVER TIME', style_main_header)
        worksheet.write_merge(0, 1, 10, 10, 'Total Payment', style_main_header)
        worksheet.write_merge(0, 1, 11, 11, '', style_main_header)
        worksheet.write_merge(0, 1, 12, 12, '', style_main_header)

        row = 1
        column = 0
        payslip = self.env['hr.payslip'].search([])
        fixed_portion_sum=0
        variable_sum=0
        over_time_sum=0
        total_sum=0
        count = 0
        for data in payslip:
            absent_days=0
            for day in data.worked_days_line_ids:
                if day.work_entry_type_id.name != "Attendance":
                    absent_days=absent_days+day.number_of_days
            if data.date_from.strftime("%m") == self.month:
                row += 1
                count += 1
                worksheet.write(row, column, count, style2)
                worksheet.write(row, column + 1, data.employee_id.name or '', style2)
                worksheet.write(row, column + 2, data.employee_id.permit_no or '', style2)
                worksheet.write(row, column + 3, data.employee_id.phone or '', style2)
                worksheet.write(row, column + 4, data.employee_id.bank_account_id.bank_name or '', style2)
                worksheet.write(row, column + 5, data.employee_id.iban_card_number or '', style2)
                worksheet.write(row, column + 6, absent_days or '', style2)
                fixed_portion_sum=fixed_portion_sum+data.contract_id.fixed_portion
                worksheet.write(row, column + 7, data.contract_id.fixed_portion or '', style2)
                variable_sum=variable_sum+data.contract_id.variable
                worksheet.write(row, column + 8, data.contract_id.variable or '', style2)
                over_time_sum=over_time_sum+(data.over_time*20)
                worksheet.write(row, column + 9, data.over_time*20 or '', style2)
                total_sum=total_sum+data.contract_id.fixed_portion+data.contract_id.variable+(data.over_time*20)
                worksheet.write(row, column + 10, data.contract_id.fixed_portion+data.contract_id.variable+(data.over_time*20) or '', style2)
                # worksheet.write(row, column + 3, data.permit_no or '', style2)
                # worksheet.write(row, column + 3, data.permit_no or '', style2)
        row += 1
        worksheet.write_merge(row,row,0, 6 , 'Total', style_main_bottom)
        worksheet.write(row, 7, fixed_portion_sum, style_main_header)
        worksheet.write(row, 8, variable_sum, style_main_header)
        worksheet.write(row, 9, over_time_sum, style_main_header)
        worksheet.write(row, 10, total_sum, style_main_header)

        fp = BytesIO()
        workbook.save(fp)
        export_id = self.env['payslip.xls'].create(
            {'report_excel_file': base64.encodestring(fp.getvalue()), 'report_file_name': filename})
        fp.close()
        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'payslip.xls',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
        }
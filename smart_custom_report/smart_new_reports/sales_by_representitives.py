from odoo import models, fields, api

class EmployeeInvoiceReportLine(models.TransientModel):
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')

    @api.model
    def generate_report(self,date_from,date_to):
        self.ensure_one()
        self.env.cr.execute("""
            SELECT 
                he.name as employee_name,
                COUNT(CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE NULL END) AS invoice_count,
                SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_total ELSE 0 END) AS total_sales,
                SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_total ELSE 0 END) AS total_returns,
                (SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_total ELSE 0 END) - 
                 SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_total ELSE 0 END)) AS net_sales,
                SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_total - am.amount_residual ELSE 0 END) - 
                SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_total - am.amount_residual ELSE 0 END) AS total_paid,
                SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_residual ELSE 0 END) - 
                SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_residual ELSE 0 END) AS not_paid
            FROM 
                account_move am
            JOIN 
                hr_employee he ON am.x_studio_employee = he.id
            WHERE 
                am.x_studio_employee IS NOT NULL
                AND he.department_id = 3
                AND am.date >= %s AND am.date <= %s
            GROUP BY 
                am.x_studio_employee, he.name;
            """, ( date_from, date_to))

        result = self.env.cr.fetchall()
        report_lines_vals = []
        for row in result:
            report_lines_vals.append({
                'employee_name': row[0],
                'invoice_count': row[1],
                'total_sales': row[2],
                'total_returns': row[3],
                'net_sales': row[4],
                'total_paid': row[5],
                'not_paid': row[6],
            })

        return report_lines_vals
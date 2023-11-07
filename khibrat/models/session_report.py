from odoo import api, fields, models, _
import base64

class Session_Report(models.Model):
    _name = "session.report"
    _rec_name= 'report_name'
    _inherit = 'mail.thread'
    
    report_name=fields.Char(string="اسم المستند")
    report_file= fields.Binary(string="المستند")

    case_id_report=fields.Many2one('cases.data',string='رقم الدعوى')
    session_report_id= fields.Many2one('sessions.data',string="رقم الجلسة")

    def action_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'عرض التقرير',
            'view_mode': 'form',
            'res_model': 'session.report',
            'res_id': self.id,
            # 'domain': [('driver_id', '=', self.id)],
            'context': "{'create': False}"
        }
    
    def action_email_report(self):
        template = self.env.ref('khibrat.sending_mail_template')
        for rec in self:
            attachment_name = rec.report_name
            attachment_data = rec.report_file

            # Clear existing attachments
            template.attachment_ids = [(5, 0, 0)]

            template.write({
                'attachment_ids': [(0, 0, {
                    'name': attachment_name,
                    'datas': attachment_data,
                    # 'datas_fname': attachment_name,
                })],
            })
            template.send_mail(rec.id, force_send=True)
    

    # def action_email_report(self):
    #     # Get the report template
    #     report = self.env.ref('khibrat.sending_mail_template') # Replace with your report template name

    #     # Render the report as PDF
    #     report_vals = report.render_qweb_pdf(self.ids)
        

    #     # Get the email template
    #     email_template = self.env.ref('khibrat.sending_mail_template.id')  # Replace with your email template XML ID

    #     # Replace the attachment placeholder with the actual attachment
    #     attachment_name = report_vals.get('report_name')
    #     attachment_data = report_vals.get('report_file')

    #     email_template.write({
    #         'attachment_ids': [(0, 0, {
    #             'name': attachment_name,
    #             'datas': attachment_data,
    #             'datas_fname': attachment_name,
    #         })],
    #     })

    #     # Send the email using the updated template
    #     email_template.send_mail(self.id, force_send=True)


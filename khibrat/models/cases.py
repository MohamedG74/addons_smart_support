from odoo import api, fields, models, _
from datetime import datetime
from .hijri_converter.convert import Gregorian, Hijri
from random import randint
from odoo.exceptions import ValidationError
from lxml import etree

class Cases(models.Model):
    _name = "cases.data"

    prosecution_number= fields.Char(string="رقم الدعوى")

    branch=fields.Selection([('الرياض','الرياض'),
                            ('جدة','جدة'),], string="الفرع")

    partner_id = fields.Many2one('res.partner', string='اسم العميل', required=True)
    company = fields.Char(string='طبيعة العميل')


    registration_date = fields.Date(string="تاريخ القيد")

    hijri_date = fields.Char(string='التاريخ الهجرى', compute="_compute_hijri_date",readonly=True)

    prosecution_type = fields.Many2one('case.type', string="نوع الدعوى", store=True)

    stage=fields.Selection([('دراسة القضية','دراسة القضية'),
                            ('تجهيز القضية','تجهيز القضية'),
                            ('المرحلة الإبتدائية','المرحلة الإبتدائية'),
                            ('المرحلة الإستئنافية الاولى','المرحلة الإستئنافية الاولى'),
                            ('مرحلة التنفيذ','مرحلة التنفيذ'),
                            ('المرحلة العليا الاولى','المرحلة العليا الاولى'),
                            ('المرحلة الإستئنافية الثانية','المرحلة الإستئنافية الثانية'), 
                            ('المرحلة العليا الثانية','المرحلة العليا الثانية'),
                            ('مرحلة الانتهاء','مرحلة الانتهاء'),], default='دراسة القضية',
                            string="المرحلة", group_expand='_group_expand_states')

    resumption_side=fields.Char(string="الجهة المستأنفة")

    resumption_number=fields.Char(string="رقم قيد الإستئناف")

    resumption_date=fields.Date(string="تاريخ قيد الإستئناف")
    resumption_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_resumption_date_hijri",readonly=True)


    demands=fields.Selection([('financial', 'مالى'),('not_financial','غير مالى'),('else','أخرى')],string="الطلبات")
    notes = fields.Text(string="طلبات أخرى")
    not_financial_notes = fields.Text(string="طلبات غير مالى")


    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        help="Utility field to express amount currency")

    defendants_rights_x=fields.Monetary(string="اصل الحق المُدعى عليه", currency_field='company_currency_id')

    compensation_x=fields.Monetary(string="التعويض", currency_field='company_currency_id')

    fees_x=fields.Monetary(string="أتعاب المحاماه", currency_field='company_currency_id')

    total_X=fields.Monetary(string="إجمالى المبلغ المطلوب", currency_field='company_currency_id')

    @api.onchange('defendants_rights_x', 'compensation_x', 'fees_x')
    def onchange_field_x(self):
        if self.defendants_rights_x or self.compensation_x or self.fees_x:
            self.total_X = self.defendants_rights_x + self.compensation_x + self.fees_x 

    #بيانات المرحلة الإستئنافية الثانية 
    resumption_side_2=fields.Char(string="الجهة المستأنفة")

    resumption_number_2=fields.Char(string="رقم قيد الإستئناف")

    resumption_date_2=fields.Date(string="تاريخ قيد الإستئناف")
    resumption_date_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_resumption_date_2_hijri",readonly=True)


    demands_2=fields.Selection([('financial', 'مالى'),('not_financial','غير مالى'),('else','أخرى')],string="الطلبات")
    notes_2 = fields.Text(string="طلبات أخرى")
    not_financial_notes_2 = fields.Text(string="طلبات غير مالى")


    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        help="Utility field to express amount currency")

    defendants_rights_2=fields.Monetary(string="اصل الحق المُدعى عليه", currency_field='company_currency_id')

    compensation_2=fields.Monetary(string="التعويض", currency_field='company_currency_id')

    fees_2=fields.Monetary(string="أتعاب المحاماه", currency_field='company_currency_id')

    total_2=fields.Monetary(string="إجمالى المبلغ المطلوب", currency_field='company_currency_id')

    @api.onchange('defendants_rights_2', 'compensation_2', 'fees_2')
    def onchange_field(self):
        if self.defendants_rights_2 or self.compensation_2 or self.fees_2:
            self.total_2 = self.defendants_rights_2 + self.compensation_2 + self.fees_2 


    #بيانات المرحلة العليا الاولى 
    objecting_side=fields.Char(string="الجهة المعترضية")
    objecting_number=fields.Char(string="رقم قيد الإعتراض")
    
    objecting_date=fields.Date(string="تاريخ قيد الإعتراض")
    objecting_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_objecting_date_hijri",readonly=True)
    
    supreme_circle=fields.Boolean(string="الدائرة العليا", default=False)
    temporary_decision=fields.Selection([('x_1', 'وقف التنفيذ'),('x_2','تبادل مذكرات')], string="القرار المؤقت" ,default='x_1')

    #وقف التنفيذ
    stay_of_execution_number=fields.Char(string="رقم وقف التنفيذ")
    stay_of_execution_date=fields.Date(string="تاريخ وقف التنفيذ")
    stay_of_execution_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_stay_of_execution_date_hijri", readonly=True)
    stay_of_execution_spoken=fields.Char(string="منطوق وقف التنفيذ")
    stay_of_execution_date_pickup=fields.Date(string="تاريخ استلام وقف التنفيذ")
    stay_of_execution_date_pickup_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_stay_of_execution_date_pickup_hijri", readonly=True)



    #بيانات المرحلة العليا الثانية 
    objecting_side_2=fields.Char(string="الجهة المعترضية")
    objecting_number_2=fields.Char(string="رقم قيد الإعتراض")
    objecting_date_2=fields.Date(string="تاريخ قيد الإعتراض")
    objecting_date_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_objecting_date_2_hijri", readonly=True)
    supreme_circle_2=fields.Boolean(string="الدائرة العليا", default=False)
    temporary_decision_2=fields.Selection([('x_3', 'وقف التنفيذ'),('x_4','تبادل مذكرات')],string="القرار المؤقت" ,default='x_3')

    #وقف التنفيذ
    stay_of_execution_number_2=fields.Char(string="رقم وقف التنفيذ")
    
    stay_of_execution_date_2=fields.Date(string="تاريخ وقف التنفيذ")
    stay_of_execution_date_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_stay_of_execution_date_2_hijri", readonly=True)
    
    stay_of_execution_spoken_2=fields.Char(string="منطوق وقف التنفيذ")
    
    stay_of_execution_date_pickup_2=fields.Date(string="تاريخ استلام وقف التنفيذ")
    stay_of_execution_date_pickup_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_stay_of_execution_date_pickup_2_hijri", readonly=True)

    #دراسة القضية
    list_lawsuit_name=fields.Char(string="اسم المستند")
    list_lawsuit=fields.Binary(string="لائحة الدعوى")

    list_lawsuit_pic=fields.Many2many('ir.attachment', string="صور المستندات")
    notes_1=fields.Text(string="ملاحظات")

    #رفع الاخطار
    attachment_name=fields.Char(string="اسم المستند")
    attachment=fields.Binary(string="الإخطار")

    #مهلة خاصة بانهاء دراسة القضية
    start_date = fields.Datetime(string="من")
    start_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_start_date_hijri", readonly=True)
    end_date = fields.Datetime(string="الى")
    end_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_end_date_hijri", readonly=True)



    #فيما يخص نقل قضيه من مرحله الى مرحله 
    from_primary_to_resumption_name=fields.Char(string="اسم المستند")
    from_primary_to_resumption=fields.Binary(string="إرفاق إعتراض الخصم لدى الاستئنافية الاولى")

    from_resumption_2_to_supreme_name=fields.Char(string="اسم المستند")
    from_resumption_2_to_supreme=fields.Binary(string="إرفاق إعتراض الخصم لدى العليا الاولى")

    from_resumption_to_resumption_name_2=fields.Char(string="اسم المستند")
    from_resumption_to_resumption_2=fields.Binary(string="قرار العليا الاولى بنقل القضية الى الاستئنافية الثانية ")
    

    from_supreme_to_supreme_name_2=fields.Char(string="اسم المستند")
    from_supreme_to_supreme_2=fields.Binary(string="إرفاق إعتراض الخصم لدى العليا الثانية")


    name_of_day=fields.Char(string='اليوم')

    lawyer_ids=fields.One2many('lawyers.data','lawyer_id',string='المحامون')
    lawyer_many2many_ids=fields.Many2many('lawyers.data',string='المحامون')

    client_ids=fields.One2many('clients.data','client_id',string='المُدعى')
    client_many2many_ids=fields.Many2many('clients.data',string='المُدعى')

    defendant_ids=fields.One2many('defendant.data','defendant_id',string='المُدعى عليه')
    defendant_many2many_ids=fields.Many2many('defendant.data',string='المُدعى عليه')

    interfering_ids=fields.One2many('interfering.data','interfering_id',string='الجهة المتدخلة')
    interfering_many2many_ids=fields.Many2many('interfering.data',string='الجهة المتدخلة')
    
    entries_ids=fields.One2many('entries.data','entries_id',string='الجهة المدخلة')
    entries_many2many_ids=fields.Many2many('entries.data',string='الجهة المدخلة')

    document_ids=fields.One2many('document.data','document_id',string='المستندات')

    demands_ids=fields.One2many('demands.data','demands_id',string='الطلبات')

    session_ids=fields.One2many('sessions.data','case_id',string='الجلسات')

    primary_judgment_ids=fields.One2many('primary.judgment','primary_judgment_id',string='الحكم الابتدائى')

    appellate_judgment_ids=fields.One2many('appellate.judgment','appellate_judgment_id',string='الحكم الاستئنافى')
    appellate_judgment_ids_second=fields.One2many('appellate.judgmentsecond','appellate_judgment_id_2',string='الحكم الاستئنافى الثاني')

    final_requests_ids=fields.One2many('final.requests','final_requests_id',string='الطلبات الختامية')

    final_judgment_ids=fields.One2many('final.judgment','final_judgment_id',string='الحكم النهائى الاول')
    final_judgment_ids_second=fields.One2many('final.judgmentsecond','final_judgment_id_2',string='الحكم النهائى الثاني')
    
    exchange_notes_ids=fields.One2many('exchange.notes','exchange_notes_id',string='تبادل مذكرات')


    #document_added_by_user_id
    document_added_by_user_id = fields.Integer(string="user id")
    document_added_by_user_name = fields.Char(string="user name")

    #حالة القضية
    case_status=fields.Selection([('منظورة', 'منظورة'),('منتهية','منتهية')],string="حالة القضية")


    #الصفة
    client_or_defendant=fields.Char(string="الصفة", compute="_compute_client_or_defendant", readonly=True)

    @api.depends('partner_id', 'client_many2many_ids', 'defendant_many2many_ids')
    def _compute_client_or_defendant(self):
        for rec in self:
            if rec.partner_id:
                if rec.partner_id.name in rec.client_many2many_ids.mapped('name'):
                    rec.client_or_defendant = "مُدعى"
                elif rec.partner_id.name in rec.defendant_many2many_ids.mapped('name'):
                    rec.client_or_defendant = "مُدعى عليه"
                elif rec.partner_id.name not in rec.defendant_many2many_ids.mapped('name'):
                    rec.client_or_defendant = "   "



    counts_of_primary_judgments = fields.Char(string="counts of lines", compute='_compute_line_counts_of_primary_judgments')
    @api.depends('primary_judgment_ids')
    def _compute_line_counts_of_primary_judgments(self):
        for record in self:
            record.counts_of_primary_judgments = len(record.primary_judgment_ids)

    counts=fields.Char(string="counts of lines", compute='_compute_last_line_count')
    @api.depends('final_judgment_ids')
    def _compute_last_line_count(self):
        for record in self:
            record.counts = len(record.final_judgment_ids)
    
    counts_of_final_judgment_ids_second=fields.Char(string="counts of lines", compute='_compute_line_count_final_judgment_ids_second')
    @api.depends('final_judgment_ids_second')
    def _compute_line_count_final_judgment_ids_second(self):
        for record in self:
            record.counts_of_final_judgment_ids_second = len(record.final_judgment_ids_second)
    

    counts_of_appellate_judgment_ids=fields.Char(string="counts of lines", compute='_compute_line_count')
    @api.depends('appellate_judgment_ids')
    def _compute_line_count(self):
        for record in self:
            record.counts_of_appellate_judgment_ids = len(record.appellate_judgment_ids)
    
    counts_of_appellate_judgment_ids_2=fields.Char(string="counts of lines", compute='_compute_line_count_appellate_judgment_ids_second')
    @api.depends('appellate_judgment_ids_second')
    def _compute_line_count_appellate_judgment_ids_second(self):
        for record in self:
            record.counts_of_appellate_judgment_ids_2 = len(record.appellate_judgment_ids_second)


    # @api.onchange('stage')
    # def _onchange_stage(self):
    #     for rec in self:
    #         if rec.stage == ("دراسة القضية, المرحلة الإبتدائية") or not rec.prosecution_number:
    #             raise ValidationError(_("الرجاء إدخال رقم الدعوى"))
    #         elif rec.stage == ("المرحلة الإبتدائية, دراسة القضية, المرحلة الاستئنافية الاولى") or not rec.list_lawsuit and not rec.list_lawsuit_pic:
    #             raise ValidationError(_("الرجاء إرفاق لائحة الدعوى او صور المستندات"))
    
    @api.onchange('stage')
    def _onchange_stage(self):
        for rec in self:
            if rec.stage == 'المرحلة الإبتدائية' and not rec.prosecution_number:
                raise ValidationError(_("الرجاء إدخال رقم الدعوى"))
            
            elif rec.stage == 'المرحلة الإبتدائية' and not rec.attachment:
                raise ValidationError(_("الرجاء إرفاق الإخطار"))
            
            elif rec.stage == 'المرحلة الإبتدائية' and not rec.list_lawsuit:
                raise ValidationError(_("الرجاء إرفاق لائحة الدعوى"))
            
            elif not rec.list_lawsuit_pic:
                raise ValidationError(_("الرجاء إرفاق صور المستندات"))

    @api.model
    def create(self, vals):
        record = super(Cases, self).create(vals)
        record._check_transfer_fields()
        return record

    def write(self, vals):
        res = super(Cases, self).write(vals)
        self._check_transfer_fields()
        return res

    def _check_transfer_fields(self):
        for rec in self:
            #في حالة عدم تسجيل تقرير اي جلسة من الجلسات في اي مرحلة من المراحل
            for session in rec.session_ids:
                if not session.session_report_ids:
                    raise ValidationError(_("الرجاء تسجيل التقرير للجلسة رقم: %s" % session.session_number))


            if rec.stage == "مرحلة التنفيذ" and not rec.primary_judgment_ids:
                raise ValidationError(_("الرجاء إرفاق الحكم الابتدائى "))
            if rec.stage == "مرحلة التنفيذ" and rec.primary_judgment_ids and rec.from_primary_to_resumption and not rec.appellate_judgment_ids:
                raise ValidationError(_("الرجاء إرفاق الحكم الاستئنافى الاول "))



            if rec.stage == "المرحلة الإستئنافية الاولى" and not rec.from_primary_to_resumption and not rec.primary_judgment_ids:
                raise ValidationError(_("الرجاء إرفاق الحكم الابتدائى"))
            elif rec.stage == "المرحلة الإستئنافية الاولى" and not rec.from_primary_to_resumption:
                raise ValidationError(_("الرجاء إرفاق إعتراض الخصم لدى الاستئنافية الاولى"))
            
            
            


            elif rec.stage == "المرحلة العليا الاولى" and not rec.primary_judgment_ids and not rec.appellate_judgment_ids:
                raise ValidationError(_("لا يمكن نقل القضية الى العليا الاولى"))
            elif rec.stage == "المرحلة العليا الاولى" and not rec.from_resumption_2_to_supreme:
                raise ValidationError(_("الرجاء إرفاق إعتراض الخصم لدى العليا الاولى"))
            
            
            
            elif rec.stage == "المرحلة الإستئنافية الثانية" and not rec.primary_judgment_ids and not rec.appellate_judgment_ids:
                raise ValidationError(_("لا يمكن نقل القضية الى الإستئنافية الثانية"))
            
            elif rec.stage == "المرحلة العليا الثانية" and not rec.primary_judgment_ids and not rec.appellate_judgment_ids and not rec.appellate_judgment_ids:
                raise ValidationError(_("لا يمكن نقل القضية الى العليا الثانية"))
           


            elif rec.stage == "المرحلة الإستئنافية الثانية" and not rec.final_judgment_ids:
                raise ValidationError(_("الرجاء إرفاق حكم العليا الاول"))
            #لو الحكم نقض في العليا الاولى
            elif rec.stage == "المرحلة الإستئنافية الثانية" and not rec.from_resumption_to_resumption_2 and rec.final_judgment_ids.final_judgment_spoken == 'repeal':
                raise ValidationError(_("الرجاء إرفاق قرار العليا الاولى بنقل القضية الى الاستئنافية الثانية"))            
            elif rec.stage == "المرحلة العليا الثانية" and not rec.appellate_judgment_ids_second and rec.final_judgment_ids.final_judgment_spoken == 'repeal':
                raise ValidationError(_("لا يمكن نقل القضية الى العليا الثانية"))
            elif rec.stage == "مرحلة الانتهاء" and not rec.appellate_judgment_ids_second and  rec.final_judgment_ids.final_judgment_spoken == 'repeal':
                raise ValidationError(_("لا يمكن نقل القضية من العليا الاولى الى مرحلة الانتهاء"))

            #لو الحكم تأييد في العليا الاولى
            elif rec.stage == "المرحلة الإستئنافية الثانية" and not rec.from_resumption_to_resumption_2 and rec.final_judgment_ids.final_judgment_spoken == 'confirmation':
                raise ValidationError(_("لا يمكن نقل القضية من العليا الاولى الى الاستئنافية الثانية"))
            




            #لو الحكم تأييد في الاستئنافية الثانية
            elif rec.stage == "المرحلة العليا الثانية" and not rec.from_supreme_to_supreme_2 and rec.final_judgment_ids.final_judgment_spoken == 'confirmation':
                raise ValidationError(_("لا يمكن نقل القضية من العليا الاولى الى العليا الثانية"))
            
            elif rec.stage == "المرحلة العليا الثانية" and not rec.final_judgment_ids_second and rec.appellate_judgment_ids_second.appellate_judgment_spoken_2 == 'confirmation':
                raise ValidationError(_("لا يمكن نقل القضية من الإستئنافية الثانية الى العليا الثانية"))

            elif rec.stage == "المرحلة العليا الثانية" and not rec.from_supreme_to_supreme_2:
                raise ValidationError(_("الرجاء إرفاق إعتراض الخصم لدى العليا الثانية"))
            

            #لو الحكم نقض في الإستئنافية الثانية
            # elif rec.stage == "مرحلة الانتهاء" and not rec.final_judgment_ids_second:
            #     raise ValidationError(_("الرجاء إرفاق حكم العليا الثاني"))
            
            elif rec.stage == "مرحلة الانتهاء" and rec.appellate_judgment_ids_second.appellate_judgment_spoken_2 == 'repeal' and not rec.final_judgment_ids_second:
                raise ValidationError(_("الرجاء إرفاق حكم العليا الثاني"))
        


            



    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.company = self.partner_id.is_company

            if self.company == 'True':
                self.company = "Company"
            else:
                self.company = "Individual"


    def _get_default_color(self):
        return randint(1, 11)
    color = fields.Integer(string='Color', default=_get_default_color,
        help="Transparent tags are not visible in the kanban view of your projects and tasks.")


    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).stage.selection]

    @api.onchange('registration_date')
    def _compute_hijri_date(self):
        for rec in self:
            if rec.registration_date:
                rec.hijri_date = Gregorian.fromdate(rec.registration_date).to_hijri()
            else:
                rec.hijri_date = Hijri.today()

    @api.onchange('resumption_date')
    def _compute_resumption_date_hijri(self):
        for rec in self:
            if rec.resumption_date:
                rec.resumption_date_hijri = Gregorian.fromdate(rec.resumption_date).to_hijri()
            else:
                rec.resumption_date_hijri = Hijri.today()    
    
    @api.onchange('resumption_date_2')
    def _compute_resumption_date_2_hijri(self):
        for rec in self:
            if rec.resumption_date_2:
                rec.resumption_date_2_hijri = Gregorian.fromdate(rec.resumption_date_2).to_hijri()
            else:
                rec.resumption_date_2_hijri = Hijri.today()    
    
    @api.onchange('objecting_date')
    def _compute_objecting_date_hijri(self):
        for rec in self:
            if rec.objecting_date:
                rec.objecting_date_hijri = Gregorian.fromdate(rec.objecting_date).to_hijri()
            else:
                rec.objecting_date_hijri = Hijri.today()    
    
    @api.onchange('stay_of_execution_date')
    def _compute_stay_of_execution_date_hijri(self):
        for rec in self:
            if rec.stay_of_execution_date:
                rec.stay_of_execution_date_hijri = Gregorian.fromdate(rec.stay_of_execution_date).to_hijri()
            else:
                rec.stay_of_execution_date_hijri = Hijri.today()    
    
    @api.onchange('stay_of_execution_date_pickup')
    def _compute_stay_of_execution_date_pickup_hijri(self):
        for rec in self:
            if rec.stay_of_execution_date_pickup:
                rec.stay_of_execution_date_pickup_hijri = Gregorian.fromdate(rec.stay_of_execution_date_pickup).to_hijri()
            else:
                rec.stay_of_execution_date_pickup_hijri = Hijri.today()
    
    @api.onchange('objecting_date_2')
    def _compute_objecting_date_2_hijri(self):
        for rec in self:
            if rec.objecting_date_2:
                rec.objecting_date_2_hijri = Gregorian.fromdate(rec.objecting_date_2).to_hijri()
            else:
                rec.objecting_date_2_hijri = Hijri.today()    
    
    @api.onchange('stay_of_execution_date_2')
    def _compute_stay_of_execution_date_2_hijri(self):
        for rec in self:
            if rec.stay_of_execution_date_2:
                rec.stay_of_execution_date_2_hijri = Gregorian.fromdate(rec.stay_of_execution_date_2).to_hijri()
            else:
                rec.stay_of_execution_date_2_hijri = Hijri.today()    
    
    @api.onchange('stay_of_execution_date_pickup_2')
    def _compute_stay_of_execution_date_pickup_2_hijri(self):
        for rec in self:
            if rec.stay_of_execution_date_pickup_2:
                rec.stay_of_execution_date_pickup_2_hijri = Gregorian.fromdate(rec.stay_of_execution_date_pickup_2).to_hijri()
            else:
                rec.stay_of_execution_date_pickup_2_hijri = Hijri.today()    
    
    

    #مهلة خاصة بانهاء دراسة القضية    
    @api.onchange('start_date')
    def _compute_start_date_hijri(self):
        for rec in self:
            if rec.start_date:
                rec.start_date_hijri = Gregorian.fromdate(rec.start_date).to_hijri()
            else:
                rec.start_date_hijri = Hijri.today()    
    
    @api.onchange('end_date')
    def _compute_end_date_hijri(self):
        for rec in self:
            if rec.end_date:
                rec.end_date_hijri = Gregorian.fromdate(rec.end_date).to_hijri()
            else:
                rec.end_date_hijri = Hijri.today()    


    

    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id,'%s' % (rec.prosecution_number)))
        return res 


    def action_add_session(self):
        return {
            'name':'إضافة جلسة',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sessions.data',
            'context': {'default_case_id': self.id, 
                        'default_session_many2many_clients': self.client_many2many_ids.ids,
                        'default_session_many2many_defendants': self.defendant_many2many_ids.ids, 
                        'default_session_many2many_interfering_related': self.interfering_many2many_ids.ids,
                        'default_session_many2many_entries_related': self.entries_many2many_ids.ids,
                        'default_stage_in_sessions': self.stage},

            # 'context': {'default_case_id': self.id, 
            #             'default_session_clients': self.client_many2many_ids.ids,
            #             'default_session_defendants': self.defendant_many2many_ids.ids, 
            #             'default_session_interfering_related': self.interfering_many2many_ids.ids,
            #             'default_session_entries_related': self.entries_many2many_ids.ids,
            #             'default_stage_in_sessions': self.stage},
            # 'target': 'new'
        }
    
    def action_add_final_requests(self):
        return {
            'name':'إضافة طلبات ختامية',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'final.requests',
            'context': {'default_final_requests_id': self.id,
                        'default_final_request_many2many_clients': self.client_many2many_ids.ids,
                        'default_final_request_many2many_defendants': self.defendant_many2many_ids.ids, 
                        'default_final_request_many2many_interfering_related': self.interfering_many2many_ids.ids,
                        'default_final_request_many2many_entries_related': self.entries_many2many_ids.ids,
                        'default_stage_in_final_requests':self.stage,},
        }
    

    def action_add_demand(self):
        return {
            'name':'إضافة طلب',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'demands.data',
            'context': {'default_demands_id': self.id,
                        'default_stage_in_demands':self.stage},
        } 
    def action_add_document(self):
        current_user = self.env.user
        self.write({
            'document_added_by_user_id': current_user.id,
            'document_added_by_user_name': current_user.name,
        })
        return {
            'name':'إضافة مستند',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'document.data',
            'context': {'default_document_id': self.id},
        }



    def action_add_primary_judgment(self):
        return {
            'name':'إضافة حكم إبتدائي',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'primary.judgment',
            'context': {'default_primary_judgment_id': self.id,
                        'default_stage_in_primary_judgment': self.stage},
        }

    def action_add_appellate_judgment(self):
        return {
            'name':'إضافة حكم إستئنافي',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'appellate.judgment',
            'context': {'default_appellate_judgment_id': self.id,
                        'default_stage_in_appellate_judgment': self.stage},
        }
    def action_add_appellate_judgment_2(self):
        return {
            'name':'إضافة حكم إستئنافي ثاني',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'appellate.judgmentsecond',
            'context': {'default_appellate_judgment_id_2': self.id,
                        'default_stage_in_appellate_judgment_2': self.stage},
        }
    
    def action_add_final_judgment(self):
        return {
            'name':'إضافة حكم نهائي',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'final.judgment',
            'context': {'default_final_judgment_id': self.id,
                        'default_stage_in_final_judgment': self.stage},
        }

    def action_add_final_judgment_2(self):
        return {
            'name':'إضافة حكم نهائي ثاني',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'final.judgmentsecond',
            'context': {'default_final_judgment_id_2': self.id,
                        'default_stage_in_final_judgment_2': self.stage,
                        'default_final_judgment_stage_id_2' : self.stage},
        }
    
    def action_add_exchange_notes(self):
        return {
            'name':'إضافة تبادل مذكرات',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'exchange.notes',
            'context': {'default_exchange_notes_id': self.id,
                        'default_stage_in_exchange_notes':self.stage},
        }
    

# class ResConfigSettingsInherit(models.TransientModel):
#     _inherit = 'res.config.settings'

#     use_arabic_dates = fields.Boolean(string='Use Arabic Dates')

#     @api.model
#     def get_values(self):
#         res = super(ResConfigSettingsInherit, self).get_values()
#         use_arabic_dates = self.env['ir.config_parameter'].sudo().get_param('khibrat.use_arabic_dates', default=False)
#         res.update(use_arabic_dates=use_arabic_dates)
#         return res

#     def set_values(self):
#         super(ResConfigSettingsInherit, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param('khibrat.use_arabic_dates', self.use_arabic_dates)



    # @api.depends('client_many2many_ids.document_file_lawyer')  # Add dependencies as needed
    # def _compute_attachment_binary(self):
    #     template = self.env.ref('khibrat.lawyers_agency_end_date')
    #     for rec in self:
    #         attachment_name = rec.client_many2many_ids.document_name_lawyer
    #         attachment_data = rec.client_many2many_ids.document_file_lawyer

    #         # Clear existing attachments
    #         template.attachment_ids = [(5, 0, 0)]

    #         template.write({
    #             'attachment_ids': [(0, 0, {
    #                 'name': attachment_name,
    #                 'datas': attachment_data,
    #             })],
    #         })
    #         template.send_mail(rec.id, force_send=True)
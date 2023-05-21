# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.exceptions import UserError, Warning


class HRProbationAppraisal(models.Model):
    _name = 'hr.probation.appraisal'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin', 'utm.mixin']

    _description = 'HR Probation Appraisal'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    job_id = fields.Many2one('hr.job',related="employee_id.job_id")
    user_id = fields.Many2one('res.users', string="User",default=lambda self: self.env.user)
    name = fields.Char(string="Refferance", required=False, default=lambda self: _('New') )
    date = fields.Date()

    remarks = fields.Html('Remarks', translate=True)
    employee_no = fields.Char(related="employee_id.employee_no")
    recommendation = fields.Html('Recommendation')
    department_id = fields.Many2one('hr.department', related="employee_id.department_id")
    contract_id = fields.Many2one('hr.contract',related="employee_id.contract_id")
    join_date = fields.Date(related="contract_id.date_start")
    appraiser_id = fields.Many2one('hr.employee')
    appraiser_job = fields.Many2one('hr.job',related="appraiser_id.job_id")
    appraisal_line = fields.One2many('hr.probation.line','probation_id')
    
    reciewer_id = fields.Many2one('res.users','Line Manager')
    gm_user = fields.Many2one('res.users','HR Manager')
    total_score = fields.Integer('Total',compute ="compute_total_score")
    @api.depends('appraisal_line.score')
    def compute_total_score(self):
    	for x in self:
    		total_score = 0.0
    		for line in x.appraisal_line:
    			total_score += line.score
    		x.total_score = total_score

    state = fields.Selection([
            ('draft', 'Draft'),
            ('review', 'Waiting Review'),
            ('waitin_app', 'Waiting Approve'),
            ('approved','Approved'),
            ('reject','Rejected'),
        ], string='Status',default="draft", index=True, tracking=True)
    def unlink(self):
        if self.state == 'approved':
            raise UserError('You cannot delete approved probation appraisal')
        else:
            return super().unlink()
    def submit(self):
        self.state = 'review'
    def review(self):
        self.state = 'waitin_app'
        self.reciewer_id = self.env.user.id
    def waitin_app(self):
        self.state = 'approved'
        self.gm_user = self.env.user.id
    def reject(self):
        self.state = 'reject'
    def set_draft(self):
        self.state = 'draft'
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'hr.probation.appraisal') or _('New')
        res = super(HRProbationAppraisal, self).create(vals)
        return res
    def action_create_confirmation_letter(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        lang = self.env.context.get('lang')
        
        mail_template = self.env.ref('hr_appraisal_custom.email_template_confirmation', raise_if_not_found=False)

        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'hr.probation.appraisal',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

class HRProbationAppraisalLine(models.Model):
    _name = 'hr.probation.line'


    probation_id = fields.Many2one('hr.probation.appraisal')
    serial = fields.Integer('#')
    attribute = fields.Text('Attribute')
    description = fields.Text('Description')
    score = fields.Integer('Score')
    max_num = fields.Integer('Max',default="5",readonly="1")
                                       
    

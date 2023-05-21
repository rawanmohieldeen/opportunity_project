# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.exceptions import UserError, Warning


class WarningLetter(models.Model):
    _name = 'warning.letter'
    _description = 'HR Warning Letters'



    
    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id = fields.Many2one('res.users', string="User",default=lambda self: self.env.user)
    name = fields.Char(string="Title", required=False, )
    date = fields.Date()

    misconduct = fields.Html('misconduct', translate=True)
    employee_no = fields.Char(related="employee_id.employee_no")
    designation = fields.Char()
    department_id = fields.Many2one('hr.department', related="employee_id.department_id")
    employee_user = fields.Many2one('res.users',related="employee_id.user_id")

    def action_warning_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        if not self.misconduct :
            raise UserError('You have to write the warning information')
        lang = self.env.context.get('lang')
        mail_template = self.env.ref('warning_letter.email_template_warning', raise_if_not_found=False)
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'warning.letter',
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

class Employee(models.Model):
    _inherit = 'hr.employee'

    emp_type = fields.Selection([
        ('saudi', 'Saudis'),
        ('no_saudi', 'Non- Saudis'), 
       
    ], string='Type Of Employee', index=True, tracking=True,required=True)

    national_id = fields.Char(string="National ID No")
    iqama = fields.Char('Iqama')



    def _compute_termination_count(self):
        self.termination_count = self.env['hr.termination'].search_count([('employee_id', '=', self.id)])

    termination_count = fields.Integer(string="Termination Count", compute='_compute_termination_count')

    def action_create_termination_letter(self):
        termination = self.env['hr.termination'].search([('employee_id', '=', self.id)])
        action_vals = {
            'name': _('HR Termination'),
            'domain': [('id', 'in', termination.ids)],
            'view_type': 'form',
            'res_model': 'hr.termination',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
        if len(termination) > 0:
            action_vals.update({'res_id': termination[0].id, 'view_mode': 'tree,form'})
        else:
            action_vals.update({'view_mode': 'form',
                                'domain': [('employee_id', '=', self.id)],
                                'context': {
                                    "default_employee_id": self.id,

                                }})
        return action_vals
class TerminationApproval(models.Model):
    _name = 'hr.termination'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin', 'utm.mixin']

    employee_id = fields.Many2one('hr.employee')  
    
    employee_no = fields.Char(related="employee_id.employee_no")
    national_id = fields.Char(related="employee_id.national_id")
    iqama = fields.Char(related="employee_id.iqama")
    department_id = fields.Many2one(related="employee_id.department_id")
    job_id = fields.Many2one(related="employee_id.job_id")
    notice_period = fields.Char()
    date = fields.Date('Date of Issuing the Termination Notice')
    end_date = fields.Date('Separation Date')
    reaon = fields.Text('Reason for Termination')
    comments = fields.Text('Comments')
    reciewer_id = fields.Many2one('res.users')
    gm_user = fields.Many2one('res.users')

    state = fields.Selection([
            ('draft', 'Draft'),
            ('review', 'Waiting Review'),
            ('waitin_app', 'Waiting Approve'),
            ('approved','Approved'),
            ('reject','Rejected'),
        ], string='Status',default="draft", index=True, tracking=True)
    def unlink(self):
        if self.state == 'approved':
            raise UserError('You cannot delete qpproved termination')
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
    def action_create_termination_letter(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        if not self.employee_id.emp_type :
            raise UserError('You have to select the type of employee first')
        if not self.end_date or not self.notice_period:
            raise UserError('You have to add notice Information First')
        lang = self.env.context.get('lang')
        
        mail_template = self.env.ref('warning_letter.email_template_termination', raise_if_not_found=False)

        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'hr.employee',
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
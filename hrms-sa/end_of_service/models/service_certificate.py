# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ServiceCertifiacte(models.Model):
    _name = 'service.certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'HR Service Certificate'
    _rec_name = 'employee_id'
    
    employee_id = fields.Many2one('hr.employee', string="Employee",required=True,tracking=True)
    department_id = fields.Many2one('hr.department', string="Department / Project",related="employee_id.department_id")
    date = fields.Date(tracking=True)
    capacity = fields.Char('Capacity in certificate form')
    user_id = fields.Many2one('res.users', string="User",default=lambda self: self.env.user)
    employee_user = fields.Many2one('res.users',related="employee_id.user_id")



    def action_email_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()

        lang = self.env.context.get('lang')
        mail_template = self.env.ref('end_of_service.email_template_service_certificate', raise_if_not_found=False)
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'service.certificate',
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
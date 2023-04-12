# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError




class Applicant(models.Model):
    _inherit = "hr.applicant"

    terms_id = fields.Many2one('hr.recruitment.terms')
    referance_name = fields.Char('Referance Name')
    referance_email = fields.Char('Referance Email')
    company_name = fields.Char('Referance Company')
    address = fields.Char('Referance Company Address')
    previous_job = fields.Char('Previous Job')

    def action_terms_and_conditions(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        terms = True
        if not self.terms_id:
        	raise UserError('You have to select terms and condition first.')
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template(terms)
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'force_email': True,
            # 'model_description': self.with_context(lang=lang).type_name,
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
    def action_referance_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        if not self.referance_name or not self.referance_email:
            raise UserError('You have to write the referance information')
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'hr.applicant',
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
    def _find_mail_template(self,terms = False):
        self.ensure_one()
        if terms == True:
            return self.env.ref('hr_recruitment_terms.email_template_terms', raise_if_not_found=False)
        else:
            return self.env.ref('hr_recruitment_terms.referance_form_template',raise_if_not_found=False)

# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api, _


class PolicyRequest(models.Model):
    _name = 'policy.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference Number", required=True,
                       readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    chapter_reference = fields.Char(string="Chapter reference", required=True)
    subject_reference = fields.Char(string="Subject reference", required=True)
    issue_with = fields.Selection([('policy', 'Policy'), ('procedure', 'Procedure')], string="Issue with",
                                  required=True)
    description = fields.Text(string="Description of the issue", required=True)
    suggested_solution = fields.Text(string="Suggested solution", required=True)
    rationale_for_hange = fields.Text(string="Rationale for Change", required=True)
    comments = fields.Text(string="Comments", required=True)
    min_salary = fields.Monetary(string="Minimum Salary", required=True)
    max_salary = fields.Monetary(string="Maximum Salary", required=True)
    attach_copy_of_budget_plan = fields.Binary(string="Attach a Copy Of Budget Plan")

    update_no = fields.Integer(string="Update No", required=True)
    update_date = fields.Date(string="Update Date", required=True)
    section_no = fields.Integer(string="Section No.", required=True)
    policy_procedure = fields.Selection([('added', 'Added'), ('amended', 'Amended'), ('deleted', 'Deleted')],
                                        string="Policy/Procedure ", required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'policy.request') or _('New')
        res = super(PolicyRequest, self).create(vals)
        return res


    reciewer_id = fields.Many2one('res.users',string="VP")
    reciewer_id2 = fields.Many2one('res.users',string="HRD")
    gm_user = fields.Many2one('res.users',string='GM')

    state = fields.Selection([
            ('draft', 'Draft'),
            ('review', 'Waiting Review'),
            ('waiting_review','Waiting Review'),
            ('waitin_app', 'Waiting Approve'),
            ('approved','Approved'),
            ('reject','Rejected'),
        ], string='Status',default="draft", index=True, tracking=True)
    def unlink(self):
        if self.state == 'approved':
            raise UserError('You cannot delete approved sheet')
        else:
            return super().unlink()
    def submit(self):
        self.state = 'review'
    def review(self):
        self.state = 'waiting_review'
        self.reciewer_id = self.env.user.id
    def waiting_review(self):
        self.state = 'waitin_app'
        self.reciewer_id2 = self.env.user.id
    def waitin_app(self):
        self.state = 'approved'
        self.gm_user = self.env.user.id
    def reject(self):
        self.state = 'reject'
    def set_draft(self):
        self.state = 'draft'
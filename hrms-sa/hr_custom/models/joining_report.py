# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class JoiningReport(models.Model):
    _name = 'joining.report'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _rec_name = 'employee_id'
    
    employee_id = fields.Many2one('hr.employee',required=True)
    employee_no = fields.Char('Employee Code')
    date = fields.Date('Date of Joining')
    state = fields.Selection(selection=[
        ('draft','Draft'),('line_manager','Line Manager Approval'),
        ('hr','HR Approval'),('approved','Approved')],default="draft")


    def action_draft(self):
        self.write({'state':'line_manager'})

    def action_line_manager(self):
        self.write({'state':'hr'})

    def action_hr(self):
        self.write({'state':'approved'})
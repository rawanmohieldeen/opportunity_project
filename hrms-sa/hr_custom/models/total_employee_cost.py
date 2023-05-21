# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class TotalEmployeeCost(models.Model):
    _name = 'total.employee.cost'
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
    employee_name = fields.Many2one('hr.employee',string="Employee Name",required=True)
    job_title = fields.Many2one('hr.job',string="Job Title",required=True)
    commencement_date = fields.Date(string="Commencement Date")

    visa_cost = fields.Monetary(string="Visa Cost",required=True)
    mobilisation_from = fields.Monetary(string="Mobilisation From",required=True)
    demobilisation_to = fields.Monetary(string="Demobilisation To",required=True)

    comments = fields.Text(string="Comments",required=True)



    lines_ids = fields.One2many('total.employee.cost.line','total_employee_cost_id')

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'total.employee.cost') or _('New')
       res = super(TotalEmployeeCost, self).create(vals)
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
            raise UserError('You cannot delete approved request')
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
class TotalEmployeeCostLine(models.Model):
    _name = 'total.employee.cost.line'
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)

    total_employee_cost_id = fields.Many2one('total.employee.cost')
    item  = fields.Selection([('base_salary ', 'Base Salary '), ('special_allowance', 'Special Allowance'), ('transportation_allowance', 'Transportation Allowance'), ('fuel_allowance', 'Fuel Allowance'), ('medical_insurance', 'Medical Insurance'), ('lmra', 'LMRA'), ('gosi', 'GOSI')],string="Item",required=True)

    monthly_cost = fields.Monetary(string="Monthly Cost",required=True)
    annual_cost = fields.Monetary(string="Annual Cost",required=True)
    total_tec = fields.Monetary(string="Total TEC",required=True)    
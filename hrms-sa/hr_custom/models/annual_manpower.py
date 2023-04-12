# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class AnnualDepartmentalManpowerPlanning(models.Model):
    _name = 'annual.departmental.manpower.planning'
    name = fields.Char(string="Reference Number", required=True,
                          readonly=True, default=lambda self: _('New'))
    department = fields.Many2one('hr.department',string="Department",required=True)
    date = fields.Date(string="Date")
    lines_ids = fields.One2many('annual.departmental.manpower.planning.line','plan_id')

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'annual.departmental.manpower.planning') or _('New')
       res = super(AnnualDepartmentalManpowerPlanning, self).create(vals)
       return res


class AnnualDepartmentalManpowerPlanningLine(models.Model):
    _name = 'annual.departmental.manpower.planning.line'
    plan_id = fields.Many2one('annual.departmental.manpower.planning')
    position_title = fields.Many2one('hr.job',string="Position Title",required=True)
    department = fields.Many2one('hr.department',string="Department",required=True)
    date = fields.Date(string="Date")
    promote = fields.Integer(string="Promote",required=True)
    transfer = fields.Integer(string="Transfer")
    replacement = fields.Integer(string="Replacement",required=True)
    additional = fields.Integer(string="Additional",required=True)
    retrench = fields.Integer(string="Retrench",required=True)
    total = fields.Integer(string="Total",compute="_compute_total")
    comments = fields.Char(string="Comments")


    api.depends('promote','transfer','replacement','additional','retrench')
    def _compute_total(self):
        for line in self:
            line.total= ((line.promote + line.transfer + line.replacement) + line.additional - line.retrench) 











class AnnualManpowerPlanning(models.Model):
    _name = 'annual.manpower.planning'
    name = fields.Char(string="Reference Number", required=True,
                          readonly=True, default=lambda self: _('New'))
    department = fields.Many2one('hr.department',string="Department",required=True)
    date = fields.Date(string="Date")
    lines_ids = fields.One2many('annual.manpower.planning.line','plan_id')

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'annual.manpower.planning') or _('New')
       res = super(AnnualManpowerPlanning, self).create(vals)
       return res


class AnnualManpowerPlanningLine(models.Model):
    _name = 'annual.manpower.planning.line'
    plan_id = fields.Many2one('annual.manpower.planning')
    position_title = fields.Many2one('hr.job',string="Position Title",required=True)
    department = fields.Many2one('hr.department',string="Department",required=True)
    date = fields.Date(string="Date")
    promote = fields.Integer(string="Promote",required=True)
    transfer = fields.Integer(string="Transfer")
    replacement = fields.Integer(string="Replacement",required=True)
    additional = fields.Integer(string="Additional",required=True)
    retrench = fields.Integer(string="Retrench",required=True)
    total = fields.Integer(string="Total",compute="_compute_total")
    comments = fields.Char(string="Comments")


    api.depends('promote','transfer','replacement','additional','retrench')
    def _compute_total(self):
        for line in self:
            line.total= ((line.promote + line.transfer + line.replacement) + line.additional - line.retrench) 











class PositionRequest(models.Model):
    _name = 'position.request'
    name = fields.Char(string="Reference Number", required=True,
                          readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    department = fields.Many2one('hr.department',string="Originating Department",required=True)
    date = fields.Date(string="Date")
    new_position = fields.Char(string="Name for New Position", required=True)
    reports_to = fields.Many2one('hr.job',string="Reports to", required=True)
    justification_for_new_position = fields.Text(string="Justification for New Position", required=True)
    proposed_grade = fields.Monetary(string="Proposed Grade", required=True)
    proposed_min_salary = fields.Monetary(string="Proposed Minimum Salary", required=True)
    proposed_max_salary = fields.Monetary(string="Proposed Maximum Salary", required=True)
    comments = fields.Text(string="Comments", required=True)
    broad_roles_responsibilities = fields.Text(string="Broad Roles & Responsibilities", required=True)
    attach_envisaged_job_escription = fields.Binary(string="Attach envisaged Job Description")
    
    update_no = fields.Integer(string="Update No", required=True)
    update_date = fields.Date(string="Update Date", required=True)
    section_no = fields.Integer(string="Section No.", required=True)
    policy_procedure  = fields.Selection([('added', 'Added'), ('amended', 'Amended'), ('deleted', 'Deleted')],string="Policy/Procedure ",required=True)

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'position.request') or _('New')
       res = super(PositionRequest, self).create(vals)
       return res



# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class PersonnelRequisition(models.Model):
    _name = 'personnel.requisition'
    name = fields.Char(string="Reference Number", required=True,
                          readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    company = fields.Many2one('res.partner',string="Comapny",required=True)
    position_title = fields.Many2one('hr.job',string="Position Title",required=True)
    date_of_request = fields.Date(string="Date of Request",required=True)
    department = fields.Many2one('hr.department',string="Department",required=True)
    position_location = fields.Many2one('res.country',string="Position Location",required=True)
    city = fields.Char(string="City",required=True)
    new_position = fields.Selection([('yes', 'Yes'), ('no', 'NO')],string="New Position",required=True)
    replacement_for = fields.Many2one('hr.employee',string="Replacement Fsor")
    position = fields.Selection([('permanent', 'Permanent'), ('temporary', 'Temporary'), ('part-time', 'Part-time')],string="Position",required=True)
    min_range = fields.Monetary(string="Minimum Salary")
    max_range = fields.Monetary(string="Maximum Salary")
    attach_copy_of_budget_plan = fields.Binary(string="attach a copy of budget plan")

    qualifications = fields.Char(string="Qualifications",required=True)
    experience = fields.Integer(string="Experience",required=True)
    language = fields.Many2many('res.lang',string="Language",required=True)
    job_description_experience_skills = fields.Binary(string="Job Description / Experience / Skills")
    comments = fields.Text(string="Comments")

    recruitment_agency = fields.Selection([('yes', 'Yes'), ('no', 'NO')],string="Recruitment Agency",required=True)
    agency_estimated_cost = fields.Monetary(string="Agency Estimated Cost") 
    attach_copy_of_estimated_cost = fields.Binary(string="attach copy of estimated cost")
    advertisement = fields.Many2one('hr.advertise',string="Advertisement")
    adv_estimated_cost = fields.Monetary(string="Adv Estimated Cost") 
    attach_copy_of_draft_advertisement_and_estimated_cost = fields.Binary(string="attach copy of draft advertisement and estimated cost")

    state = fields.Selection([('draft', 'New'), ('deputy_general_manager', 'Deputy General Manager'), ('hr_director_approval', 'HR Director Approval'),
         ('general_manager_approval', 'General Manager Approval'),('done', 'Done')],
        string='Status', readonly=True, copy=False, default='draft')
    
    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'personnel.requisition') or _('New')
       res = super(PersonnelRequisition, self).create(vals)
       return res


    def confirm(self):
        self.state = 'deputy_general_manager'


    def deputy_general_manager_confirm(self):
        self.state = 'hr_director_approval'


    def hr_director_approval_confirm(self):
        self.state = 'general_manager_approval'


    def general_manager_approval_confirm(self):
        self.state = 'done'




class PersonnelRequisitionNonExecutive(models.Model):
    _name = 'personnel.requisition.non.executive'
    name = fields.Char(string="Reference Number", required=True,
                          readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    company = fields.Many2one('res.partner',string="Comapny",required=True)
    position_title = fields.Many2one('hr.job',string="Position Title",required=True)
    date_of_request = fields.Date(string="Date of Request",required=True)
    department = fields.Many2one('hr.department',string="Department",required=True)
    position_location = fields.Many2one('res.country',string="Position Location",required=True)
    city = fields.Char(string="City",required=True)
    new_position = fields.Selection([('yes', 'Yes'), ('no', 'NO')],string="New Position",required=True)
    replacement_for = fields.Many2one('hr.employee',string="Replacement Fsor")
    position = fields.Selection([('permanent', 'Permanent'), ('temporary', 'Temporary'), ('part-time', 'Part-time')],string="Position",required=True)
    min_range = fields.Monetary(string="Minimum Salary")
    max_range = fields.Monetary(string="Mximum Salary")
    attach_copy_of_budget_plan = fields.Binary(string="attach a copy of budget plan")

    qualifications = fields.Char(string="Qualifications",required=True)
    experience = fields.Integer(string="Experience",required=True)
    language = fields.Many2many('res.lang',string="Language",required=True)
    job_description_experience_skills = fields.Binary(string="Job Description / Experience / Skills")
    comments = fields.Text(string="Comments")

    recruitment_agency = fields.Selection([('yes', 'Yes'), ('no', 'NO')],string="Recruitment Agency",required=True)
    agency_estimated_cost = fields.Monetary(string="Agency Estimated Cost") 
    attach_copy_of_estimated_cost = fields.Binary(string="attach copy of estimated cost")
    advertisement = fields.Many2one('hr.advertise',string="Advertisement")
    adv_estimated_cost = fields.Monetary(string="Adv Estimated Cost") 
    attach_copy_of_draft_advertisement_and_estimated_cost = fields.Binary(string="attach copy of draft advertisement and estimated cost")

    state = fields.Selection([('draft', 'New'), ('deputy_general_manager', 'Deputy General Manager'), ('hr_director_approval', 'HR Director Approval'),
         ('general_manager_approval', 'General Manager Approval'),('done', 'Done')],
        string='Status', readonly=True, copy=False, default='draft')

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'personnel.requisition.non.executive') or _('New')
       res = super(PersonnelRequisitionNonExecutive, self).create(vals)
       return res


    def confirm(self):
        self.state = 'deputy_general_manager'


    def deputy_general_manager_confirm(self):
        self.state = 'hr_director_approval'


    def hr_director_approval_confirm(self):
        self.state = 'general_manager_approval'


    def general_manager_approval_confirm(self):
        self.state = 'done'


class HrAdvertise(models.Model):
    _name = 'hr.advertise'
    names = fields.Char()
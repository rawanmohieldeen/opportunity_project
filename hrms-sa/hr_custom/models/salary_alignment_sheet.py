# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class SalaryAlignmentSheet(models.Model):
    _name = 'salary.alignment.sheet'
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
    candidate_name = fields.Many2one('hr.employee',string="Candidate Name",required=True)
    age = fields.Integer(string="Age")
    highest_qualification  = fields.Selection([
        ('bachelor_degree ', 'Bachelor Degree'), 
        ('master_degree', 'Master Degree'), 
        ('doctorate_degree', 'Doctorate Degree')],
        string="Highest Qualification",
        required=True)
    year_of_passing = fields.Integer(string="Year of Passing")
    current_designation = fields.Char(string="Current Designation")
    reporting_to = fields.Char(string="Reporting To")
    current_employer = fields.Char(string="Current Employer")
    total_experience = fields.Integer(string="Total Experience")
    proposed_position = fields.Many2one('hr.job',string="Proposed Position",required=True)
    proposed_grade = fields.Many2one('hr.grade',string="Proposed Grade")


    incumbent = fields.Many2one('hr.employee',string="Incumbent")
    grade = fields.Many2one('hr.grade',string="Grade")
    gross = fields.Monetary(string="Gross (PM)")
    gross_to_incumbent = fields.Float(string="Gross to Incumbent % Diff.")
    comments = fields.Char(string="Comments")
    comments1 = fields.Char(string="Comments")


    compensation_offer_details_lines_ids = fields.One2many('compensation.offer.details.line','compensation_offer_details_id')
    salary_line = fields.One2many('salary.details.line','salary_id')

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'salary.alignment.sheet') or _('New')
       res = super(SalaryAlignmentSheet, self).create(vals)
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
            return super().unlink(self)
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
    total_gross_salary = fields.Monetary(string="Total Gross Salary")

class CompensationOfferDetailsLine(models.Model):
    _name = 'compensation.offer.details.line'
    compensation_offer_details_id = fields.Many2one('salary.alignment.sheet')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    package = fields.Many2one('hr.salary.rule',string="Package")
    current = fields.Monetary(string="Current",required=True)
    expected  = fields.Monetary(string="Expected",required=True)
    proposed = fields.Monetary(string="Proposed",required=True)  
    proposed_to_current= fields.Float(string="Proposed to Current % Diff.",compute="_compute_total_diff")
    proposed_to_expected= fields.Float(string="Proposed to Expected % Diff.",compute="_compute_total_diff")
    expected_to_current= fields.Float(string="Expected to Current % Diff.",compute="_compute_total_diff")
    total_gross_salary = fields.Monetary(string="Total Gross Salary")


    api.depends('current','expected','proposed')
    def _compute_total_diff(self):
        for line in self:
            line.proposed_to_current = line.expected_to_current = line.proposed_to_expected = 0
            if  line.current != 0:
                line.proposed_to_current= ((line.proposed - line.current) / line.current) 
                line.expected_to_current= ((line.expected - line.current) / line.current) 
            if line.expected != 0:
                line.proposed_to_expected= ((line.proposed - line.expected) / line.expected) 


class slaryLines(models.Model):
    _name = 'salary.details.line'

    salary_id = fields.Many2one('salary.alignment.sheet')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)

    name = fields.Char(string="Comparable incumbent in KMC Saudi")
    grade = fields.Many2one('hr.grade',string="Grade")
    gross = fields.Monetary(string="Gross (pm)",required=True)
    different  = fields.Float(string="Diff %.",compute="_compute_total_diff")
    comments = fields.Text('Comments')


    api.depends('gross','salary_id.total_gross_salary')
    def _compute_total_diff(self):
        for line in self:
            line.different = 0
            if  line.gross != 0:
                line.different = ((line.salary_id.total_gross_salary - line.gross) / line.gross) 
            
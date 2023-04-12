# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class SalaryAlignmentSheet(models.Model):
    _name = 'salary.alignment.sheet'
    name = fields.Char(string="Reference Number", required=True,
                          readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    candidate_name = fields.Many2one('hr.applicant',string="Candidate Name",required=True)
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

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'salary.alignment.sheet') or _('New')
       res = super(SalaryAlignmentSheet, self).create(vals)
       return res




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
            line.proposed_to_current= ((line.proposed - line.current) / line.current) 
            line.proposed_to_expected= ((line.proposed - line.expected) / line.expected) 
            line.expected_to_current= ((line.expected - line.current) / line.current) 
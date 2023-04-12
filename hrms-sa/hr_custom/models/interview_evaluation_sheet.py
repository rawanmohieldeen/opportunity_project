# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class InterviewEvaluationSheet(models.Model):
    _name = 'interview.evaluation.sheet'
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
    date_of_interview = fields.Date(string="Date of Interview")
    position_applied_for = fields.Many2one('hr.job',string="Position Applied for",required=True)
    department = fields.Many2one('hr.department',string="Department",required=True)
    scoring_legend  = fields.Selection([
        ('excellent ', 'Excellent'), 
        ('good', 'Good'), 
        ('average', 'Average'), 
        ('below_average', 'Below Average'), 
        ('poor', 'Poor')],
        string="Scoring Legend",
        required=True)

    evaluation_lines_ids = fields.One2many('evaluation.line','evaluation_id')
    interviewees_limitations_lines_ids = fields.One2many('interviewees.limitations.line','interviewees_limitations_id')
    compensation_and_joining_details_lines_ids = fields.One2many('compensation.joining.details.line','compensation_and_joining_details_id')
    interviewees_strength_lines_ids = fields.One2many('interviewees.strength.line','interviewees_strength_id')

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'interview.evaluation.sheet') or _('New')
       res = super(InterviewEvaluationSheet, self).create(vals)
       return res


class EvaluationLine(models.Model):
    _name = 'evaluation.line'
    evaluation_id = fields.Many2one('interview.evaluation.sheet')
    attributes = fields.Many2one('evaluation.attributes')
    description  = fields.Char(string="Description",related='attributes.description')
    max_points  = fields.Integer(string="Max Points",related='attributes.points')
    score = fields.Integer(string="Score",required=True)  


class IntervieweesStrengthLine(models.Model):
    _name = 'interviewees.strength.line'
    interviewees_strength_id = fields.Many2one('interview.evaluation.sheet')
    strength  = fields.Char(string="Strength")  


class IntervieweesLimitationsLine(models.Model):
    _name = 'interviewees.limitations.line'
    interviewees_limitations_id = fields.Many2one('interview.evaluation.sheet')
    limitation  = fields.Char(string="Limitation")  


class CompensationJoiningDetailsLine(models.Model):
    _name = 'compensation.joining.details.line'
    compensation_and_joining_details_id = fields.Many2one('interview.evaluation.sheet')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    current_salary_currency = fields.Many2one('res.currency',string="Current Salary Currency")
    current_basic_salary = fields.Monetary(string="Current Basic Salary (Per Month)",required=True)
    current_other_allowances  = fields.Monetary(string="Current Other Allowances (Per Month) ",required=True)
    current_annual_incentives = fields.Monetary(string="Current Annual Incentives",required=True)  
    expected_joining_date = fields.Date(string="Expected Joining Date")
    employment_type = fields.Selection([('permanent', 'Permanent'), ('contract', 'Contract')],string="Employment Type",required=True)
    interview_outcome = fields.Selection([('select', 'Select'), ('shortlist', 'Shortlist'), ('hold', 'Hold'), ('reject', 'Reject')],string="Interview Outcome",required=True)


  


class EvaluationAttributes(models.Model):
    _name = 'evaluation.attributes'
    name  = fields.Char(string="Name")  
    description  = fields.Char(string="Description")
    points  = fields.Integer(string="points")
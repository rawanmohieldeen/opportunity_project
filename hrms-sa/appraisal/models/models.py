# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api, _


class LeaveApplicationForm(models.Model):
    _name = 'leave.application.form'
    name = fields.Char(string="Reference Number", required=True,
                       readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    employee_name = fields.Many2one('hr.employee', string="Employee Name", required=True)
    job_title = fields.Many2one('hr.job', string="Job Title", required=True)
    department = fields.Many2one('hr.department', string="Department", required=True)
    date_of_joining = fields.Date(string="Date of Joining")
    appraiser_name = fields.Many2one('hr.employee', string="Appraiser Name", required=True)
    appraiser_job_title = fields.Many2one('hr.job', string="Appraiser Job Title", required=True)

    overall_remarks_by_line_manage = fields.Text(string="Overall Remarks by Line Manage")
    recommendations_by_line_manage = fields.Text(string="Recommendations by Line Manage")

    appraisal_lines_ids = fields.One2many('appraisal.line', 'appraisal_id')

    # new addition for report form #
    review_period = fields.Date('Review Period')
    line_items_ids = fields.One2many('specific.obj.line', 'job_sp_id', string='Job Specific Objectives')
    line_items_a_ids = fields.One2many('job.obj.line', 'job_sa_id')
    action_line_ids = fields.One2many('course.action', 'co_line_id')
    comments = fields.Text('Comments')
    line_gen_ids = fields.One2many('generic.performance.line', 'gen_id')
    line_per_con_ids = fields.One2many('performance.counselling.line','perf_line_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('emp_submit', 'Employee Submit'), ('appraiser_appr', 'Appraiser Approval')], string='Status', default='draft')

    def action_draft(self):
        self.write({
            'state': 'draft'
        })

    def action_submit(self):
        self.write({
            'state': 'emp_submit'
        })

    def action_approval(self):
        self.write({
            'state': 'appraiser_appr'
        })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'leave.application.form') or _('New')
        res = super(LeaveApplicationForm, self).create(vals)
        return res


class EvaluationLine(models.Model):
    _name = 'appraisal.line'
    appraisal_id = fields.Many2one('leave.application.form')
    attributes = fields.Many2one('leave.application.form.attributes')
    description = fields.Char(string="Description", related='attributes.description')
    max_points = fields.Integer(string="Max", readonly=True, default=5)
    score = fields.Selection([
        ('1 ', '1'),
        ('2', '3'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')],
        string="Score",
        required=True)


class EvaluationAttributes(models.Model):
    _name = 'leave.application.form.attributes'
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")


class ProbationApplicationForm(models.Model):
    _name = 'probation.application.form'
    name = fields.Char(string="Reference Number", required=True,
                       readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    employee_name = fields.Many2one('hr.employee', string="Employee Name", required=True)
    job_title = fields.Many2one('hr.job', string="Job Title", required=True)
    department = fields.Many2one('hr.department', string="Department", required=True)
    date_of_joining = fields.Date(string="Date of Joining")
    appraiser_name = fields.Many2one('hr.employee', string="Appraiser Name", required=True)
    appraiser_job_title = fields.Many2one('hr.job', string="Appraiser Job Title", required=True)

    overall_remarks_by_line_manage = fields.Text(string="Overall Remarks by Line Manage")
    recommendations_by_line_manage = fields.Text(string="Recommendations by Line Manage")

    appraisal_lines_ids = fields.One2many('probation.appraisal.line', 'appraisal_id')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'probation.application.form') or _('New')
        res = super(ProbationApplicationForm, self).create(vals)
        return res


class ProbationEvaluationLine(models.Model):
    _name = 'probation.appraisal.line'
    appraisal_id = fields.Many2one('probation.application.form')
    attributes = fields.Many2one('probation.application.form.attributes')
    description = fields.Char(string="Description", related='attributes.description')
    max_points = fields.Integer(string="Max", readonly=True, default=5)
    score = fields.Selection([
        ('1 ', '1'),
        ('2', '3'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')],
        string="Score",
        required=True)


class ProbationEvaluationAttributes(models.Model):
    _name = 'probation.application.form.attributes'
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")


# part A
class JobSpecificA(models.Model):
    _name = 'job.obj.line'
    _description = 'Job Specific Objectives part A'
    # @api.depends('score_emp', 'score_appraiser')
    # def compute_avg_score(self):
    #     for record in self:
    #         # x = []
    #         if record.score_emp or record.score_appraiser:
    #             x = (record.score_emp + record.score_appraiser) / len(record.score_emp)
    #             record.avg_score_for = int(x)
    #         else:
    #             record.avg_score_for = 0

    # avg_score_for = fields.Integer(compute='compute_avg_score', string='Average Score')
    job_sa_id = fields.Many2one('leave.application.form')
    object_job = fields.Char('Objectives')
    jo_a_measure = fields.Char('Measure')
    jo_a_time = fields.Char('Timescale')
    jo_res = fields.Char('Results')
    score_emp = fields.Selection([('1', '1'), ('2', '2'),
                                  ('3', '3'), ('4', '4'), ('5', '5')
                                  ], string='Score by Employee')
    score_appraiser = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'), ('5', '5')

        ],
        string='Score by Appraiser')
    comments_a = fields.Text('Comments')


# part c
class JobSpecificOb(models.Model):
    _name = 'specific.obj.line'
    _description = 'Job Specific Objectives of Past 12 Months'

    job_sp_id = fields.Many2one('leave.application.form')
    object_job = fields.Char('Objectives')
    jo_measure = fields.Char('Measure')
    jo_s_time = fields.Char('Timescale')
    jo_tarin = fields.Char('Training Required')


# part-B
class GenericPerformanceLine(models.Model):
    _name = 'generic.performance.line'
    _description = 'Generic Performance Indicator'

    gen_id = fields.Many2one('leave.application.form')
    att_gen = fields.Char('Attributes')
    des_gen = fields.Char('Description')
    sco_emp_gen = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'),
         ('4', '4'), ('5', '5')
         ], string='Score by Employee'
    )
    sco_appr_gen = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'),
         ('4', '4'), ('5', '5')
         ], string='Score by Appraiser'
    )


class PerformanceCounselling(models.Model):
    _name = 'performance.counselling.line'
    # _rec_name = 'perf_line_id'

    perf_line_id = fields.Many2one('leave.application.form')
    objectives = fields.Char('Objectives')
    measure = fields.Char('Measure')
    timescale = fields.Char('Timescale')
    # results = fields.Char('Results')
    train_required = fields.Char('Training Required')


class CourseAction(models.Model):
    _name = 'course.action'

    co_line_id = fields.Many2one('leave.application.form')
    action = fields.Char('Action')

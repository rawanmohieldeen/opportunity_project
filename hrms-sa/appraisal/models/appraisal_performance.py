from odoo import models, fields, api, _


class AppraisalPerformance(models.Model):
    _name = 'appraisal.performance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    # update to remote

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, copy=False,
                                  track_visibility='onchange')
    deparment_id = fields.Many2one('hr.department', string='Deparment', required=True,
                                   related='employee_id.department_id', copy=False)
    job_id = fields.Many2one('hr.job', string='Job Title', related='employee_id.job_id')
    review_period = fields.Date('Review Date')
    join_date = fields.Date(string='Date of Join',related='employee_id.contract_id.date_start')
    appraiser_employee_id = fields.Many2one('hr.employee', string='Appraiser', required=True, copy=False,
                                            track_visibility='onchange')
    appraiser_job_id = fields.Many2one('hr.job', string='Appraiser Job Title', related='appraiser_employee_id.job_id',readonly=True)
    average_score_a = fields.Float('Average Score', compute='_compute_score_a', required=True, )
    average_score_b = fields.Float('Average Score', compute='_compute_score_b', required=True, )

    job_objective_past_ids = fields.One2many('job.objective.past', 'performance_id',
                                             string="Job Objective Past 12 Month IDs", )
    generic_indicators_ids = fields.One2many('generic.indicators', 'performance_id', string="Generic Indicators IDs", )
    job_objective_next_ids = fields.One2many('job.objective.next', 'performance_id',
                                             string="Job Objective Next 12 Month IDs", )
    appraisal_outcome_ids = fields.One2many('appraisal.outcome', 'performance_id', string="Appraisal Outcome IDs", )
    appraisal_recommendations_ids = fields.One2many('appraisal.recommendations', 'performance_id',
                                                    string="Appraisal Recommendations IDs", )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('line_approve', 'Line Manager Approve'),
        ('hr_approve', 'HR Manager Approve'),
        ('general_approve', 'General Manager Approve'),
    ], string='Status', default='draft')

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirm'

    def action_line_approve(self):
        self.state = 'line_approve'

    def action_hr_approve(self):
        self.state = 'hr_approve'

    def action_general_approve(self):
        self.state = 'general_approve'

    @api.depends('job_objective_past_ids')
    def _compute_score_a(self):
        total = 0
        average = 0.0
        count = 0
        for rec in self:
            for line in rec.job_objective_past_ids:
                total += int(line.employee_score) + int(line.appraiser_score)
                count += 2
            if count != 0:
                average = total / count
            rec.average_score_a = average

    @api.depends('generic_indicators_ids')
    def _compute_score_b(self):
        total = 0
        average = 0.0
        count = 0
        for rec in self:
            for line in rec.generic_indicators_ids:
                total += int(line.employee_score) + int(line.appraiser_score)
                count += 2
            if count != 0:
                average = total / count
            rec.average_score_b = average

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'appraisal.performance') or _('New')
        res = super(AppraisalPerformance, self).create(vals)
        return res


class JobObjectivePast(models.Model):
    _name = 'job.objective.past'

    objectives = fields.Char(string='Objectives', required=True)
    measure = fields.Char(string='Measure', required=True)
    timescale = fields.Char(string='Timescale', required=True)
    results = fields.Char(string='Results', required=True)
    employee_score = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string="Score by Employee", required=True, )
    appraiser_score = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string="Score by Appraiser", required=True, )

    performance_id = fields.Many2one('appraisal.performance', string='Performance', required=True)


class GenericIndicators(models.Model):
    _name = 'generic.indicators'

    attributes = fields.Char(string='Attributes', required=True)
    description = fields.Char(string='Description', required=True)
    employee_score = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string="Score by Employee", required=True, )
    appraiser_score = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string="Score by Appraiser", required=True, )

    performance_id = fields.Many2one('appraisal.performance', string='Performance', required=True)


class JobObjectiveNext(models.Model):
    _name = 'job.objective.next'

    objectives = fields.Char(string='Objectives', required=True)
    measure = fields.Char(string='Measure', required=True)
    timescale = fields.Char(string='Timescale', required=True)
    training_required = fields.Char(string='Training Required', required=True)
    performance_id = fields.Many2one('appraisal.performance', string='Performance', required=True)


class AppraisalOutcome(models.Model):
    _name = 'appraisal.outcome'

    indicators = fields.Char(string='Indicators', required=True)
    score = fields.Integer(string='Score', required=True)
    weight = fields.Float(string='Weight', required=True)
    weight_Score = fields.Float(string='Weighted Score', required=True)
    performance_id = fields.Many2one('appraisal.performance', string='Performance', required=True)


class AppraisalRecommendations(models.Model):
    _name = 'appraisal.recommendations'

    parameter = fields.Char(string='Parameter', required=True)
    recommendations = fields.Integer(string='Recommendations', required=True)
    performance_id = fields.Many2one('appraisal.performance', string='Performance', required=True)

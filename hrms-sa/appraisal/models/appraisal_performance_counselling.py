from odoo import models, fields, api , _

class AppraisalPerformanceCounselling(models.Model):
    _name = 'appraisal.performance.counselling'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    

    name = fields.Char(string="Reference",required=True, copy=False, readonly=True,default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee',string='Employee',required=True,copy=False,track_visibility='onchange')
    deparment_id = fields.Many2one('hr.department',string='Deparment',required=True,related='employee_id.department_id',copy=False)
    job_id = fields.Many2one('hr.job',string='Job Title',related='employee_id.job_id')
    review_period = fields.Date('Review Date')
    join_date = fields.Date(string='Date of Join',related='employee_id.contract_id.date_start')
    appraiser_employee_id = fields.Many2one('hr.employee',string='Appraiser',required=True,copy=False,track_visibility='onchange')
    appraiser_job_id = fields.Many2one('hr.job',string='Appraiser Job Title',readonly=True,related='appraiser_employee_id.job_id')
    
    performance_counselling_ids = fields.One2many('performance.counselling', 'performance_id',string="PerformanceCounselling IDs",)
    course_action_ids = fields.One2many('course.action', 'performance_id',string="Course of Action IDs",)
    
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('appraiser_approve', 'Appraiser Approve'),
            
        ], string='Status', default='draft')

    def action_draft(self):
        self.state='draft'
        
    def action_confirm(self):
        self.state='confirm'

    def action_appraiser_approve(self):
        self.state='appraiser_approve'


    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'appraisal.performance.counselling') or _('New')
       res = super(AppraisalPerformanceCounselling, self).create(vals)
       return res


class PerformanceCounselling(models.Model):
    _name = 'performance.counselling'

    objectives = fields.Char(string='Objectives',required=True)
    measure = fields.Char(string='Measure',required=True)
    timescale = fields.Char(string='Timescale',required=True)
    training_required = fields.Char(string='Training Required',required=True)
    performance_id = fields.Many2one('appraisal.performance.counselling',string='Performance Counselling',required=True)

class CourseAction(models.Model):
    _name = 'course.action'

    action = fields.Char(string='Action',required=True)
    performance_id = fields.Many2one('appraisal.performance.counselling',string='Performance Counselling',required=True)

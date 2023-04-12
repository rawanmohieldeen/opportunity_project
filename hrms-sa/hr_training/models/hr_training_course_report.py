from odoo import models, fields, api , _

class HrTrainingCourseReport(models.Model):
    _name = 'hr.training.course.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    

    name = fields.Char(string="Reference",required=True, copy=False, readonly=True,default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee',string='Employee',required=True,copy=False)
    deparment_id = fields.Many2one('hr.department',string='Deparment',required=True,related='employee_id.department_id',copy=False)
    job_id = fields.Many2one('hr.job',string='Designation',related='employee_id.job_id')
    line_ids = fields.One2many('hr.training.course.report.line', 'training_course_report_id',string="Line IDs",)
    q_object = fields.Selection([
        ('yes', 'YES'),
        ('no', 'No'),
        ('partly', 'Partly'),
       ], string="Do you think the course has achieved its object?",required=True,track_visibility='onchange')
    q_attend = fields.Char(string='Where you the right person to attend the course?',required=True,track_visibility='onchange')
    q_duties = fields.Selection([
        ('yes', 'YES'),
        ('no', 'No'),
       ], string="Will the course help in your duties (please elaborate)?",required=True,track_visibility='onchange')
    problems = fields.Text(string='Mention any problems faced at the training',track_visibility='onchange')
    course_time = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('weak', 'Weak'),
       ], string="Timing of the Course",required=True,track_visibility='onchange')
    course_duration = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('Average', 'Average'),
        ('weak', 'Weak'),
       ], string="Course Duration",required=True,track_visibility='onchange')
    course_place = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('Average', 'Average'),
        ('weak', 'Weak'),
       ], string="Course Place",required=True,track_visibility='onchange')
    training_method = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('Average', 'Average'),
        ('weak', 'Weak'),
       ], string="Training Method",required=True,track_visibility='onchange')
    remark = fields.Char(string='Remarks',required=True,track_visibility='onchange')
    recommend = fields.Selection([
        ('yes', 'YES'),
        ('no', 'No'),
       ], string="Would you recommend the course to other colleagues? ",required=True,track_visibility='onchange')
    other_comments = fields.Text(string='Other Comments',track_visibility='onchange')

   
    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'hr.training.course.report') or _('New')
       res = super(HrTrainingCourseReport, self).create(vals)
       return res


class HrTrainingCourseReportLine(models.Model):
    _name = 'hr.training.course.report.line'

    course_id = fields.Many2one('hr.training.course',string='Proposed Training',required=True,copy=False)
    relevance_to_duties = fields.Text(string='Relevance to Duties',track_visibility='onchange')
    place = fields.Char(string='Place',required=True,track_visibility='onchange')
    duration = fields.Integer(string='Duration',required=True,)
    duration_unit = fields.Selection([
        ('day', 'Day(s)'),
        ('month', 'Month(s)'),
       ], string="Duration Unit",required=True,)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    fees = fields.Monetary('Fees',required=True,currency_field='currency_id',)
    training_course_report_id = fields.Many2one('hr.training.course.report',string="Course Report",required=True,)

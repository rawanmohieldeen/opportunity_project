from odoo import models, fields, api

class HrTrainingCourse(models.Model):
    _name = 'hr.training.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'


    employee_id = fields.Many2one('hr.employee', string="Employee")
    user_id = fields.Many2one('res.users', string="User",default=lambda self: self.env.user)

    employee_no = fields.Char(related="employee_id.employee_no")
    job_id = fields.Many2one('hr.job',related="employee_id.job_id")
    department_id = fields.Many2one('hr.department', related="employee_id.department_id")
    course_line = fields.One2many('hr.training.course.line','course_id')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('waitin_app', 'Waiting HR Manager Approve'),
            ('approve','Approved'),
            ('reject','Rejected'),
        ], string='Status', default='draft')
    def submit(self):
        self.state = 'waitin_app'
    def waitin_app(self):
        self.state = 'approve'
    def reject(self):
        self.state = 'reject'
    def set_draft(self):
        self.state = 'draft'

class HrTrainingCourseLine(models.Model):
    _name = 'hr.training.course.line'
    _rec_name = 'course'

    course_id = fields.Many2one('hr.training.course')
    course = fields.Char(string='Training Course',required=True,track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', string="Employee",related="course_id.employee_id")
    place = fields.Char(string='Place',required=True,track_visibility='onchange')
<<<<<<< HEAD
    duration = fields.Integer(string='Duration',required=True,track_visibility='onchange')
    duration_unit = fields.Selection(selection=[('day', 'Days'),
                                        ('month','Months'),('year','Years')], default='day', track_visibility='onchange')
=======
    duration = fields.Char(string='Duration',required=True,track_visibility='onchange')
    duration_unit = fields.Selection([
        ('day', 'Day(s)'),
        ('month', 'Month(s)'),
       ], string="Duration Unit",required=True,track_visibility='onchange')
>>>>>>> bd76736a3eaf4c02202b61f19d1e7ec72835c511
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    fees = fields.Monetary('Fees',required=True,currency_field='currency_id',)
    comments = fields.Char(string='Comments',required=True,track_visibility='onchange')
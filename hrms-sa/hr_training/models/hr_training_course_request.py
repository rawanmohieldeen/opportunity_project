from odoo import models, fields, api , _

class HrTrainingCourseRequest(models.Model):
    _name = 'hr.training.course.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    

    name = fields.Char(string="Reference",required=True, copy=False, readonly=True,default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee',string='Employee',required=True,copy=False)
    deparment_id = fields.Many2one('hr.department',string='Deparment',required=True,related='employee_id.department_id',copy=False)
    job_id = fields.Many2one('hr.job',string='Designation',related='employee_id.job_id')
    request_for = fields.Selection([
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('course', 'Short / Professional Course'),
       ], string="Request For",required=True,track_visibility='onchange')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('line_approve', 'Line Manager Approve'),
            ('hr_approve', 'HR Manager Approve'),
            ('general_approve', 'General Manager Approve'),
        ], string='Status', default='draft')
    line_ids = fields.One2many('hr.training.course.request.line', 'training_course_request_id',string="Line IDs",)
    
    def action_draft(self):
        self.state='draft'
        
    def action_confirm(self):
        self.state='confirm'

    def action_line_approve(self):
        self.state='line_approve'

    def action_hr_approve(self):
        self.state='hr_approve'

    def action_general_approve(self):
        self.state='general_approve'


    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'hr.training.course.request') or _('New')
       res = super(HrTrainingCourseRequest, self).create(vals)
       return res


class HrTrainingCourserequestLine(models.Model):
    _name = 'hr.training.course.request.line'

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
    line_manager_comments = fields.Text(string='Line Manager Comments',track_visibility='onchange')
    training_course_request_id = fields.Many2one('hr.training.course.request',string="Course request",required=True,)

from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError

class HrTrainingPlan(models.Model):
    _name = 'hr.training.plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Reference",required=True, copy=False, readonly=True,default=lambda self: _('New'))
    from_date = fields.Date(string="From Date",required=True,track_visibility='onchange')
    to_date = fields.Date(string="To Date",required=True,track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    overall_budget = fields.Monetary('Overall Budget',compute='_compute_budget',required=True,currency_field='currency_id',)  
    state = fields.Selection([
            ('draft', 'Draft'),
            ('hr_approve', 'HR Manager Approve'),
            ('vp_approve', 'VP Approve'),
            ('general_approve', 'General Manager Approve'),
            ('approve', 'Approved'),
        ], string='Status', default='draft')
    line_ids = fields.One2many('hr.training.plan.line', 'training_plan_id',string="Line IDs",)
  
    def action_draft(self):
        self.state='draft'
        
    def action_confirm(self):
        for rec in self:
            if rec.overall_budget == 0.0 :
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>rrr",)
                    raise ValidationError(_("Overall Budget Must Be Not Zero!"))
            self.state='hr_approve'

    def action_confirm2(self):
        self.state='vp_approve'

    def action_hr_approve(self):
        self.state='general_approve'

    def action_general_approve(self):
        self.state='approve'

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'hr.training.plan') or _('New')
       res = super(HrTrainingPlan, self).create(vals)
       return res


    @api.depends('line_ids')
    def _compute_budget(self):
        total = 0
        for rec in self:
            for line in rec.line_ids:
                total += line.budget
            rec.overall_budget = total


class HrTrainingPlanLine(models.Model):
    _name = 'hr.training.plan.line'

    employee_id = fields.Many2one('hr.employee',string='Employee',required=True,copy=False)
    deparment_id = fields.Many2one('hr.department',string='Deparment',required=True,related='employee_id.department_id',copy=False)
    employee_no = fields.Char('Empl. ID',related='employee_id.employee_no')
    course_id = fields.Many2one('hr.training.course',string='Proposed Training',required=True,copy=False)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
       ], string="Priority",required=True,default='0')
    duration = fields.Integer(string='Duration',required=True,)
    duration_unit = fields.Selection([
        ('day', 'Day(s)'),
        ('month', 'Month(s)'),
       ], string="Duration Unit",required=True,)
    provider = fields.Char(string='Training Provider',required=True,)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    budget = fields.Monetary('Budget',required=True,currency_field='currency_id',)
    training_plan_id = fields.Many2one('hr.training.plan',string="Plans",required=True,track_visibility='onchange')

    @api.onchange('course_id')
    def _get_data(self):
        if self.course_id:
            self.duration = self.course_id.duration
            self.duration_unit = self.course_id.duration_unit
            self.provider = self.course_id.place
            self.budget = self.course_id.fees
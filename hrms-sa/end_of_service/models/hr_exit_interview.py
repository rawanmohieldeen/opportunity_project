from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError

class HrExitInterview(models.Model):
    _name = 'hr.exit.interview'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    employee = fields.Many2one('hr.employee', string='Employee', required=True, readonly=False, help="Employee",
                               default=lambda self: self.env.user.employee_id.id,
                               states={'draft': [('readonly', False)]})
    name = fields.Char(string="Reference",required=True, copy=False, readonly=True,default=lambda self: _('New'))
    # factor_id = fields.Many2one('hr.exit.factors',string="Factor",required=True,track_visibility='onchange')
    # critical_incidents_examples = fields.Char(string='Critical Incidents Examples',required=True,track_visibility='onchange')
    # points = fields.Integer(string="Points",required=True,track_visibility='onchange')
    # hr_comments = fields.Char(string='HR Comments',required=True,track_visibility='onchange')
    suggestions = fields.Text(string='I have the following suggestions to make the company a better place',track_visibility='onchange')
    other_comments = fields.Text(string='Other Comments',track_visibility='onchange')
    future_opportunity = fields.Text(string='If an opportunity ever arises, I will/will not consider joining the company again because',track_visibility='onchange')
    contact_address = fields.Text(string='Contact address for all further correspondence is Address',track_visibility='onchange')
    details = fields.Text(string='Details of any mentionable incident during the notice period of the person',track_visibility='onchange')
    character_certificate = fields.Text(string='Can a good character certificate be issued to the person?',track_visibility='onchange')
    employment_reconsideration = fields.Text(string='Can the person be rconsidered for re-employment?',track_visibility='onchange')
    hr_other_comments = fields.Text(string='Other Comments',track_visibility='onchange')
    positive_features_ids = fields.One2many('hr.positive.features', 'interview_id',string="Positive Features",)
    negative_features_ids = fields.One2many('hr.negative.features', 'interview_id',string="Negative Features",)

    fator_line = fields.One2many('hr.factor.line', 'interview_id',string="Factors Line",)


    @api.constrains("points")
    def _check_field(self):
        for rec in self:
            if rec.points > 100 or rec.points <1:
                raise ValidationError(_("Please Enter Correct Point Between 1 and 100"))
                
    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'hr.exit.interview') or _('New')
       res = super(HrExitInterview, self).create(vals)
       return res
class HRFactorsLine(models.Model):
    _name = 'hr.factor.line'

    interview_id = fields.Many2one('hr.exit.interview',string="Interview",required=True,track_visibility='onchange')
    factor_id = fields.Many2one('hr.exit.factors',string="Factor",required=True,track_visibility='onchange')
    critical_incidents_examples = fields.Char(string='Critical Incidents Examples',required=True,track_visibility='onchange')
    points = fields.Integer(string="Points",required=True,track_visibility='onchange')
    hr_comments = fields.Char(string='HR Comments',required=True,track_visibility='onchange')
class PositiveFeatures(models.Model):
    _name = 'hr.positive.features'

    name = fields.Char(string='Three major positive features of working with the company',required=True,)
    interview_id = fields.Many2one('hr.exit.interview',string="Interview",required=True,track_visibility='onchange')

class NegativeFeatures(models.Model):
    _name = 'hr.negative.features'

    name = fields.Char(string='Three major negative features of working with the company',required=True,)
    interview_id = fields.Many2one('hr.exit.interview',string="Interview",required=True,track_visibility='onchange')




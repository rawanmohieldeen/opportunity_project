# -*- coding: utf-8 -*-

import datetime

from odoo import models, fields, api, _


class OffencesPenalties(models.Model):
    _name = 'offence.penalty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Table of Offences and Penalty'
    _rec_name = 'type_action'

    type_action = fields.Char('Type of Action', required=True)
    initial_pro = fields.Char('Initial Procedure', required=True)
    f_time = fields.Char('First time', required=True)
    s_time = fields.Char('Second time', required=True)
    third_time = fields.Char('Third time', required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company,
                                 string="Company"
                                 )
    user_id = fields.Many2one('res.users', string='Responsible', ondelete='cascade', index=True,
                              help="If set, action binding only applies for this user.")
    offence_line_ids = fields.One2many('offence.line', 'offence_id')


class OffenceForm(models.Model):
    _name = 'hr.offence'
    _rec_name = 'emp_id'

    emp_id = fields.Many2one('hr.employee', string='Employee', required=True)
    designation = fields.Many2one(related='emp_id.job_id', string='Designation', required=True)
    dep_id = fields.Many2one(related='emp_id.department_id', string='Department', required=True)
    violating_emp = fields.Many2one('hr.employee', string='Violating employee', required=True)
    date_vio = fields.Date('Date of Violation', required=True)


class OffenceLine(models.Model):
    _name = 'offence.line'

    offence_id = fields.Many2one('offence.penalty')
    fu_de = fields.Text('Further details and explanation')
    reco_penalty = fields.Selection([
        ('ver', 'Verbal warning'),
        ('first', 'First'),
        ('second', 'Second'),
        ('w', 'Written warning'),
        ('termination', 'Termination')
    ], string='Recomanded penalty')

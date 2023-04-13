# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PromotionLetter(models.Model):
    _name = 'promotion.letter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'HR Promotion Letters'
    _rec_name = 'employee_id'
    
    employee_id = fields.Many2one('hr.employee', string="Employee",required=True,tracking=True)
    employee_no = fields.Char(related="employee_id.employee_no")
    designation = fields.Char()
    department_id = fields.Many2one('hr.department', string="Department / Project",related="employee_id.department_id")
    new_job_id = fields.Many2one('hr.job', string="Promoted To",required=True)
    promoted_date = fields.Date(tracking=True)
    details_ids = fields.One2many('promotion.details','promotion_id')



class PromotionDetails(models.Model):
    _name = 'promotion.details'

    particulars = fields.Char(required=True)
    amount = fields.Float(required=True)
    promotion_id = fields.Many2one('promotion.letter')
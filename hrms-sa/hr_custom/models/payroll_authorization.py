# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api,_


class PayrollAuthorization(models.Model):
    _name = 'payroll.authorization'
    name = fields.Char(string="Reference Number", required=True,
                          readonly=True, default=lambda self: _('New'))
    employee_name = fields.Many2one('hr.employee',string="Employee Name",required=True)
    employee_department = fields.Many2one('hr.department',string="Employee Department",required=True)
    employee_designation = fields.Many2one('hr.job',string="Employee Designation ",required=True)
    employee_grade  = fields.Many2one('hr.grade',string="Employee Grade")
    starting_date = fields.Date(string="Starting Date",required=True)


    department_first = fields.One2many('payroll.authorization.attributes','payroll_authorization', string="DepartmentFirst" )
    iban_number = fields.Integer(string="IBAN Number",required=True)

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'payroll.authorization') or _('New')
       res = super(PayrollAuthorization, self).create(vals)
       return res


class HrGrade(models.Model):
    _name = 'hr.grade'

    name = fields.Char(string="Employee Grade")


class PayrollAuthorizationAttributes(models.Model):
    _name = 'payroll.authorization.attributes'
    names = fields.Char()
    payroll_authorization = fields.Many2one('payroll.authorization')
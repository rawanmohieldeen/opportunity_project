# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.exceptions import UserError, Warning
from dateutil import relativedelta


class BusinessTravelRequest(models.Model):
    _name = 'business.travel.request'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee')  
    
    employee_no = fields.Char(related="employee_id.employee_no")
    department_id = fields.Many2one(related="employee_id.department_id")
    job_id = fields.Many2one(related="employee_id.job_id")
    trip = fields.Boolean('Business Trip')
    to_country = fields.Many2one('res.country', string='Destination Country', copy=False, tracking=True)
    to_state = fields.Many2one('res.country.state', string='Destination City', copy=False, tracking=True)
    training = fields.Boolean('Training')
    date = fields.Date('Departure Date')
    duration = fields.Integer('Duration of Travel')
    end_date = fields.Date('Return Date')
# travel
    travel_info = fields.Selection([
            ('own', 'OWN'),
            ('kmc', 'KMC To Arrange'),
            ('host', 'Host'),
          
        ], string='travel', index=True, tracking=True)
    

# Accommodation
    accommodation_info = fields.Selection([
            ('own', 'OWN'),
            ('kmc', 'KMC to Arrange'),
            ('host', 'Host'),
          
        ], string='Accommodation', index=True, tracking=True)
   
# Visa Requirement 

    visa = fields.Selection([
            ('required', 'Required'),
            ('not', 'Not Required'),
            ('exit', 'Exit Permit Required'),
          
        ], string='Visa Requirement', index=True, tracking=True)

    description = fields.Html('Travel Description')
    comments = fields.Html('Comments')
    
    travel_detail = fields.One2many('business.travel.request.details','travel_details')

# fields  To be completed by HRM (only if arranged by KMC):
    travel_line = fields.One2many('business.travel.request.line','travel_id')
# Travel Cost (In SR) fields

    airfare = fields.Float('Airfare')
    accommodation = fields.Float('Accommodation')
    others_fees = fields.Float('Others')
    total = fields.Float('Total',compute="compute_total")
    @api.depends('airfare','accommodation','others_fees')
    def compute_total(self):
        for travel in self:
        	travel.total = travel.airfare + travel.accommodation + travel.others_fees

    hr_comments = fields.Html('Comments')

    reciewer_id = fields.Many2one('res.users',string="HRM")
    reciewer_id2 = fields.Many2one('res.users',string="HRD")
    gm_user = fields.Many2one('res.users',string='VP')

    state = fields.Selection([
            ('draft', 'Draft'),
            ('review', 'Waiting Review'),
            ('waitin_app', 'Waiting Approve'),
            ('approved','Approved'),
            ('reject','Rejected'),
        ], string='Status',default="draft", index=True, tracking=True)
    def unlink(self):
        if self.state == 'approved':
            raise UserError('You cannot delete approved request')
        else:
            return super().unlink()
    def submit(self):
        self.state = 'review'
    def review(self):
        self.state = 'waiting_review'
        self.reciewer_id = self.env.user.id
    def waiting_review(self):
        self.state = 'waitin_app'
        self.reciewer_id2 = self.env.user.id
    def waitin_app(self):
        self.state = 'approved'
        self.gm_user = self.env.user.id
    def reject(self):
        self.state = 'reject'
    def set_draft(self):
        self.state = 'draft'
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'business.travel.request') or _('New')
        res = super(BusinessTravelRequest, self).create(vals)
        return res
class BusinessTravelRequestLinr(models.Model):
    _name = 'business.travel.request.line'

    travel_id = fields.Many2one('business.travel.request')
    serial = fields.Integer('#')
    hotel = fields.Text('Hotel Name')
    location = fields.Text('Location')
    room = fields.Char('Room Type')
    checkin_date = fields.Date('Check In')                                       
    checkout_date = fields.Date('Check Out')
    num_night = fields.Integer('No. Of Nights')
    time_check = fields.Char('Check Out Time')


class BusinessTravelRequestLinr3(models.Model):
    _name = 'business.travel.request.details'

    travel_details = fields.Many2one('business.travel.request')
    serial = fields.Integer('#')
    travel_class = fields.Text('Travel Class')
    destination = fields.Text('Destination')
    flight_time = fields.Char('Flight Time (AM/PM)')
    Departure = fields.Date('Departure')                                       
    arrival = fields.Date('Arrival')
# Expense Claim
class ExpenseClaim(models.Model):
    _name = 'expense.claim'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee')  
    
    employee_no = fields.Char(related="employee_id.employee_no")
    department_id = fields.Many2one(related="employee_id.department_id")
    job_id = fields.Many2one(related="employee_id.job_id")
    date = fields.Date('Date')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    days_num = fields.Integer(compute="compute_days")
    @api.depends('from_date','to_date')
    def compute_days(self):
        for claim in self:
            claim.days_num = relativedelta.relativedelta(claim.to_date, claim.from_date).days

    destination = fields.Char()
    expense_line = fields.One2many('expense.claim.line','expense_id')
    currency_id = fields.Many2one('res.currency')
    exchange_rate = fields.Many2one('res.currency.rate',domain="[('currency_id','=',currency_id)]")
    # rate = fields.Float(related="exchange_rate.rate")

    total_exp = fields.Float(compute="compute_total",readonly=True)
    advance = fields.Float()
    others_fees = fields.Float(compute="compute_total")
    ammount_return = fields.Float()  
    balance = fields.Float(compute="compute_total")


    @api.depends('advance','ammount_return')
    def compute_total(self):
        for travel in self:
            total = travel.total_exp = 0
            for line in travel.expense_line:
                total += line.sr1
            travel.total_exp = total
            travel.others_fees = travel.total_exp - travel.advance
            travel.balance = travel.total_exp - travel.advance + travel.ammount_return


    reciewer_id = fields.Many2one('res.users','HR Manager')
    reciewer_id2 = fields.Many2one('res.users','HR Director')
    gm_user = fields.Many2one('res.users','VP')

    state = fields.Selection([
            ('draft', 'Draft'),
            ('review', 'Waiting HR Manager Review'),
            ('waiting_review', 'Waiting HR Director Review'),
            ('waitin_app', 'Waiting VP Approve'),
            ('approved','Approved'),
            ('reject','Rejected'),
        ], string='Status',default="draft", index=True, tracking=True)
    def unlink(self):
        if self.state == 'approved':
            raise UserError('You cannot delete approved form')
        else:
            return super().unlink(self)
    def submit(self):
        self.state = 'review'
    def review(self):
        self.state = 'waiting_review'
        self.reciewer_id = self.env.user.id
    def waiting_review(self):
        self.state = 'waitin_app'
        self.reciewer_id2 = self.env.user.id
    def waitin_app(self):
        self.state = 'approved'
        self.gm_user = self.env.user.id
    def reject(self):
        self.state = 'reject'
    def set_draft(self):
        self.state = 'draft'
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'expense.claim') or _('New')
        res = super(ExpenseClaim, self).create(vals)
        return res
class ExpenseClaimLine(models.Model):
    _name = 'expense.claim.line'

    expense_id = fields.Many2one('expense.claim')
    name = fields.Char()
    sr1 = fields.Float()
    sr2 = fields.Float()
    sr3 = fields.Float()

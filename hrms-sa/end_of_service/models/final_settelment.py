from odoo import models, fields, api, _

class FinalSettlement(models.Model):
    _name = 'hr.final.settlement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',required=True,track_visibility='onchange',readonly=True)
    employee_id = fields.Many2one('hr.employee')
    contract = fields.Many2one('hr.contract',related="employee_id.contract_id")
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        string='Company Currency',
        related='company_id.currency_id', readonly=True,
    )
    effective_date = fields.Date()
    wage = fields.Monetary(related="contract.wage")
    annual_leave = fields.Monetary('Annual Leave Encashment')
    indemnity = fields.Monetary('Indemnity')
    payment_due = fields.Monetary('Total Payment due')
    start_date = fields.Date(related="contract.date_start")
    last_day =fields.Date('Last working day')
    leave_up = fields.Monetary('Indemnity/Annual Leave Encashment up to')
    annual_leave_ent = fields.Monetary('Annual Leave Entitlement')
    # salary package

    transportation = fields.Monetary('Transportation Allowance',related="contract.travel_allowance")
    house = fields.Monetary('Housing Allowance',related="contract.house")
    car = fields.Monetary('Car Allowance',related="contract.car")
    tickets = fields.Monetary('Tickets Allowance',related="contract.tickets")
    mobile = fields.Monetary('Mobile Phone  Allowance',related="contract.mobile")
    fuel = fields.Monetary('Fuel Allowance',related="contract.fuel")

    salry_up = fields.Monetary('Salary up to')
    total_salary  = fields.Monetary('Total Salary')
    pro_rate_balance = fields.Integer('Pro-rata balance up to')
    leave_inhancement = fields.Monetary('Leave Encashment for ')
    # calculation
    from_date = fields.Date('From')
    to_date = fields.Date('To')
    months = fields.Integer('Months')
    days = fields.Integer('Days')
    account_user = fields.Many2one('res.users')
    line_ids = fields.One2many('hr.final.settlement.line','settlement_id')
    total_indemnity = fields.Monetary(compute="compute_total")

    @api.depends('line_ids')
    def compute_total(self):
        for x in self:
            x.total_indemnity
            for line in x.line_ids:
                x.total_indemnity += line.balance
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
               'hr.final.settlement') or _('New')
        res = super(FinalSettlement, self).create(vals)
        return res
    state = fields.Selection([
            ('draft', 'Draft'),
            ('approved','Account Approved'),
        ], string='Status',default="draft", index=True, tracking=True)
    def unlink(self):
        if self.state == 'approved':
            raise UserError('You cannot delete approved request')
        else:
            return super().unlink(self)
    def action_approve(self):
        self.account_user = self.env.user.id
        self.state = 'approved'

class FinalSettlementLine(models.Model):
    _name = 'hr.final.settlement.line'

    settlement_id = fields.Many2one('hr.final.settlement')
    company_id = fields.Many2one(
        comodel_name='res.company',
        related="settlement_id.company_id")
    currency_id = fields.Many2one(
        string='Company Currency',
        related='settlement_id.currency_id', readonly=True,
    )
    from_num = fields.Integer('From')
    to_num = fields.Integer('To')
    balance = fields.Monetary()

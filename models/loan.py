# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta


class Loan(models.Model):
    _name = 'library.loan'
    _description = 'Library Loan'
    _order = 'loan_date desc'
    _rec_name = 'display_name'

    display_name = fields.Char(string='Loan', compute='_compute_display_name', store=True)

    # Relations
    book_id = fields.Many2one(
        'library.book',
        string='Book',
        required=True,
        ondelete='cascade',
        index=True
    )
    reader_id = fields.Many2one(
        'library.reader',
        string='Reader',
        required=True,
        ondelete='cascade',
        index=True
    )

    # Dates
    loan_date = fields.Date(
        string='Loan Date',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    return_date = fields.Date(
        string='Expected Return Date',
        required=True,
        tracking=True
    )
    actual_return_date = fields.Date(
        string='Actual Return Date',
        tracking=True
    )

    # State
    state = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    ], string='State', default='borrowed', required=True, tracking=True)

    # Computed fields
    days_overdue = fields.Integer(
        string='Days Overdue',
        compute='_compute_days_overdue',
        help='Number of days past the return date'
    )

    @api.depends('book_id', 'reader_id')
    def _compute_display_name(self):
        """Generate display name for loan"""
        for loan in self:
            if loan.book_id and loan.reader_id:
                loan.display_name = f"{loan.book_id.name} - {loan.reader_id.name}"
            else:
                loan.display_name = "New Loan"

    @api.depends('return_date', 'state', 'actual_return_date')
    def _compute_days_overdue(self):
        """Compute days overdue"""
        today = fields.Date.today()
        for loan in self:
            if loan.state == 'borrowed' and loan.return_date:
                if today > loan.return_date:
                    loan.days_overdue = (today - loan.return_date).days
                else:
                    loan.days_overdue = 0
            else:
                loan.days_overdue = 0

    @api.model
    def create(self, vals):
        """Override create to check availability and set return date"""
        book = self.env['library.book'].browse(vals.get('book_id'))
        
        # Check if book is available
        if book.state == 'unavailable' or book.available_copies <= 0:
            raise UserError(f'Book "{book.name}" is not available. Available copies: {book.available_copies}')
        
        # Set default return date (14 days from loan date)
        if not vals.get('return_date'):
            loan_date = vals.get('loan_date', fields.Date.today())
            if isinstance(loan_date, str):
                loan_date = fields.Date.from_string(loan_date)
            vals['return_date'] = loan_date + timedelta(days=14)

        loan = super(Loan, self).create(vals)
        
        # Update book state
        book._update_book_states()
        
        return loan

    def write(self, vals):
        """Override write to update book states"""
        result = super(Loan, self).write(vals)
        
        # Update book states if loan state changed
        if 'state' in vals:
            for loan in self:
                loan.book_id._update_book_states()
        
        return result

    def action_return_book(self):
        """Mark loan as returned"""
        for loan in self:
            if loan.state == 'returned':
                raise UserError('This loan is already returned.')
            
            loan.write({
                'state': 'returned',
                'actual_return_date': fields.Date.today()
            })
            
            # Update book state
            loan.book_id._update_book_states()

    def action_mark_overdue(self):
        """Manually mark loan as overdue"""
        for loan in self:
            if loan.state == 'borrowed':
                loan.write({'state': 'overdue'})

    @api.model
    def cron_check_overdue_loans(self):
        """Cron job to automatically mark overdue loans"""
        today = fields.Date.today()
        overdue_loans = self.search([
            ('state', '=', 'borrowed'),
            ('return_date', '<', today)
        ])
        overdue_loans.write({'state': 'overdue'})

    @api.constrains('loan_date', 'return_date')
    def _check_dates(self):
        """Validate loan dates"""
        for loan in self:
            if loan.return_date and loan.loan_date:
                if loan.return_date < loan.loan_date:
                    raise ValidationError('Return date cannot be before loan date.')

    @api.constrains('book_id')
    def _check_book_availability(self):
        """Check book availability when creating loan"""
        for loan in self:
            if loan.state == 'borrowed' and loan.book_id:
                if loan.book_id.available_copies <= 0:
                    raise ValidationError(
                        f'Book "{loan.book_id.name}" has no available copies.'
                    )


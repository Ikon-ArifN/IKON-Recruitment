from odoo import models, fields, api, _
from datetime import date, timedelta, datetime
import odoorpc
from odoo.exceptions import ValidationError


# Dev: hendra(07-10-2023)
# Class for inherit  Account Move
class AccountMove(models.Model):
    _inherit = 'account.move'
    sequence_prefix = 'BILL'

    def action_post(self):
        """
        Custom implementation of the 'action_post' method.
        This function posts the account move and performs additional actions.
        """
        print("oke")
        print(test)
        # config connection odoorpc
        odoo = odoorpc.ODOO("localhost", port=8069)
        odoo.login("distributor_db", "odoo", "odoo")

        # Get the sale order based on the invoice origin
        sale = self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)

        # Get the purchase orders based on the sale order ID
        purchase_order_model = odoo.env['purchase.order']
        result = purchase_order_model.search([('sale_order_id', '=', sale.id)])
        purchase_orders = purchase_order_model.browse(result)

        # Check if bill number already exists in the database
        current_date = date.today().strftime('%Y/%m')
        existing_bills = odoo.env['account.move'].search([
            ('name', 'like', f'{AccountMove.sequence_prefix}/{current_date}/%')
        ], order='sequence_number desc', limit=1)

        if existing_bills:
            # Get the last sequence number from existing bills
            last_sequence = int(existing_bills[0])
        else:
            last_sequence = 0

        # Generate the sequence number for the new bill
        sequence_number = str(last_sequence + 1).zfill(4)
        name = f"{AccountMove.sequence_prefix}/{current_date}/{sequence_number}"

        # Validate Invoice Date
        # if not self.invoice_date:
        #     raise ValidationError("Invoice date is required. Please provide the invoice date.")
        # else:
        #     self.invoice_date

        for move in self:
            # Prepare data for creating the new account move
            # print(self.env.context)
            move_data = {
                'name': name,
                'currency_id': move.currency_id.id,
                'state': 'draft',
                'auto_post': move.auto_post,
                'date': move.date.strftime('%Y-%m-%d'),
                'sequence_number': int(sequence_number),
                'payment_id': move.payment_id.id,
                'partner_id': move.partner_id.id,
                'commercial_partner_id': move.commercial_partner_id.id,
                'partner_shipping_id': move.partner_shipping_id.id,
                'sequence_prefix': AccountMove.sequence_prefix,
                'ref': purchase_orders.name,
                'move_type': 'in_invoice',
                'payment_state': 'not_paid',
                'invoice_partner_display_name': move.invoice_partner_display_name,
                'invoice_origin': purchase_orders.name,
                # 'invoice_date': True,
                'invoice_date_due': move.invoice_date_due.strftime('%Y-%m-%d'),
                'amount_untaxed': move.amount_untaxed,
                'amount_tax': move.amount_tax,
                'amount_total': move.amount_total,
                'amount_residual': move.amount_residual,
                'amount_untaxed_signed': move.amount_untaxed_signed,
                'amount_tax_signed': move.amount_tax_signed,
                'amount_total_signed': move.amount_total_signed,
                'amount_total_in_currency_signed': move.amount_total_in_currency_signed,
                'amount_residual_signed': move.amount_residual_signed,
                'posted_before': True,
                'id_register': self.ids[0],
            }
            # Create the new account move
            print("move_data",move_data)
            move_id = odoo.execute_kw('account.move', 'create', [move_data])
            odoo.execute_kw('account.move', 'write', [[move_id], move_data])
            account_move_line_model = odoo.env['account.move.line']

            # Search for account move lines in the existing account move
            account_move_line_models = self.env['account.move.line']
            account_lines = account_move_line_models.search([('move_id', '=', self.ids[0])])

            # Create move lines for each account move line
            for line in account_lines:
                for product in line.product_id:
                    # Prepare data for creating move lines
                    move_line_data = {
                        'move_id': move_id,
                        'product_id': product.id,
                        'journal_id': move.journal_id.id,
                        'company_id': line.company_id.id,
                        'company_currency_id': line.currency_id.id,
                        'partner_id': line.partner_id.id,
                        'quantity': line.quantity,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal,
                        'price_total': line.price_total,
                        'name': line.name,
                        'debit': line.debit,
                        'credit': line.credit,
                        'balance': line.balance,
                        'amount_currency': line.amount_currency,
                    }
                    print("move_line_data",move_line_data)
                    account_move_line_model.create(move_line_data)

        moves_with_payments = self.filtered('payment_id')
        other_moves = self - moves_with_payments

        # Perform action for records with payment IDs
        if moves_with_payments:
            moves_with_payments.payment_id.action_post()
        else:
            print("No records with payment IDs. Performing alternative action...")


        # Perform action for records without payment IDs
        if other_moves:
            other_moves._post(soft=False)
        else:
            print("No records without payment IDs. Performing alternative action...")

        return False

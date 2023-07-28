from odoo import models, fields, api, _
import datetime
import itertools
import logging
from collections import Counter
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FIELDS_RECURSION_LIMIT = 3

class PPUInvoice(models.Model):
    _name = 'ppu.invoice'
    _description = 'PPU Invoice'

    employee_id_number = fields.Char(string='Employee ID Number')
    employee_account_no = fields.Char(string='Employee – Account No. (1)')
    full_name = fields.Char(string='Full Name')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    department_code = fields.Char(string='Department – Code')
    department_description = fields.Char(string='Department – Description')
    position_code = fields.Char(string='Position – Code')
    position_description = fields.Char(string='Position – Description')
    date_of_hire = fields.Date(string='Date of hire', date_format='%d/%m/%Y')
    basic_salary = fields.Float(string='BASIC SALARY')
    uang_makan = fields.Float(string='UANG MAKAN')
    tunjangan_transport = fields.Float(string='TUNJANGAN TRANSPORT')
    tunjangan_1 = fields.Float(string='TUNJANGAN 1')
    tunjangan_2 = fields.Float(string='TUNJANGAN 2')
    insentif_1 = fields.Float(string='INSENTIF 1')
    insentif_2 = fields.Float(string='INSENTIF 2')
    outpatient = fields.Float(string='OUTPATIENT')
    lembur = fields.Float(string='LEMBUR')
    lembur_02 = fields.Float(string='LEMBUR_02')
    uang_saku = fields.Float(string='UANG SAKU')
    koordinator = fields.Float(string='KOORDINATOR')
    terminasi = fields.Float(string='TERMINASI')
    kompensasi = fields.Float(string='KOMPENSASI')
    penghasilan_lain = fields.Float(string='PENGHASILAN LAIN')
    tunjangan_pajak = fields.Float(string='TUNJANGAN PAJAK')
    bpjs_kesehatan_perusahaan_allowance = fields.Float(string='BPJS KESEHATAN PERUSAHAAN ALLOWANCE')
    bpjs_kesehatan_perusahaan_deduction = fields.Float(string='BPJS KESEHATAN PERUSAHAAN DEDUCTION')
    bpjs_kesehatan_karyawan_deduction = fields.Float(string='BPJS KESEHATAN KARYAWAN DEDUCTION')
    bpjstk_us = fields.Float(string='bpjstk_us')
    jht_2_by_employee_deduction = fields.Float(string='JHT 2% BY EMPLOYEE DEDUCTION')
    jaminan_pensiun_2_perusahaan_deduction = fields.Float(string='JAMINAN PENSIUN 2% PERUSAHAAN DEDUCTION')
    jaminan_pensiun_1_karyawan_deduction = fields.Float(string='JAMINAN PENSIUN 1% KARYAWAN DEDUCTION')
    dplk_us = fields.Float(string='DPLK_US')
    dplk_peg = fields.Float(string='DPLK_PEG')
    opct = fields.Float(string='OPCT')
    bonus = fields.Float(string='BONUS')
    thr = fields.Float(string='THR')
    thr_realisasi = fields.Float(string='THR Realisasi')
    pesangon = fields.Float(string='PESANGON')
    pkwt = fields.Float(string='PKWT')
    opsl_01 = fields.Float(string='OPSL_01')
    supervisi_01 = fields.Float(string='SPRVISI_01')
    seragam_01 = fields.Float(string='SERAGAM_01')
    diklat_01 = fields.Float(string='DIKLAT_01')
    rekrut_01 = fields.Float(string='REKRUT_01')
    ganti_01 = fields.Float(string='GANTI_01')
    lain_01 = fields.Float(string='LAIN_01')
    gross_salary = fields.Float(string='Gross Salary')
    opsl_02 = fields.Float(string='OPSL_02')
    supervisi_02 = fields.Float(string='SPRVISI_02')
    seragam_02 = fields.Float(string='SERAGAM_02')
    diklat_02 = fields.Float(string='DIKLAT_02')
    rekrut_02 = fields.Float(string='REKRUT_02')
    ganti_02 = fields.Float(string='GANTI_02')
    lain_02 = fields.Float(string='LAIN_02')
    net_salary = fields.Float(string='Net Salary')
    opsl_03 = fields.Float(string='OPSL_03')
    supervisi_03 = fields.Float(string='SPRVISI_03')
    seragam_03 = fields.Float(string='SERAGAM_03')
    diklat_03 = fields.Float(string='DIKLAT_03')
    rekrut_03 = fields.Float(string='REKRUT_03')
    ganti_03 = fields.Float(string='GANTI_03')
    lain_03 = fields.Float(string='LAIN_03')
    tax = fields.Float(string='Tax')
    tax_irreguler = fields.Float(string='Tax Irregular')
    potongan_iuran = fields.Float(string='POTONGAN IURAN')
    potongan_pinjaman = fields.Float(string='POTONGAN PINJAMAN')
    potongan_klaim = fields.Float(string='POTONGAN KLAIM')
    potongan_transfer = fields.Float(string='POTONGAN TRANSFER')
    potongan_lain_lain = fields.Float(string='POTONGAN LAIN-LAIN')
    potongan_koperasi = fields.Float(string='Potongan Koperasi')
    total_deduction = fields.Float(string='Total Deduction')
    take_home_pay = fields.Float(string='Take Home Pay')
    peng_bruto = fields.Float(string='Peng. Bruto')
    fee = fields.Float(string='Fee')
    klaim = fields.Float(string='Klaim')
    ppn = fields.Float(string='Ppn')
    total = fields.Float(string='Total')
    pph23 = fields.Float(string='Pph23')
    jasa = fields.Char(string='JASA')
    jasa_total = fields.Integer(string='JASA Total', compute='compute_jasa_totals')

    @api.model
    def compute_jasa_totals(self):
        # Get all 'jasa' values from the records
        jasa_values = self.env['ppu.invoice'].search_read([], ['jasa'])
        # Use Counter to count occurrences of each 'jasa' value
        jasa_counts = Counter(item['jasa'] for item in jasa_values)
        return jasa_counts


    def action_open_invoice_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'PPU Invoice',
            'res_model': 'ppu.invoice',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    # Action to generate the invoice report
    def action_generate_invoice_report(self):
        report_name = 'your_module_name.report_ppu_invoice_custom'  # Replace with your actual report's XML ID
        return self.env.ref(report_name).report_action(self)

    def action_GetJasa(self):
        jasa_totals = self.env['ppu.invoice'].compute_jasa_totals()
        logger.info(jasa_totals)



class ImportValidationError(Exception):
    """
    This class is made to correctly format all the different error types that
    can occur during the pre-validation of the import that is made before
    calling the data loading itself. The Error data structure is meant to copy
    the one of the errors raised during the data loading. It simplifies the
    error management at client side as all errors can be treated the same way.

    This exception is typically raised when there is an error during data
    parsing (image, int, dates, etc..) or if the user did not select at least
    one field to map with a column.
    """
    def __init__(self, message, **kwargs):
        super().__init__(message)
        self.type = kwargs.get('error_type', 'error')
        self.message = message
        self.record = False
        self.not_matching_error = True
        self.field_path = [kwargs['field']] if kwargs.get('field') else False
        self.field_type = kwargs.get('field_type')


class Import(models.TransientModel):
    _inherit = 'base_import.import'
    _description = 'Base Import'



    # def _parse_date_from_data(self, data, index, name, field_type, options):
    #     options['date_format'] = '%d/%m/%Y'
    #     dt = datetime.datetime
    #     fmt = fields.Date.to_string if field_type == 'date' else fields.Datetime.to_string
    #     d_fmt = options.get('date_format')
    #     # test = options['date_format']
    #     # d_fmt = datetime.strptime(date_fmt, "%d/%m/%Y")

    #     dt_fmt = options.get('datetime_format')
    #     for num, line in enumerate(data):
    #         if not line[index]:
    #             continue

    #         v = line[index].strip()
    #         try:
    #             # first try parsing as a datetime if it's one
    #             if dt_fmt and field_type == 'datetime':
    #                 try:
    #                     line[index] = fmt(dt.strptime(v, dt_fmt))
    #                     continue
    #                 except ValueError:
    #                     pass
    #             # otherwise try parsing as a date whether it's a date
    #             # or datetime
    #             line[index] = fmt(dt.strptime(v, d_fmt))
    #         except ValueError as e:
    #             raise ImportValidationError(
    #                 _("Column %s contains incorrect values. Error in line %d: %s") % (name, num + 1, e),
    #                 field=name, field_type=field_type
    #             )
    #         except Exception as e:
    #             raise ImportValidationError(
    #                 _("Error Parsing Date [%s:L%d]: %s") % (name, num + 1, e),
    #                 field=name, field_type=field_type
    #             )








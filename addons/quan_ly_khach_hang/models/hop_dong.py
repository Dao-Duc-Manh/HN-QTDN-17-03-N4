from odoo import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class HopDong(models.Model):
    _name = 'hop_dong'
    _description = 'Bảng chứa thông tin hợp đồng'
    _rec_name = "so_hop_dong"

    so_hop_dong = fields.Char("Số hợp đồng", store=True, readonly=True)
    ten_hop_dong = fields.Char("Tên hợp đồng", required=True)
    mo_ta = fields.Text("Mô tả hợp đồng", required=True)
    ngay_ky = fields.Date("Ngày ký", required=True)
    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc", required=True)
    gia_tri_hop_dong = fields.Monetary("Giá trị hợp đồng", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', 
                                   default=lambda self: self.env.company.currency_id)
    
    tinh_trang = fields.Selection([
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
        ('tam_dung', 'Tạm dừng'),
    ], string='Tình trạng', default='dang_thuc_hien')

    trang_thai = fields.Many2one('trang_thai_hop_dong', string='Trạng thái', 
                                  compute="_compute_trang_thai", store=True, readonly=True)
    
    id_khach_hang = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    nguoi_quan_ly = fields.Many2one('res.users', string="Người quản lý", required=True,
                                     default=lambda self: self.env.user)
    tep_dinh_kem = fields.Binary("Tệp đính kèm")
    ten_tep = fields.Char("Tên tệp")
    
    # Văn bản liên quan - lấy từ khách hàng
    van_ban_lien_ket = fields.Char(
        string="Văn bản liên quan",
        compute="_compute_van_ban_lien_ket",
        store=False
    )
    
    @api.depends('id_khach_hang')
    def _compute_van_ban_lien_ket(self):
        for record in self:
            if record.id_khach_hang:
                van_ban_di = self.env['van_ban_di'].search([('id_khach_hang', '=', record.id_khach_hang.id)])
                van_ban_den = self.env['van_ban_den'].search([('id_khach_hang', '=', record.id_khach_hang.id)])
                total = len(van_ban_di) + len(van_ban_den)
                record.van_ban_lien_ket = f"VB đi: {len(van_ban_di)}, VB đến: {len(van_ban_den)}" if total > 0 else "Không có"
            else:
                record.van_ban_lien_ket = ""

    @api.model
    def create(self, vals):
        count = self.env['hop_dong'].search_count([]) + 1
        if 'ngay_ky' in vals:
            ngay_ky = fields.Date.from_string(vals['ngay_ky'])
            vals['so_hop_dong'] = f"HD{count:05d}_{ngay_ky.strftime('%Y%m%d')}"
        else:
            vals['so_hop_dong'] = f"HD{count:05d}"
        return super(HopDong, self).create(vals)

    @api.depends('ngay_ket_thuc', 'ngay_bat_dau', 'tinh_trang')
    def _compute_trang_thai(self):
        _logger.info("### COMPUTE TRẠNG THÁI HỢP ĐỒNG ĐƯỢC GỌI ###")

        # Truy vấn một lần cho hiệu suất tốt hơn
        trang_thai_dict = {tt['ten_trang_thai']: tt['id'] for tt in self.env['trang_thai_hop_dong'].search_read(
            [('ten_trang_thai', 'in', ['Hoàn thành', 'Đang thực hiện', 'Sắp hết hạn', 'Quá hạn', 'Hủy', 'Tạm dừng'])], 
            ['ten_trang_thai', 'id']
        )}

        today = date.today()

        for record in self:
            _logger.info(f"Đang tính trạng thái cho hợp đồng ID: {record.id}")

            if record.tinh_trang == 'huy':
                record.trang_thai = trang_thai_dict.get('Hủy', False)
            elif record.tinh_trang == 'tam_dung':
                record.trang_thai = trang_thai_dict.get('Tạm dừng', False)
            elif record.tinh_trang == 'hoan_thanh':
                record.trang_thai = trang_thai_dict.get('Hoàn thành', False)
            elif record.tinh_trang == 'dang_thuc_hien':
                if record.ngay_ket_thuc:
                    days_remaining = (record.ngay_ket_thuc - today).days
                    if days_remaining < 0:
                        record.trang_thai = trang_thai_dict.get('Quá hạn', False)
                    elif days_remaining <= 30:
                        record.trang_thai = trang_thai_dict.get('Sắp hết hạn', False)
                    else:
                        record.trang_thai = trang_thai_dict.get('Đang thực hiện', False)
                else:
                    record.trang_thai = trang_thai_dict.get('Đang thực hiện', False)
            else:
                record.trang_thai = False


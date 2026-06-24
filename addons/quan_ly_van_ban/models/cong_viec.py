from odoo import models, fields, api
from datetime import date, timedelta
import logging
_logger = logging.getLogger(__name__)


class CongViec(models.Model):

    _name = 'cong.viec'
    _description = 'Bảng chứa thông tin công việc'
    _rec_name = "ten_cong_viec"

    ten_cong_viec = fields.Char("Tên công việc", required=True)
    yeu_cau = fields.Text("Yêu cầu xử lý", required=True)
    ngay_tao = fields.Date("Ngày tạo", required=True)
    han_xu_ly = fields.Date("Hạn xử lý", required=True)
    ngay_hoan_thanh = fields.Date("Ngày hoàn thành")
    
    tinh_trang = fields.Selection([
        ('da_nhan', 'Đã nhận'),
        ('huy', 'Huỷ'),
    ], string='Tình trạng')

    trang_thai = fields.Many2one('trang_thai', string='Trạng thái', compute="_compute_trang_thai", store=True , readonly = True)
    
    chi_dao = fields.Many2one('nhan_vien', string="Chỉ đạo", required=True)
    chu_tri_giai_quyet = fields.Many2one('nhan_vien', string="Chủ trì giải quyết")
    van_ban_den_id = fields.Many2one('van_ban_den', string="Văn bản xử lý")

    khach_hang_id = fields.Many2one('khach_hang', string='Khách hàng liên quan')
    van_ban_di_id = fields.Many2one('van_ban_di', string='Văn bản đi liên quan')


    @api.depends('ngay_hoan_thanh', 'han_xu_ly', 'tinh_trang', 'ngay_tao')
    def _compute_trang_thai(self):
        _logger.info("### COMPUTE TRẠNG THÁI ĐƯỢC GỌI ###")

        # Truy vấn một lần cho hiệu suất tốt hơn
        trang_thai_dict = {tt['ten_trang_thai']: tt['id'] for tt in self.env['trang_thai'].search_read(
            [('ten_trang_thai', 'in', ['Hoàn thành', 'Hoàn thành quá hạn', 'Huỷ', 'Đã nhận', 'Đang xử lý'])], ['ten_trang_thai', 'id']
        )}

        today = date.today()  # Lấy ngày hiện tại chỉ một lần

        for record in self:
            _logger.info(f"Đang tính trạng thái cho công việc ID: {record.id}")

            # Nếu đã hoàn thành
            if record.ngay_hoan_thanh:
                if record.han_xu_ly and record.ngay_hoan_thanh > record.han_xu_ly:
                    record.trang_thai = trang_thai_dict.get('Hoàn thành quá hạn', False)
                else:
                    record.trang_thai = trang_thai_dict.get('Hoàn thành', False)
            # Nếu bị hủy
            elif record.tinh_trang == 'huy':
                record.trang_thai = trang_thai_dict.get('Huỷ', False)
            # Nếu đã nhận hoặc chưa có tình trạng
            else:
                # Mặc định là đã nhận nếu chưa có tình trạng
                if not record.tinh_trang or record.tinh_trang == 'da_nhan':
                    if record.han_xu_ly:
                        # Nếu hạn xử lý đã qua (quá hạn) nhưng chưa hoàn thành
                        if today > record.han_xu_ly:
                            # Vẫn hiển thị "Đã nhận" nếu chưa có trạng thái "Quá hạn"
                            record.trang_thai = trang_thai_dict.get('Đã nhận', False)
                        # Nếu hạn xử lý chưa đến hoặc trong hôm nay
                        else:
                            record.trang_thai = trang_thai_dict.get('Đang xử lý', False)
                    else:
                        record.trang_thai = trang_thai_dict.get('Đã nhận', False)
                else:
                    record.trang_thai = trang_thai_dict.get('Đã nhận', False)
    
    @api.model
    def create(self, vals):
        """Override create để tự động set tình trạng và tính toán trạng thái"""
        # Nếu chưa có tình trạng, mặc định là 'da_nhan'
        if 'tinh_trang' not in vals or not vals.get('tinh_trang'):
            vals['tinh_trang'] = 'da_nhan'
        
        # Nếu chưa có ngày tạo, set là ngày hiện tại
        if 'ngay_tao' not in vals or not vals.get('ngay_tao'):
            vals['ngay_tao'] = fields.Date.today()
        
        record = super(CongViec, self).create(vals)
        # Tính toán trạng thái sau khi tạo
        record._compute_trang_thai()
        return record
    
    def write(self, vals):
        """Override write để tự động tính toán lại trạng thái khi có thay đổi"""
        result = super(CongViec, self).write(vals)
        # Tính toán lại trạng thái nếu có thay đổi các field liên quan
        if any(field in vals for field in ['ngay_hoan_thanh', 'han_xu_ly', 'tinh_trang']):
            self._compute_trang_thai()
        return result

    @api.model
    def action_nhac_cong_viec_sap_han(self):
        """Cron job: Gửi thông báo vào kênh Discuss khi công việc còn ≤ 3 ngày đến hạn"""
        today = date.today()
        ngay_canh_bao = today + timedelta(days=3)

        # Tìm công việc sắp đến hạn, chưa hoàn thành, chưa hủy
        cong_viec_sap_han = self.search([
            ('han_xu_ly', '>=', fields.Date.to_string(today)),
            ('han_xu_ly', '<=', fields.Date.to_string(ngay_canh_bao)),
            ('ngay_hoan_thanh', '=', False),
            ('tinh_trang', '!=', 'huy'),
            ('trang_thai', '=', self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đang xử lý')], limit=1).id),

        ])

        if not cong_viec_sap_han:
            _logger.info("Không có công việc nào sắp đến hạn.")
            return

        # Tìm hoặc tạo kênh "Nhắc việc"
        Channel = self.env['mail.channel']
        kenh = Channel.search([('name', '=', 'Nhắc việc')], limit=1)
        if not kenh:
            kenh = Channel.create({
                'name': 'Nhắc việc',
                'channel_type': 'channel',
                'description': 'Kênh thông báo tự động – công việc sắp đến hạn',
            })
            _logger.info("Đã tạo kênh 'Nhắc việc' mới.")

        # Gửi từng thông báo vào kênh
        for cv in cong_viec_sap_han:
            so_ngay_con_lai = (cv.han_xu_ly - today).days
            ten_chu_tri = cv.chu_tri_giai_quyet.ho_ten if cv.chu_tri_giai_quyet else 'Chưa phân công'
            ten_chi_dao = cv.chi_dao.ho_ten if cv.chi_dao else 'Không có'

            noi_dung = (
                "⚠️ NHẮC VIỆC SẮP ĐẾN HẠN\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 Công việc : {cv.ten_cong_viec}\n"
                f"👤 Chủ trì   : {ten_chu_tri}\n"
                f"👔 Chỉ đạo   : {ten_chi_dao}\n"
                f"📅 Hạn xử lý : {cv.han_xu_ly}\n"
                f"⏳ Còn lại   : {so_ngay_con_lai} ngày\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            )

            kenh.message_post(
                body=noi_dung,
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
            )
            _logger.info(f"Đã gửi nhắc việc: {cv.ten_cong_viec}")

        _logger.info(f"Hoàn tất: Đã gửi {len(cong_viec_sap_han)} thông báo vào kênh 'Nhắc việc'.")


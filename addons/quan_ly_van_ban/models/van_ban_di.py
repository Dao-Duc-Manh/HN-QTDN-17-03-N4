from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa thông tin van_ban_di'
    _rec_name = "tieu_de"

    ngay_di             = fields.Date("Ngày đi", required=True)
    so_hieu             = fields.Char("Số hiệu", store=True, readonly=True)
    trich_yeu           = fields.Text("Trích yếu", required=True)
    tieu_de             = fields.Char("Tiêu đề", required=True)
    tep_dinh_kem        = fields.Binary("Tệp đính kèm")
    ho_so               = fields.Many2one('ho_so', string='Hồ sơ')
    id_loai_van_ban     = fields.Many2one('loai_van_ban', string='Loại văn bản')
    id_co_quan_ban_hanh = fields.Many2one('phong_ban', string='Cơ quan ban hành')
    id_nguoi_phat_hanh  = fields.Many2one('nhan_vien', string='Người ký')
    dia_chi_nhan        = fields.Text("Nơi nhận", required=True)
    id_do_mat           = fields.Many2one('do_mat', string='Độ mật')
    id_nam              = fields.Many2one('nam', string='Năm')
    id_khach_hang       = fields.Many2one('khach_hang', string='Khách hàng liên quan')

    state = fields.Selection([
        ('draft',     'Dự thảo'),
        ('pending',   'Trình ký'),
        ('signed',    'Đã ký'),
        ('issued',    'Ban hành'),
        ('cancelled', 'Hủy'),
    ], string='Trạng thái', default='draft')

    def action_trinh_ky(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(_('Chỉ có thể trình ký từ trạng thái Dự thảo.'))
            record.state = 'pending'

    def action_ky(self):
        for record in self:
            if record.state != 'pending':
                raise ValidationError(_('Chỉ có thể ký từ trạng thái Trình ký.'))
            record.state = 'signed'

    def action_ban_hanh(self):
        for record in self:
            if record.state != 'signed':
                raise ValidationError(_('Chỉ có thể ban hành từ trạng thái Đã ký.'))
            record.state = 'issued'

            # Tự động tạo công việc
            self.env['cong.viec'].create({
                'ten_cong_viec' : f"Xử lý văn bản: {record.tieu_de}",
                'yeu_cau'       : (
                    f"Văn bản số {record.so_hieu} đã được ban hành.\n"
                    f"Trích yếu: {record.trich_yeu}"
                ),
                'ngay_tao'      : fields.Date.today(),
                'han_xu_ly'     : fields.Date.today() + timedelta(days=7),
                'tinh_trang'    : 'da_nhan',
                'chi_dao'       : record.id_nguoi_phat_hanh.id if record.id_nguoi_phat_hanh else False,
                'van_ban_den_id': False,
                'khach_hang_id' : record.id_khach_hang.id if record.id_khach_hang else False,
                'van_ban_di_id' : record.id,
            })

            # Chuẩn bị nội dung thông báo
            ten_nguoi_ky   = record.id_nguoi_phat_hanh.ho_ten if record.id_nguoi_phat_hanh else 'Không rõ'
            ten_co_quan    = record.id_co_quan_ban_hanh.display_name if record.id_co_quan_ban_hanh else 'Không rõ'
            ten_khach_hang = record.id_khach_hang.ten_khach_hang if record.id_khach_hang else 'Không có'

            noi_dung = (
                f"🔔 VĂN BẢN MỚI ĐƯỢC BAN HÀNH\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 Tiêu đề      : {record.tieu_de}\n"
                f"🔢 Số hiệu      : {record.so_hieu or 'Chưa có'}\n"
                f"📝 Trích yếu    : {record.trich_yeu}\n"
                f"✍️  Người ký     : {ten_nguoi_ky}\n"
                f"🏢 Cơ quan      : {ten_co_quan}\n"
                f"👤 Khách hàng   : {ten_khach_hang}\n"
                f"📅 Ngày ban hành: {record.ngay_di}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )

            # Gửi vào kênh General có sẵn của Odoo
            kenh = self.env['mail.channel'].search(
                [('name', 'ilike', 'general')], limit=1
            )
            if not kenh:
                kenh = self.env['mail.channel'].search(
                    [('name', '=', 'Văn bản ban hành')], limit=1
                )
                if not kenh:
                    kenh = self.env['mail.channel'].create({
                        'name'        : 'Văn bản ban hành',
                        'channel_type': 'channel',
                        'description' : 'Thông báo tự động khi văn bản được ban hành',
                    })

            kenh.message_post(
                body=noi_dung,
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
            )

    def action_huy(self):
        for record in self:
            if record.state == 'issued':
                raise ValidationError(_('Không thể hủy văn bản đã ban hành.'))
            record.state = 'cancelled'

    @api.model
    def create(self, vals):
        count = self.env['van_ban_di'].search_count([]) + 1
        vals['so_hieu'] = f"{count}_{fields.Date.from_string(vals['ngay_di']).strftime('%Y%m%d')}"
        return super(VanBanDi, self).create(vals)

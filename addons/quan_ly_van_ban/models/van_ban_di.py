from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa thông tin van_ban_di'
    _rec_name = "tieu_de"

    ngay_di = fields.Date("Ngày đi", required=True)
    so_hieu = fields.Char("Số hiệu", store=True, readonly=True)
    trich_yeu = fields.Text("Trích yếu", required=True)
    tieu_de = fields.Char("Tiêu đề", required=True)
    tep_dinh_kem = fields.Binary("Tệp đính kèm")
    ho_so = fields.Many2one('ho_so', string='Hồ sơ')

    id_loai_van_ban = fields.Many2one('loai_van_ban', string='Loại văn bản')
    id_co_quan_ban_hanh = fields.Many2one('phong_ban', string='Cơ quan ban hành')
    id_nguoi_phat_hanh = fields.Many2one('nhan_vien', string='Người ký')
    dia_chi_nhan = fields.Text("Nơi nhận", required=True)
    id_do_mat = fields.Many2one('do_mat', string='Độ mật')
    id_nam = fields.Many2one('nam', string='Năm')

    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('pending', 'Trình ký'),
        ('signed', 'Đã ký'),
        ('issued', 'Ban hành'),
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


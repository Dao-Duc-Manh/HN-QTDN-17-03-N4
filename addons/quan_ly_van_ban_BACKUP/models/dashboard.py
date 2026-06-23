from odoo import models, fields, api


class VanBanDashboard(models.TransientModel):
    _name = 'van_ban.dashboard'
    _description = 'Dashboard Quản lý Văn bản'

    # Computed fields for statistics
    tong_van_ban_den = fields.Integer(string="Tổng văn bản đến", compute="_compute_statistics", store=False)
    tong_van_ban_di = fields.Integer(string="Tổng văn bản đi", compute="_compute_statistics", store=False)
    tong_nhan_su = fields.Integer(string="Tổng nhân sự", compute="_compute_statistics", store=False)
    cong_viec_hoan_thanh = fields.Integer(string="Công việc đã hoàn thành", compute="_compute_statistics", store=False)
    cong_viec_dang_xu_ly = fields.Integer(string="Công việc đang xử lý", compute="_compute_statistics", store=False)
    cong_viec_hoan_thanh_muon = fields.Integer(string="Công việc hoàn thành muộn", compute="_compute_statistics", store=False)
    cong_viec_da_nhan = fields.Integer(string="Công việc đã nhận", compute="_compute_statistics", store=False)

    @api.model
    def action_open_dashboard(self):
        """Tạo record dashboard và trả về action để mở form view"""
        dashboard = self.create({})
        # Tính toán statistics ngay sau khi tạo
        dashboard._compute_statistics()
        return {
            'name': 'Dashboard Quản lý Văn bản',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban.dashboard',
            'res_id': dashboard.id,
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref('quan_ly_van_ban.view_van_ban_dashboard_form').id,
        }

    @api.depends()
    def _compute_statistics(self):
        # Tổng số lượng
        self.tong_van_ban_den = self.env['van_ban_den'].search_count([])
        self.tong_van_ban_di = self.env['van_ban_di'].search_count([])
        # Kiểm tra xem model nhan_vien có tồn tại không
        try:
            self.tong_nhan_su = self.env['nhan_vien'].search_count([])
        except KeyError:
            # Model chưa được load, đặt giá trị mặc định
            self.tong_nhan_su = 0

        # Công việc theo trạng thái
        trang_thai_hoan_thanh = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành')], limit=1)
        trang_thai_dang_xu_ly = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đang xử lý')], limit=1)
        trang_thai_hoan_thanh_qua_han = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành quá hạn')], limit=1)
        trang_thai_da_nhan = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đã nhận')], limit=1)

        self.cong_viec_hoan_thanh = self.env['cong.viec'].search_count([('trang_thai', '=', trang_thai_hoan_thanh.id)]) if trang_thai_hoan_thanh else 0
        self.cong_viec_dang_xu_ly = self.env['cong.viec'].search_count([('trang_thai', '=', trang_thai_dang_xu_ly.id)]) if trang_thai_dang_xu_ly else 0
        self.cong_viec_hoan_thanh_muon = self.env['cong.viec'].search_count([('trang_thai', '=', trang_thai_hoan_thanh_qua_han.id)]) if trang_thai_hoan_thanh_qua_han else 0
        self.cong_viec_da_nhan = self.env['cong.viec'].search_count([('trang_thai', '=', trang_thai_da_nhan.id)]) if trang_thai_da_nhan else 0


    def action_view_van_ban_den(self):
        return {
            'name': 'Văn bản đến',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_den',
            'view_mode': 'tree,form',
        }

    def action_view_van_ban_di(self):
        return {
            'name': 'Văn bản đi',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_di',
            'view_mode': 'tree,form',
        }

    def action_view_nhan_su(self):
        # Kiểm tra xem model có tồn tại không
        try:
            self.env['nhan_vien']
            return {
                'name': 'Nhân sự',
                'type': 'ir.actions.act_window',
                'res_model': 'nhan_vien',
                'view_mode': 'tree,form',
            }
        except KeyError:
            # Model chưa được load, trả về action rỗng
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi',
                    'message': 'Module nhân sự chưa được cài đặt',
                    'type': 'danger',
                }
            }

    def action_view_cong_viec_chi_tiet(self):
        return {
            'name': 'Công việc',
            'type': 'ir.actions.act_window',
            'res_model': 'cong.viec',
            'view_mode': 'tree,form',
        }

    def action_view_cong_viec_hoan_thanh(self):
        trang_thai_hoan_thanh = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành')], limit=1)
        domain = [('trang_thai', '=', trang_thai_hoan_thanh.id)] if trang_thai_hoan_thanh else []
        return {
            'name': 'Công việc đã hoàn thành',
            'type': 'ir.actions.act_window',
            'res_model': 'cong.viec',
            'view_mode': 'tree,form',
            'domain': domain,
        }

    def action_view_cong_viec_dang_xu_ly(self):
        trang_thai_dang_xu_ly = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đang xử lý')], limit=1)
        domain = [('trang_thai', '=', trang_thai_dang_xu_ly.id)] if trang_thai_dang_xu_ly else []
        return {
            'name': 'Công việc đang xử lý',
            'type': 'ir.actions.act_window',
            'res_model': 'cong.viec',
            'view_mode': 'tree,form',
            'domain': domain,
        }

    def action_view_cong_viec_hoan_thanh_muon(self):
        trang_thai_hoan_thanh_qua_han = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành quá hạn')], limit=1)
        domain = [('trang_thai', '=', trang_thai_hoan_thanh_qua_han.id)] if trang_thai_hoan_thanh_qua_han else []
        return {
            'name': 'Công việc hoàn thành muộn',
            'type': 'ir.actions.act_window',
            'res_model': 'cong.viec',
            'view_mode': 'tree,form',
            'domain': domain,
        }

    def action_view_cong_viec_da_nhan(self):
        trang_thai_da_nhan = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đã nhận')], limit=1)
        domain = [('trang_thai', '=', trang_thai_da_nhan.id)] if trang_thai_da_nhan else []
        return {
            'name': 'Công việc đã nhận',
            'type': 'ir.actions.act_window',
            'res_model': 'cong.viec',
            'view_mode': 'tree,form',
            'domain': domain,
        }


from odoo import models, fields, api
from odoo.tools import html_escape


class DashboardMD(models.Model):
    _name = 'dashboard_md'
    _description = 'Dashboard Management'

    # Tổng số liệu
    total_van_ban_den = fields.Integer(string="Tổng số văn bản đến", compute="_compute_total_van_ban_den")
    total_van_ban_di = fields.Integer(string="Tổng số văn bản đi", compute="_compute_total_van_ban_di")
    total_nhan_su = fields.Integer(string="Tổng số nhân sự", compute="_compute_total_nhan_su")
    
    # Danh sách văn bản đi
    van_ban_di_list = fields.Many2many('van_ban_di',compute="_compute_van_ban_di_list", string="Danh sách văn bản đi", default=[])
    van_ban_di_text = fields.Text(string="Danh sách văn bản đi", compute="_compute_van_ban_di_text")
    
    # Danh sách văn bản đến
    van_ban_den_list = fields.Many2many('van_ban_den', compute="_compute_van_ban_den_list", string="Danh sách văn bản đến", default=[])
    van_ban_den_text = fields.Text(string="Danh sách văn bản đến", compute="_compute_van_ban_den_text")

    # Danh sách nhân viên
    nhan_vien_list = fields.Many2many('nhan_vien', compute="_compute_nhan_vien_list", string="Danh sách nhân viên", default=[])
    nhan_vien_text = fields.Text(string="Danh sách nhân viên", compute="_compute_nhan_vien_text")
    
    # === Các field hiển thị danh sách công việc ===
    cong_viec_da_nhan_list = fields.Many2many('cong_viec', compute="_compute_cong_viec_da_nhan_list")
    cong_viec_hoan_thanh_muon_list = fields.Many2many('cong_viec', compute="_compute_cong_viec_hoan_thanh_muon_list")
    cong_viec_da_hoan_thanh_list = fields.Many2many('cong_viec', compute="_compute_cong_viec_da_hoan_thanh_list")
    cong_viec_dang_xu_ly_list = fields.Many2many('cong_viec', compute="_compute_cong_viec_dang_xu_ly_list")

    # === Các field hiển thị công việc dạng text ===
    cong_viec_da_nhan_text = fields.Text(compute="_compute_cong_viec_da_nhan_text")
    cong_viec_hoan_thanh_muon_text = fields.Text(compute="_compute_cong_viec_hoan_thanh_muon_text")
    cong_viec_da_hoan_thanh_text = fields.Text(compute="_compute_cong_viec_da_hoan_thanh_text")
    cong_viec_dang_xu_ly_text = fields.Text(compute="_compute_cong_viec_dang_xu_ly_text")

    # ===== Tính tổng số liệu =====
    @api.depends()
    def _compute_total_van_ban_den(self):
        for record in self:
            record.total_van_ban_den = self.env['van_ban_den'].search_count([])

    @api.depends()
    def _compute_total_van_ban_di(self):
        for record in self:
            record.total_van_ban_di = self.env['van_ban_di'].search_count([])
            
    @api.depends()
    def _compute_total_nhan_su(self):
        for record in self:
            record.total_nhan_su = self.env['nhan_vien'].search_count([])
            
    # ===== Lấy danh sách văn bản đi =====        
    @api.depends()
    def _compute_van_ban_di_list(self):
        for record in self:
            record.van_ban_di_list = self.env['van_ban_di'].search([], order="ngay_di desc", limit=5)  # Lấy 5 văn bản mới nhất
    @api.depends()
    def _compute_van_ban_di_text(self):
        for record in self:
            van_ban_list = self.env['van_ban_di'].search([], order="ngay_di desc", limit=5)
            if van_ban_list:
                text_lines = [f"📄 {vb.id} | {vb.ngay_di} | {vb.so_hieu} | {vb.id_nguoi_phat_hanh.ho_ten} | {vb.id_loai_van_ban.id} | {vb.id_nam.nam}" for vb in van_ban_list]
                record.van_ban_di_text = "".join(text_lines)  # Ghép với ký tự xuống dòng
            else:
                record.van_ban_di_text = "Không có văn bản đi nào"
                
    # ===== Lấy danh sách văn bản đến =====
    @api.depends()
    def _compute_van_ban_den_list(self):
        for record in self:
            record.van_ban_den_list = self.env['van_ban_den'].search([], order="ngay_den desc", limit=5)

    @api.depends()
    def _compute_van_ban_den_text(self):
        for record in self:
            van_ban_list = self.env['van_ban_den'].search([], order="ngay_den desc", limit=5)
            if van_ban_list:
                text_lines = [f"📄 {vb.id} | {vb.ngay_den} | {vb.so_hieu} | {vb.co_quan_ban_hanh} | {vb.id_loai_van_ban.id} | {vb.id_nam.nam}" for vb in van_ban_list]
                record.van_ban_den_text = "".join(text_lines)
            else:
                record.van_ban_den_text = "Không có văn bản đến nào"

    # ===== Lấy danh sách nhân viên =====
    @api.depends()
    def _compute_nhan_vien_list(self):
        for record in self:
            record.nhan_vien_list = self.env['nhan_vien'].search([], order="ngay_sinh desc", limit=5)

    @api.depends()
    def _compute_nhan_vien_text(self):
        for record in self:
            nhan_vien_list = self.env['nhan_vien'].search([], order="ngay_sinh desc", limit=5)
            if nhan_vien_list:
                text_lines = [f"👤 {nv.ma_dinh_danh} | {nv.ho_ten} | {nv.ngay_sinh} | {nv.tuoi} |{nv.lich_su_cong_tac_ids.chuc_vu_id.ten_chuc_vu} | {nv.so_dien_thoai}" for nv in nhan_vien_list]
                record.nhan_vien_text = "".join(text_lines)
            else:
                record.nhan_vien_text = "Không có nhân viên nào"

   # ===== Lấy danh sách công việc đã nhận =====
    @api.depends()
    def _compute_cong_viec_da_nhan_list(self):
        for record in self:
            record.cong_viec_da_nhan_list = self.env['cong_viec'].search([('trang_thai.ten_trang_thai', '=', 'Đã nhận')], order="han_xu_ly asc", limit=5)

    @api.depends()
    def _compute_cong_viec_da_nhan_text(self):
        for record in self:
            cong_viec_list = self.env['cong_viec'].search([('trang_thai.ten_trang_thai', '=', 'Đã nhận')], order="han_xu_ly asc", limit=5)
            if cong_viec_list:
                text_lines = [f"📩 {cv.id} | {cv.ten_cong_viec} | Hạn: {cv.han_xu_ly} | Người xử lý: {cv.chu_tri_giai_quyet.ho_ten}" for cv in cong_viec_list]
                record.cong_viec_da_nhan_text = "\n".join(text_lines)
            else:
                record.cong_viec_da_nhan_text = "Không có công việc đã nhận"

    # ===== Lấy danh sách công việc hoàn thành muộn =====
    @api.depends()
    def _compute_cong_viec_hoan_thanh_muon_list(self):
        for record in self:
            record.cong_viec_hoan_thanh_muon_list = self.env['cong_viec'].search(
                [('trang_thai.ten_trang_thai', '=', 'Hoàn thành quá hạn')], order="ngay_hoan_thanh desc", limit=5)

    @api.depends()
    def _compute_cong_viec_hoan_thanh_muon_text(self):
        for record in self:
            cong_viec_list = self.env['cong_viec'].search(
                [('trang_thai.ten_trang_thai', '=', 'Hoàn thành quá hạn')], order="ngay_hoan_thanh desc", limit=5)
            if cong_viec_list:
                text_lines = [f"⏳ {cv.id} | {cv.ten_cong_viec} | Hoàn thành: {cv.ngay_hoan_thanh} | Người xử lý: {cv.chu_tri_giai_quyet.ho_ten}" for cv in cong_viec_list]
                record.cong_viec_hoan_thanh_muon_text = "\n".join(text_lines)
            else:
                record.cong_viec_hoan_thanh_muon_text = "Không có công việc hoàn thành muộn"

    # ===== Lấy danh sách công việc đã hoàn thành =====
    @api.depends()
    def _compute_cong_viec_da_hoan_thanh_list(self):
        for record in self:
            record.cong_viec_da_hoan_thanh_list = self.env['cong_viec'].search(
                [('trang_thai.ten_trang_thai', '=', 'Hoàn thành')], order="ngay_hoan_thanh desc", limit=5)

    @api.depends()
    def _compute_cong_viec_da_hoan_thanh_text(self):
        for record in self:
            cong_viec_list = self.env['cong_viec'].search(
                [('trang_thai.ten_trang_thai', '=', 'Hoàn thành')], order="ngay_hoan_thanh desc", limit=5)
            if cong_viec_list:
                text_lines = [f"✅ {cv.id} | {cv.ten_cong_viec} | Hoàn thành: {cv.ngay_hoan_thanh} | Người xử lý: {cv.chu_tri_giai_quyet.ho_ten}" for cv in cong_viec_list]
                record.cong_viec_da_hoan_thanh_text = "\n".join(text_lines)
            else:
                record.cong_viec_da_hoan_thanh_text = "Không có công việc đã hoàn thành"

    # ===== Lấy danh sách công việc đang xử lý =====
    @api.depends()
    def _compute_cong_viec_dang_xu_ly_list(self):
        for record in self:
            record.cong_viec_dang_xu_ly_list = self.env['cong_viec'].search(
                [('trang_thai.ten_trang_thai', '=', 'Đang xử lý')], order="han_xu_ly asc", limit=5)

    @api.depends()
    def _compute_cong_viec_dang_xu_ly_text(self):
        for record in self:
            cong_viec_list = self.env['cong_viec'].search(
                [('trang_thai.ten_trang_thai', '=', 'Đang xử lý')], order="han_xu_ly asc", limit=5)
            if cong_viec_list:
                text_lines = [f"🔄 {cv.id} | {cv.ten_cong_viec} | Hạn: {cv.han_xu_ly} | Người xử lý: {cv.chu_tri_giai_quyet.ho_ten}" for cv in cong_viec_list]
                record.cong_viec_dang_xu_ly_text = "\n".join(text_lines)
            else:
                record.cong_viec_dang_xu_ly_text = "Không có công việc đang xử lý"

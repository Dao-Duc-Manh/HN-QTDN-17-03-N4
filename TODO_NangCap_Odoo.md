# 📋 TODO – Nâng cấp Hệ thống Odoo 15
**Dự án:** TTDN_16-06_N8 | **Nhóm 4 – CNTT 16-01**  
**Mục tiêu:** Ý tưởng 1 (Quy trình phê duyệt văn bản) + Ý tưởng 3 (Phân quyền bảo mật độ mật)

---

## ⚡ TRƯỚC KHI BẮT ĐẦU

```bash
# Đảm bảo Docker đang chạy
cd ~/TTDN_16-06_N8
sudo docker-compose ps
```

---

## BƯỚC 1 – Backup dự án

> Không ảnh hưởng hệ thống đang chạy.

```bash
cp -r ~/TTDN_16-06_N8/addons/quan_ly_van_ban \
      ~/TTDN_16-06_N8/addons/quan_ly_van_ban_BACKUP
```

- [ ] Backup xong ✓

---

## BƯỚC 2 – Cập nhật `models/van_ban_di.py`

> Thêm `_inherit = ['mail.thread', 'mail.activity.mixin']`, field `trang_thai_phe_duyet`, `ly_do_tu_choi`, và 5 action button.

```bash
# Backup file gốc
cp ~/TTDN_16-06_N8/addons/quan_ly_van_ban/models/van_ban_di.py \
   ~/TTDN_16-06_N8/addons/quan_ly_van_ban/models/van_ban_di.py.bak

# Ghi đè bằng nội dung mới
cat > ~/TTDN_16-06_N8/addons/quan_ly_van_ban/models/van_ban_di.py << 'PYEOF'
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa thông tin van_ban_di'
    _rec_name = "tieu_de"
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    id_do_mat           = fields.Many2one('do_mat', string='Độ mật', tracking=True)
    id_nam              = fields.Many2one('nam', string='Năm')

    trang_thai_phe_duyet = fields.Selection([
        ('nhap',      'Nháp'),
        ('cho_duyet', 'Chờ phê duyệt'),
        ('da_duyet',  'Đã duyệt'),
        ('tu_choi',   'Bị từ chối'),
        ('ban_hanh',  'Đã ban hành'),
    ], string='Trạng thái phê duyệt', default='nhap', tracking=True, copy=False)

    ly_do_tu_choi = fields.Text("Lý do từ chối", tracking=True, copy=False)

    def action_gui_duyet(self):
        for rec in self:
            if rec.trang_thai_phe_duyet != 'nhap':
                raise exceptions.UserError('Chỉ văn bản ở trạng thái Nháp mới được gửi duyệt!')
            rec.write({'trang_thai_phe_duyet': 'cho_duyet'})
            rec.message_post(body='📤 Văn bản đã được gửi đi chờ phê duyệt.',
                             message_type='comment', subtype_xmlid='mail.mt_note')

    def action_phe_duyet(self):
        for rec in self:
            rec.write({'trang_thai_phe_duyet': 'da_duyet', 'ly_do_tu_choi': False})
            rec.message_post(body='✅ Văn bản đã được phê duyệt.',
                             message_type='comment', subtype_xmlid='mail.mt_note')

    def action_tu_choi(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nhập lý do từ chối',
            'res_model': 'van_ban_di.tu_choi.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_van_ban_id': self.id},
        }

    def action_ban_hanh(self):
        for rec in self:
            if rec.trang_thai_phe_duyet != 'da_duyet':
                raise exceptions.UserError('Chỉ văn bản Đã duyệt mới có thể ban hành!')
            rec.write({'trang_thai_phe_duyet': 'ban_hanh'})
            rec.message_post(body='📢 Văn bản đã được ban hành chính thức.',
                             message_type='comment', subtype_xmlid='mail.mt_note')

    def action_ve_nhap(self):
        for rec in self:
            rec.write({'trang_thai_phe_duyet': 'nhap', 'ly_do_tu_choi': False})

    @api.model
    def create(self, vals):
        count = self.env['van_ban_di'].search_count([]) + 1
        vals['so_hieu'] = f"{count}_{fields.Date.from_string(vals['ngay_di']).strftime('%Y%m%d')}"
        return super(VanBanDi, self).create(vals)
PYEOF
```

- [ ] File `van_ban_di.py` đã được thay thế ✓

---

## BƯỚC 3 – Tạo file `models/van_ban_di_tu_choi_wizard.py` (MỚI)

```bash
cat > ~/TTDN_16-06_N8/addons/quan_ly_van_ban/models/van_ban_di_tu_choi_wizard.py << 'PYEOF'
# -*- coding: utf-8 -*-
from odoo import models, fields


class VanBanDiTuChoiWizard(models.TransientModel):
    _name = 'van_ban_di.tu_choi.wizard'
    _description = 'Wizard Từ Chối Văn Bản Đi'

    van_ban_id = fields.Many2one('van_ban_di', string='Văn bản', required=True)
    ly_do = fields.Text(string='Lý do từ chối', required=True)

    def action_xac_nhan_tu_choi(self):
        self.van_ban_id.write({
            'trang_thai_phe_duyet': 'tu_choi',
            'ly_do_tu_choi': self.ly_do,
        })
        self.van_ban_id.message_post(
            body=f'❌ <b>Từ chối:</b> {self.ly_do}',
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )
        return {'type': 'ir.actions.act_window_close'}
PYEOF
```

- [ ] File wizard đã tạo xong ✓

---

## BƯỚC 4 – Cập nhật `models/__init__.py`

```bash
# Thêm dòng import wizard vào sau dòng "from . import van_ban_di"
sed -i '/from . import van_ban_di$/a from . import van_ban_di_tu_choi_wizard' \
    ~/TTDN_16-06_N8/addons/quan_ly_van_ban/models/__init__.py

# Kiểm tra — phải thấy dòng wizard trong kết quả
cat ~/TTDN_16-06_N8/addons/quan_ly_van_ban/models/__init__.py
```

> ✅ Kết quả đúng sẽ có dòng: `from . import van_ban_di_tu_choi_wizard`

- [ ] `__init__.py` đã cập nhật ✓

---

## BƯỚC 5 – Cập nhật `views/van_ban_di.xml`

```bash
# Backup view gốc
cp ~/TTDN_16-06_N8/addons/quan_ly_van_ban/views/van_ban_di.xml \
   ~/TTDN_16-06_N8/addons/quan_ly_van_ban/views/van_ban_di.xml.bak

# Ghi đè bằng nội dung mới
cat > ~/TTDN_16-06_N8/addons/quan_ly_van_ban/views/van_ban_di.xml << 'XMLEOF'
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="view_van_ban_di_form" model="ir.ui.view">
            <field name="name">van_ban_di</field>
            <field name="model">van_ban_di</field>
            <field name="arch" type="xml">
                <form string="Quản lý Văn bản Đi">
                    <header>
                        <button name="action_gui_duyet" string="📤 Gửi duyệt"
                                type="object" class="oe_highlight"
                                attrs="{'invisible': [('trang_thai_phe_duyet', '!=', 'nhap')]}"/>
                        <button name="action_phe_duyet" string="✅ Phê duyệt"
                                type="object" class="btn-success"
                                attrs="{'invisible': [('trang_thai_phe_duyet', '!=', 'cho_duyet')]}"
                                groups="quan_ly_van_ban.group_truong_phong_qlvb"/>
                        <button name="action_tu_choi" string="❌ Từ chối"
                                type="object" class="btn-danger"
                                attrs="{'invisible': [('trang_thai_phe_duyet', '!=', 'cho_duyet')]}"
                                groups="quan_ly_van_ban.group_truong_phong_qlvb"/>
                        <button name="action_ban_hanh" string="📢 Ban hành"
                                type="object" class="oe_highlight"
                                attrs="{'invisible': [('trang_thai_phe_duyet', '!=', 'da_duyet')]}"/>
                        <button name="action_ve_nhap" string="↩ Về Nháp"
                                type="object"
                                attrs="{'invisible': [('trang_thai_phe_duyet', '!=', 'tu_choi')]}"/>
                        <field name="trang_thai_phe_duyet" widget="statusbar"
                               statusbar_visible="nhap,cho_duyet,da_duyet,ban_hanh"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <h2 class="text-primary" style="font-size: 25px; font-weight: bold;">
                                Văn bản đi</h2>
                        </div>
                        <div class="alert alert-danger"
                             attrs="{'invisible': [('trang_thai_phe_duyet', '!=', 'tu_choi')]}">
                            <strong>❌ Lý do từ chối:</strong>
                            <field name="ly_do_tu_choi" readonly="1" nolabel="1"/>
                        </div>
                        <div class="card p-3 shadow-sm mb-3">
                            <group col="4">
                                <field name="so_hieu" class="o_form_required"/>
                                <field name="tieu_de"/>
                                <field name="trich_yeu"/>
                            </group>
                        </div>
                        <div class="card p-3 shadow-sm mb-3">
                            <group col="4">
                                <field name="dia_chi_nhan"/>
                                <field name="ngay_di"/>
                                <field name="id_nguoi_phat_hanh"/>
                                <field name="id_co_quan_ban_hanh"/>
                            </group>
                        </div>
                        <div class="card p-3 shadow-sm mb-3">
                            <group col="4">
                                <field name="id_do_mat"/>
                                <field name="id_nam"/>
                                <field name="ho_so"/>
                                <field name="id_loai_van_ban"/>
                            </group>
                        </div>
                        <div class="card p-3 shadow-sm">
                            <h3 class="text-secondary">File đính kèm</h3>
                            <group col="4">
                                <field name="tep_dinh_kem" widget="pdf_viewer"/>
                            </group>
                        </div>
                        <notebook></notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids" widget="mail_followers"/>
                        <field name="activity_ids" widget="mail_activity"/>
                        <field name="message_ids" widget="mail_thread"/>
                    </div>
                </form>
            </field>
        </record>

        <record id="view_van_ban_di_tree" model="ir.ui.view">
            <field name="name">van_ban_di</field>
            <field name="model">van_ban_di</field>
            <field name="arch" type="xml">
                <tree decoration-success="trang_thai_phe_duyet == 'ban_hanh'"
                      decoration-warning="trang_thai_phe_duyet == 'cho_duyet'"
                      decoration-danger="trang_thai_phe_duyet == 'tu_choi'"
                      decoration-muted="trang_thai_phe_duyet == 'nhap'">
                    <field name="so_hieu"/>
                    <field name="tieu_de"/>
                    <field name="ngay_di"/>
                    <field name="ho_so"/>
                    <field name="id_loai_van_ban"/>
                    <field name="id_nguoi_phat_hanh"/>
                    <field name="id_do_mat"/>
                    <field name="id_co_quan_ban_hanh"/>
                    <field name="trang_thai_phe_duyet" widget="badge"
                           decoration-success="trang_thai_phe_duyet in ['ban_hanh','da_duyet']"
                           decoration-warning="trang_thai_phe_duyet == 'cho_duyet'"
                           decoration-danger="trang_thai_phe_duyet == 'tu_choi'"/>
                </tree>
            </field>
        </record>

        <record model="ir.ui.view" id="van_ban_di_search">
            <field name="model">van_ban_di</field>
            <field name="arch" type="xml">
                <search>
                    <field name="so_hieu"/>
                    <field name="trich_yeu"/>
                    <field name="tieu_de"/>
                    <field name="ngay_di"/>
                    <field name="id_loai_van_ban"/>
                    <filter name="filter_cho_duyet" string="Chờ phê duyệt"
                            domain="[('trang_thai_phe_duyet','=','cho_duyet')]"/>
                    <filter name="filter_da_duyet" string="Đã duyệt"
                            domain="[('trang_thai_phe_duyet','=','da_duyet')]"/>
                    <filter name="filter_ban_hanh" string="Đã ban hành"
                            domain="[('trang_thai_phe_duyet','=','ban_hanh')]"/>
                    <filter name="filter_tu_choi" string="Bị từ chối"
                            domain="[('trang_thai_phe_duyet','=','tu_choi')]"/>
                    <group expand="0" string="Nhóm theo">
                        <filter name="group_trang_thai" string="Trạng thái phê duyệt"
                                context="{'group_by': 'trang_thai_phe_duyet'}"/>
                    </group>
                </search>
            </field>
        </record>

        <record id="action_van_ban_di" model="ir.actions.act_window">
            <field name="name">Quản lý Văn Bản Đi</field>
            <field name="res_model">van_ban_di</field>
            <field name="view_mode">tree,form</field>
            <field name="search_view_id" ref="van_ban_di_search"/>
        </record>
    </data>
</odoo>
XMLEOF
```

- [ ] `van_ban_di.xml` đã cập nhật ✓

---

## BƯỚC 6 – Tạo `views/van_ban_di_tu_choi_wizard.xml` (MỚI)

```bash
cat > ~/TTDN_16-06_N8/addons/quan_ly_van_ban/views/van_ban_di_tu_choi_wizard.xml << 'XMLEOF'
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="view_van_ban_di_tu_choi_wizard_form" model="ir.ui.view">
            <field name="name">van_ban_di.tu_choi.wizard.form</field>
            <field name="model">van_ban_di.tu_choi.wizard</field>
            <field name="arch" type="xml">
                <form string="Từ chối Văn bản Đi">
                    <group>
                        <field name="van_ban_id" readonly="1"/>
                        <field name="ly_do" placeholder="Nhập lý do từ chối chi tiết..."/>
                    </group>
                    <footer>
                        <button name="action_xac_nhan_tu_choi"
                                string="✔ Xác nhận từ chối"
                                type="object" class="btn-danger"/>
                        <button string="Hủy" class="btn-secondary" special="cancel"/>
                    </footer>
                </form>
            </field>
        </record>
    </data>
</odoo>
XMLEOF
```

- [ ] `van_ban_di_tu_choi_wizard.xml` đã tạo ✓

---

## BƯỚC 7 – Tạo `security/security_groups.xml` (MỚI)

```bash
cat > ~/TTDN_16-06_N8/addons/quan_ly_van_ban/security/security_groups.xml << 'XMLEOF'
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="module_category_qlvb" model="ir.module.category">
            <field name="name">Quản lý Văn bản</field>
            <field name="sequence">20</field>
        </record>
        <record id="group_nhan_vien_qlvb" model="res.groups">
            <field name="name">Nhân viên Văn thư</field>
            <field name="category_id" ref="module_category_qlvb"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>
        <record id="group_truong_phong_qlvb" model="res.groups">
            <field name="name">Trưởng phòng Văn thư</field>
            <field name="category_id" ref="module_category_qlvb"/>
            <field name="implied_ids" eval="[(4, ref('group_nhan_vien_qlvb'))]"/>
        </record>
        <record id="group_ban_giam_doc_qlvb" model="res.groups">
            <field name="name">Ban Giám đốc Văn thư</field>
            <field name="category_id" ref="module_category_qlvb"/>
            <field name="implied_ids" eval="[(4, ref('group_truong_phong_qlvb'))]"/>
        </record>
    </data>
</odoo>
XMLEOF
```

- [ ] `security_groups.xml` đã tạo ✓

---

## BƯỚC 8 – Tạo `security/security_rules.xml` (MỚI)

```bash
cat > ~/TTDN_16-06_N8/addons/quan_ly_van_ban/security/security_rules.xml << 'XMLEOF'
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <record id="rule_van_ban_di_nhan_vien" model="ir.rule">
            <field name="name">VanBanDi: Nhân viên chỉ xem văn bản Thường</field>
            <field name="model_id" ref="model_van_ban_di"/>
            <field name="domain_force">['|',('id_do_mat','=',False),('id_do_mat.do_mat','in',['Thường','thuong'])]</field>
            <field name="perm_read" eval="True"/><field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/><field name="perm_unlink" eval="False"/>
            <field name="groups" eval="[(4, ref('group_nhan_vien_qlvb'))]"/>
        </record>
        <record id="rule_van_ban_di_truong_phong" model="ir.rule">
            <field name="name">VanBanDi: Trưởng phòng xem Thường và Mật</field>
            <field name="model_id" ref="model_van_ban_di"/>
            <field name="domain_force">['|',('id_do_mat','=',False),('id_do_mat.do_mat','in',['Thường','thuong','Mật','mat'])]</field>
            <field name="perm_read" eval="True"/><field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/><field name="perm_unlink" eval="False"/>
            <field name="groups" eval="[(4, ref('group_truong_phong_qlvb'))]"/>
        </record>
        <record id="rule_van_ban_di_giam_doc" model="ir.rule">
            <field name="name">VanBanDi: Ban Giám đốc xem toàn bộ</field>
            <field name="model_id" ref="model_van_ban_di"/>
            <field name="domain_force">[(1,'=',1)]</field>
            <field name="perm_read" eval="True"/><field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/><field name="perm_unlink" eval="True"/>
            <field name="groups" eval="[(4, ref('group_ban_giam_doc_qlvb'))]"/>
        </record>
        <record id="rule_van_ban_den_nhan_vien" model="ir.rule">
            <field name="name">VanBanDen: Nhân viên chỉ xem văn bản Thường</field>
            <field name="model_id" ref="model_van_ban_den"/>
            <field name="domain_force">['|',('id_do_mat','=',False),('id_do_mat.do_mat','in',['Thường','thuong'])]</field>
            <field name="perm_read" eval="True"/><field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/><field name="perm_unlink" eval="False"/>
            <field name="groups" eval="[(4, ref('group_nhan_vien_qlvb'))]"/>
        </record>
        <record id="rule_van_ban_den_truong_phong" model="ir.rule">
            <field name="name">VanBanDen: Trưởng phòng xem Thường và Mật</field>
            <field name="model_id" ref="model_van_ban_den"/>
            <field name="domain_force">['|',('id_do_mat','=',False),('id_do_mat.do_mat','in',['Thường','thuong','Mật','mat'])]</field>
            <field name="perm_read" eval="True"/><field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/><field name="perm_unlink" eval="False"/>
            <field name="groups" eval="[(4, ref('group_truong_phong_qlvb'))]"/>
        </record>
        <record id="rule_van_ban_den_giam_doc" model="ir.rule">
            <field name="name">VanBanDen: Ban Giám đốc xem toàn bộ</field>
            <field name="model_id" ref="model_van_ban_den"/>
            <field name="domain_force">[(1,'=',1)]</field>
            <field name="perm_read" eval="True"/><field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/><field name="perm_unlink" eval="True"/>
            <field name="groups" eval="[(4, ref('group_ban_giam_doc_qlvb'))]"/>
        </record>
    </data>
</odoo>
XMLEOF
```

- [ ] `security_rules.xml` đã tạo ✓

---

## BƯỚC 9 – Cập nhật `security/ir.model.access.csv`

```bash
# Thêm dòng access cho wizard vào cuối file
echo "access_van_ban_di_tu_choi_wizard,van_ban_di.tu_choi.wizard,model_van_ban_di_tu_choi_wizard,base.group_user,1,1,1,1" \
  >> ~/TTDN_16-06_N8/addons/quan_ly_van_ban/security/ir.model.access.csv

# Kiểm tra
tail -3 ~/TTDN_16-06_N8/addons/quan_ly_van_ban/security/ir.model.access.csv
```

- [ ] `ir.model.access.csv` đã cập nhật ✓

---

## BƯỚC 10 – Cập nhật `__manifest__.py`

```bash
# Backup
cp ~/TTDN_16-06_N8/addons/quan_ly_van_ban/__manifest__.py \
   ~/TTDN_16-06_N8/addons/quan_ly_van_ban/__manifest__.py.bak

# Mở nano để sửa thủ công
nano ~/TTDN_16-06_N8/addons/quan_ly_van_ban/__manifest__.py
```

**Thay 2 chỗ trong file:**

1. Sửa `'depends'` — thêm `'mail'`:
```python
'depends': ['base', 'mail', 'nhan_su'],
```

2. Sửa `'data'` — thêm 3 file mới, đúng thứ tự:
```python
'data': [
    'security/security_groups.xml',
    'security/ir.model.access.csv',
    'security/security_rules.xml',
    'data/van_ban_data.xml',
    'views/van_ban_di.xml',
    'views/van_ban_di_tu_choi_wizard.xml',
    'views/trang_thai.xml',
    'views/do_mat.xml',
    'views/loai_van_ban.xml',
    'views/van_ban_den.xml',
    'views/nam.xml',
    'views/cong_viec.xml',
    'views/ho_so.xml',
    'views/dashboard.xml',
    'views/dashboard_main.xml',
    'views/menu.xml',
],
```

> **Ctrl+O** để lưu, **Ctrl+X** để thoát nano.

- [ ] `__manifest__.py` đã cập nhật ✓

---

## BƯỚC 11 – Restart Docker và Update module

```bash
cd ~/TTDN_16-06_N8

# Restart Docker
sudo docker-compose down
sudo docker-compose up -d

# Đợi Odoo khởi động (khoảng 15 giây)
sleep 15

# Update module
sudo docker-compose exec odoo python odoo-bin \
  -c /etc/odoo/odoo.conf \
  -u quan_ly_van_ban \
  --stop-after-init
```

- [ ] Docker restart thành công ✓
- [ ] Module update không có lỗi ✓

---

## BƯỚC 12 – Kiểm tra log nếu có lỗi

```bash
# Xem log realtime
sudo docker-compose logs odoo --tail=60

# Lọc chỉ lỗi
sudo docker-compose logs odoo 2>&1 | grep -E "ERROR|WARNING|UserError|traceback" | tail -30
```

---

## BƯỚC 13 – Gán quyền cho user test

1. Vào **Settings > Users & Companies > Users**
2. Chọn user muốn test → tab **Access Rights**
3. Tìm section **"Quản lý Văn bản"**
4. Gán nhóm:
   - `Nhân viên Văn thư` → chỉ xem văn bản Thường
   - `Trưởng phòng Văn thư` → xem Thường + Mật, được phê duyệt
   - `Ban Giám đốc Văn thư` → xem tất cả

- [ ] Đã gán quyền cho ít nhất 2 user test ✓

---

## ✅ CHECKLIST KIỂM TRA CUỐI

### Ý tưởng 1 – Quy trình phê duyệt
- [ ] Mở form Văn bản Đi → thấy **thanh trạng thái** phía trên (Nháp → Chờ duyệt → Đã duyệt → Ban hành)
- [ ] Bấm **"📤 Gửi duyệt"** → trạng thái chuyển sang "Chờ phê duyệt"
- [ ] Đăng nhập Trưởng phòng → thấy nút **"✅ Phê duyệt"** và **"❌ Từ chối"**
- [ ] Bấm **"❌ Từ chối"** → popup wizard hiện ra để nhập lý do
- [ ] Sau từ chối → thấy **hộp đỏ hiển thị lý do** trên form
- [ ] Cuối form có **khu vực Chatter** ghi lịch sử mỗi lần đổi trạng thái
- [ ] List view Văn bản Đi → cột trạng thái màu sắc (xanh/vàng/đỏ)

### Ý tưởng 3 – Phân quyền độ mật
- [ ] **Settings > Users > Groups** → thấy nhóm "Quản lý Văn bản" với 3 nhóm con
- [ ] User **Nhân viên** → chỉ thấy văn bản có độ mật "Thường" hoặc không có độ mật
- [ ] User **Trưởng phòng** → thấy "Thường" + "Mật", không thấy "Tuyệt mật"
- [ ] User **Ban Giám đốc** → thấy tất cả văn bản

---

## 🛠️ XỬ LÝ LỖI THƯỜNG GẶP

| Lỗi | Nguyên nhân | Cách sửa |
|-----|------------|----------|
| `'mail' module not found` | Thiếu `'mail'` trong depends | Thêm `'mail'` vào `__manifest__.py` |
| `Chatter không hiện` | Thiếu `_inherit = ['mail.thread'...]` | Kiểm tra lại `van_ban_di.py` bước 2 |
| `ref 'group_truong_phong_qlvb' not found` | `security_groups.xml` chưa load | Đảm bảo nó đứng đầu trong `data:` của manifest |
| `model_van_ban_di_tu_choi_wizard not found` | Chưa thêm dòng vào `ir.model.access.csv` | Kiểm tra lại bước 9 |
| `Access Denied` khi mở form | Record rule quá chặt | Vào Settings > Technical > Security > Record Rules để kiểm tra |
| `module not loading` | Lỗi Python syntax | Chạy `sudo docker-compose logs odoo \| grep ERROR` |

---

*File này tạo bởi Claude — dự án TTDN_16-06_N8 | Tháng 6/2026*

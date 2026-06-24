odoo.define('quan_ly_van_ban.chatbox', function (require) {
    'use strict';

    var ajax = require('web.ajax');

    $(document).ready(function () {
        $('body').append(`
            <div id="qlvb-chatbox-btn" title="Tìm kiếm tài liệu">🔍</div>
            <div id="qlvb-chatbox">
                <div id="qlvb-chatbox-header">
                    <span>🔍 Tìm kiếm tài liệu</span>
                    <button id="qlvb-chatbox-close">✕</button>
                </div>
                <div id="qlvb-chatbox-body">
                    <div id="qlvb-chatbox-messages">
                        <div class="qlvb-msg-bot">Xin chào! Tôi có thể giúp bạn tìm kiếm văn bản, công việc hoặc khách hàng. Hãy nhập từ khóa.</div>
                    </div>
                    <div id="qlvb-chatbox-input-area">
                        <input type="text" id="qlvb-chatbox-input" placeholder="Nhập từ khóa tìm kiếm..." />
                        <button id="qlvb-chatbox-send">Tìm</button>
                    </div>
                </div>
            </div>
        `);

        $('#qlvb-chatbox-btn').on('click', function () {
            $('#qlvb-chatbox').toggleClass('qlvb-open');
            if ($('#qlvb-chatbox').hasClass('qlvb-open')) {
                $('#qlvb-chatbox-input').focus();
            }
        });

        $('#qlvb-chatbox-close').on('click', function () {
            $('#qlvb-chatbox').removeClass('qlvb-open');
        });

        function scrollToBottom() {
            var msgs = document.getElementById('qlvb-chatbox-messages');
            if (msgs) msgs.scrollTop = msgs.scrollHeight;
        }

        function guiTimKiem() {
            var tu_khoa = $('#qlvb-chatbox-input').val().trim();
            if (!tu_khoa) return;

            $('#qlvb-chatbox-messages').append(`<div class="qlvb-msg-user">${tu_khoa}</div>`);
            $('#qlvb-chatbox-input').val('');
            $('#qlvb-chatbox-messages').append(`<div class="qlvb-msg-bot qlvb-loading" id="qlvb-loading">⏳ Đang tìm kiếm...</div>`);
            scrollToBottom();

            ajax.jsonRpc('/qlvb/search', 'call', {tu_khoa: tu_khoa})
                .then(function (data) {
                    $('#qlvb-loading').remove();

                    if (!data.results || data.results.length === 0) {
                        $('#qlvb-chatbox-messages').append(`<div class="qlvb-msg-bot">❌ ${data.message}</div>`);
                    } else {
                        var html = `<div class="qlvb-msg-bot">✅ ${data.message}<br/><ul class="qlvb-results">`;
                        data.results.forEach(function (item) {
                            html += `
                                <li class="qlvb-result-item">
                                    <span class="qlvb-loai">${item.loai}</span>
                                    <a href="/web#action=${item.action}&id=${item.id}&model=${item.model}&view_type=form"
                                       target="_blank" class="qlvb-result-link">${item.ten}</a>
                                    <small class="qlvb-mo-ta">${item.mo_ta}</small>
                                </li>`;
                        });
                        html += '</ul></div>';
                        $('#qlvb-chatbox-messages').append(html);
                    }
                    scrollToBottom();
                })
                .catch(function () {
                    $('#qlvb-loading').remove();
                    $('#qlvb-chatbox-messages').append(`<div class="qlvb-msg-bot">⚠️ Có lỗi xảy ra, vui lòng thử lại.</div>`);
                    scrollToBottom();
                });
        }

        $('#qlvb-chatbox-send').on('click', guiTimKiem);
        $('#qlvb-chatbox-input').on('keypress', function (e) {
            if (e.which === 13) guiTimKiem();
        });
    });
});


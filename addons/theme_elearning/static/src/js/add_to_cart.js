/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.AddToCartWidget = publicWidget.Widget.extend({
  selector: ".course-card",

  start: function () {
    this._super.apply(this, arguments);
  },

  events: {
    "click .btn-register": "_onAddToCart",
    "click .btn-installment": "_onAddToCart", // Xử lý cả nút Trả góp học phí
  },

  _onAddToCart: function (ev) {
    ev.preventDefault();

    let $btn = $(ev.currentTarget);
    let productId = $btn.closest(".course-card").data("product-id");

    if (!productId) {
      console.error("Thiếu thông tin sản phẩm.");
      return;
    }

    rpc("/cart/add", { product_id: productId, quantity: 1 })
      .then((result) => {
        if (result.status === "success") {
          window.location.href = "/thanh-toan"; // Chuyển hướng ngay sang trang thanh toán
        } else {
          console.error("Lỗi khi thêm vào giỏ hàng:", result.message);
        }
      })
      .catch((error) => console.error("Lỗi khi thêm vào giỏ hàng:", error));
  },
});

// Đăng ký widget
publicWidget.registry.AddToCartWidget = publicWidget.registry.AddToCartWidget;

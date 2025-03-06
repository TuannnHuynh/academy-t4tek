/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CartWidget = publicWidget.Widget.extend({
  selector: "#cart-container",

  start: function () {
    this._super.apply(this, arguments);
    this._fetchCart();
    console.log("Widget CartWidget đã được load");
  },

  events: {
    "click .btn-cart-delete": "_onRemoveFromCart",
  },

  // Hàm lấy danh sách giỏ hàng
  _fetchCart: function () {
    rpc("/cart/get", {}, { method: "GET" }) // Fix lỗi 405
      .then((cart) => {
        console.log("Cart Data:", cart);
        this._renderCart(cart);
      })
      .catch((err) => {
        console.error("Lỗi khi tải giỏ hàng:", err);
      });
  },

  // Hàm render giao diện giỏ hàng
  _renderCart: function (cart) {
    let $cartContainer = this.$el;
    let $receiptDetail = $(".receipt-detail");
    let cartHtml = "";

    if (cart.items.length) {
      cart.items.forEach((item) => {
        cartHtml += `
          <div class="checkout-item row" data-id="${item.product_id}">
              <div class="col-md-4 checkout-item-img">
                  <img src="/web/image/product.template/${
                    item.product_id
                  }/image_256" alt=""/>
              </div>
              <div class="col-md-8">
                  <h5>${item.product_name}</h5>
                  <div class="checkout-item-price">
                      <p class="price">Học phí: <span>${item.price_unit.toLocaleString()}đ</span></p>
                  </div>
                  <div class="checkout-item-delete">
                      <a class="btn-cart-delete" data-id="${
                        item.product_id
                      }">Xoá</a>
                  </div>
              </div>
          </div>
        `;
      });
    } else {
      cartHtml = `<p class="mt-2">Giỏ hàng của bạn đang trống.</p>`;
    }

    $cartContainer.html(cartHtml);

    // 🛠 Fix lỗi cập nhật số lượng
    let totalQuantity = cart.total_quantity || 0;
    $receiptDetail.find("p:first-child span").text(totalQuantity);

    let totalPrice = cart.total_price || 0;
    $receiptDetail
      .find("p:last-child span")
      .text(totalPrice.toLocaleString() + "đ");
  },

  _onRemoveFromCart: function (ev) {
    ev.preventDefault();
    let productId = $(ev.currentTarget).data("id");

    if (!productId) {
      console.error("Không tìm thấy ID sản phẩm để xoá.");
      return;
    }

    rpc("/cart/remove", { product_id: productId }, { method: "POST" })
      .then((result) => {
        if (result.status === "success") {
          console.log("Sản phẩm đã được xoá khỏi giỏ hàng.");

          // Gọi lại _fetchCart để cập nhật giao diện
          this._fetchCart();
        } else {
          console.error("Lỗi khi xoá sản phẩm:", result.message);
        }
      })
      .catch((err) => {
        console.error("Lỗi khi xoá sản phẩm khỏi giỏ hàng:", err);
      });
  },
});

// Đăng ký widget
publicWidget.registry.CartWidget = publicWidget.registry.CartWidget;

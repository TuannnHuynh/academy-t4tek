import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

function createSlug(text) {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, "-")
    .toLowerCase();
}

let ProductListWidget = publicWidget.Widget.extend({
  selector: "#course-short-list",

  start: function () {
    let defaultCategory = "Khoá học ngắn hạn";
    this.fetchProducts(defaultCategory);
    this.setupDropdownEvents();
  },

  fetchProducts: function (category) {
    console.log("Gửi request RPC:", {
      category_name: category || "Tất cả khoá học",
    });

    rpc("/get_products", { category_name: category || "Tất cả khoá học" })
      .then((products) => {
        console.log("Dữ liệu sản phẩm nhận được:", products);
        if (products && products.length) {
          this.renderProducts(products);
        } else {
          this.$el.html("<p>Không có sản phẩm nào.</p>");
        }
      })
      .catch((err) => {
        console.error("Lỗi khi tải sản phẩm:", err);
        this.$el.html("<p>Lỗi khi tải danh sách sản phẩm.</p>");
      });
  },

  renderProducts: function (products) {
    let productHtml = "";
    products.forEach((product) => {
      const productSlug = createSlug(product.name);
      productHtml += `
        <div class="card col-md-4">
            <div class="card-content">
                <img src="${product.image}" class="card-img-top" alt="${
        product.name
      }"/>
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">
                        Ngày khai giảng: <strong>${
                          product.opening_date || "Chưa cập nhật"
                        }</strong><br/>
                        Trình độ: <strong>${
                          product.level || "Không xác định"
                        }</strong><br/>
                        Lịch học: <strong>${
                          product.study_days || "Không xác định"
                        }</strong><br/>
                        Giờ học: <strong>${
                          product.study_time || "Không xác định"
                        }</strong><br/>
                    </p>
                    <a href="/khoa-hoc-ngan-han/${productSlug}" class="btn btn-primary">Xem chi tiết</a>
                </div>
                <div class="card-footer">
                    Ưu đãi đặc biệt!
                </div>
            </div>
        </div>
      `;
    });
    this.$el.html(productHtml);
  },

  setupDropdownEvents: function () {
    let self = this;
    let selectedCategory = "Tất cả khoá học";

    this.$el
      .closest("body")
      .find("#dropdownMenuButton1 + .dropdown-menu .dropdown-item")
      .off("click")
      .on("click", function () {
        selectedCategory = $(this).data("value");
        $("#dropdownMenuButton1").text($(this).text());
        self.fetchProducts(selectedCategory);
      });
  },
});

// Đăng ký widget
publicWidget.registry.ProductListWidget = ProductListWidget;

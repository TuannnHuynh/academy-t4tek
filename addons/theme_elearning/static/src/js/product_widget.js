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
    let path = window.location.pathname;
    let params = new URLSearchParams(window.location.search);
    let defaultCategory = "Tất cả khoá học";
    let defaultLocation = params.get("location") || "Tất cả địa điểm";

    if (path.includes("/khoa-hoc-ngan-han")) {
      defaultCategory = "Khoá ngắn hạn";
      $("#dropdownMenuButton1").text("Khoá ngắn hạn");
    } else if (path.includes("/khoa-hoc-dai-han")) {
      defaultCategory = "Khoá dài hạn";
      $("#dropdownMenuButton1").text("Khoá dài hạn");
    }

    $(".course-link li:last-child").text(defaultCategory);

    $("#dropdownMenuButton2").text(defaultLocation);

    this.fetchProducts(defaultLocation, defaultCategory);
    this.setupDropdownEvents();
  },

  fetchProducts: function (location, category) {
    console.log("Gửi request RPC:", {
      location: location || "Tất cả địa điểm",
      category_name: category || "Tất cả khoá học",
    });

    rpc("/get_products", {
      location: location,
      category_name: category,
    })
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
    console.log("Dữ liệu sản phẩm nhận được:", products);
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
                    ${product.promotion_text || "Ưu đãi đặc biệt!"}
                </div>
            </div>
        </div>
      `;
    });
    this.$el.html(productHtml);
  },

  setupDropdownEvents: function () {
    let self = this;
    let selectedCategory = $("#dropdownMenuButton1").text().trim();
    let selectedLocation =
      $("#dropdownMenuButton2").text().trim() || "Tất cả địa điểm";

    this.$el
      .closest("body")
      .find("#dropdownMenuButton1 + .dropdown-menu .dropdown-item")
      .off("click")
      .on("click", function () {
        selectedCategory = $(this).data("value");
        $("#dropdownMenuButton1").text($(this).text());
        $(".course-link li:last-child").text(selectedCategory);
        self.fetchProducts(selectedLocation, selectedCategory);
      });

    // Lọc theo địa điểm
    this.$el
      .closest("body")
      .find("#dropdownMenuButton2 + .dropdown-menu .dropdown-item")
      .off("click")
      .on("click", function () {
        selectedLocation = $(this).data("value");
        $("#dropdownMenuButton2").text($(this).text());
        self.fetchProducts(selectedLocation, selectedCategory);
      });
  },
});

// Đăng ký widget
publicWidget.registry.ProductListWidget = ProductListWidget;

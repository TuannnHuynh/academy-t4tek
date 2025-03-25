odoo.define("website.banner", function (require) {
  "use strict";

  var publicWidget = require("web.public.widget");

  publicWidget.registry.BannerWidget = publicWidget.Widget.extend({
    selector: "#test_page_template",
    start: function () {
      var self = this;
      this._rpc({
        route: "/get_banners",
        params: {},
      }).then(function (banners) {
        self.renderBanners(banners);
      });
    },
    renderBanners: function (banners) {
      var container = this.$el;
      container.empty(); // Xóa nội dung cũ
      banners.forEach(function (banner, index) {
        if (banner.image) {
          var bannerHTML = `
                        <div class="banner-${index + 1}">
                            <div class="row m-0">
                                <img class="col-12 col-md-6 p-0" src="${
                                  banner.image
                                }" alt=""/>
                                <div class="banner-item col-12 py-4 py-md-0 col-md-6 p-0">
                                    <div class="content">
                                        <h2>${banner.title}</h2>
                                        <p>${banner.content}</p>
                                        <button class="btn-animate">Xem chi tiết</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
          container.append(bannerHTML);
        }
      });
    },
  });

  return publicWidget.registry.BannerWidget;
});

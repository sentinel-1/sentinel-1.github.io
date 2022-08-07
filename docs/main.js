$(function () {



  var OGPArticle = Backbone.Model.extend({

    defaults: function () {
      return {
        og_title: "Empty OGP Article..."
      };
    },
    parse: function (response, options) {
      response.article_published_time = new Date(response.article_published_time);
      response.article_modified_time = new Date(response.article_modified_time);
      return response;
    },
  });



  var OGPArticleList = Backbone.Collection.extend({

    model: OGPArticle,
    url: 'ogp.json',
    comparator: (A, B) => {
      if (A.get("article_published_time") > B.get("article_published_time")) {
        return -1;
      }
      if (A.get("article_published_time") == B.get("article_published_time")) {
        return 0;
      }
      return 1;
    },
  });


  var OGPArticles = new OGPArticleList;



  var OGPArticleView = Backbone.View.extend({

    tagName: "tr",
    template: _.template($('#item-template').html()),
    initialize: function () {},

    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },

  });



  var AppView = Backbone.View.extend({
    el: $("#OGP-shared-articles"),
    initialize: function () {
      // this.listenTo(OGPArticles, 'add', this.addOne);
      this.listenTo(OGPArticles, 'reset', this.addAll);
      // this.listenTo(OGPArticles, 'all', this.render);
      OGPArticles.fetch({ reset: true });
    },

    render: function () {},

    addOne: function (todo) {
      var view = new OGPArticleView({ model: todo });
      this.$("#OGP-article-list").append(view.render().el);
    },

    addAll: function () {
      OGPArticles.each(this.addOne, this);
    },
  });


  // Kick things off by creating the **App**.
  var App = new AppView;

});

// Backbone Application View: Course Learning Information

define([ // jshint ignore:line
    'jquery',
    'underscore',
    'backbone',
    'gettext',
    'js/utils/templates'
],
function ($, _, Backbone, gettext, TemplateUtils) {
    'use strict';
    var LearningInfoView = Backbone.View.extend({

        events: {
            'click .delete-course-learning-info': "removeLearningInfo"
        },

        initialize: function(options) {
            // Set up the initial state of the attributes set for this model instance
             _.bindAll(this, 'render');
            this.template = this.loadTemplate('course-settings-learning-fields');
            this.model = options.model;
        },

        loadTemplate: function(name) {
            // Retrieve the corresponding template for this model
            return TemplateUtils.loadTemplate(name);
        },

        render: function() {
             // rendering for this model
            $("li.course-settings-learning-fields").empty();
            var self = this;
            $.each(this.model.get('learning_info'), function( index, info ) {
                $(self.el).append(self.template({index: index, info: info}));
            });
        },

        removeLearningInfo: function(event) {
            /*
            * Remove course learning fields.
            * */
            event.preventDefault();
            var index = event.currentTarget.getAttribute('data-index'),
                existing_info = _.clone(this.model.get('learning_info'));
            existing_info.splice(index, 1);
            this.model.set('learning_info', existing_info);
            this.render();
        }

    });
    return LearningInfoView;
});

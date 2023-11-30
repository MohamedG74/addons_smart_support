odoo.define('smart_custom_report.trial_balance_sub', function(require) {
    'use strict';
     var AbstractAction = require("web.AbstractAction");
     var core = require("web.core");
    var rpc = require('web.rpc');
     var _t = core._t;
    var QWeb = core.qweb;
    var datepicker = require("web.datepicker");
    var time = require('web.time');
     var framework = require('web.framework');
     var session = require('web.session');
    var TrialBalanceSub = AbstractAction.extend({
       template: 'TrialBalanceSub',
       events: {
          'click #apply_filter': 'apply_filter',
          'click #xlsx': 'print_pdf',
          'click .view_purchase_order': 'button_view_order',
          'mousedown div.input-group.date': '_onCalendarIconClick',
       },
  
  init: function(parent, action) {
          this._super(parent, action);
          this.report_lines = action.report_lines;
          this.wizard_id = action.context.wizard | null;
       },
  
  
  start: function() {
   $("head").append("<link href='/smart_custom_report/static/src/css/main.css' type='text/css' rel='stylesheet' />");
    var self = this;
    self.initial_render = true;
    rpc.query({
       model: 'dynamic.trial.balance.sub',
       method: 'create',
       args: [{
       }]
    }).then(function(res) {
       self.wizard_id = res;
       console.log('res',res);
       self.load_data(self.initial_render);
       console.log('self',self.initial_render);
    })
  },
  _onCalendarIconClick: function(ev) {
    var $calendarInputGroup = $(ev.currentTarget);
    var calendarOptions = {
       minDate: moment({
          y: 1000
       }),
       maxDate: moment().add(200, 'y'),
       calendarWeeks: true,
       //defaultDate: moment().format(),
       sideBySide: true,
       buttons: {
          showClear: true,
          showClose: true,
          showToday: true,
       },
       icons: {
          date: 'fa fa-calendar',
       },
       //locale: moment.locale('fr'),
       //format: time.getLangDateFormat(),
       widgetParent: 'body',
       allowInputToggle: true,
       constrainInput: false ,
       locale:'en',
       format: 'DD-MM-YYYY',
    };
    $calendarInputGroup.datetimepicker(calendarOptions);
  },
  load_data: function(initial_render = true) {
          var self = this;
          self._rpc({
             model: 'dynamic.trial.balance.sub',
             method: 'purchase_report',
             args: [
                [this.wizard_id]
             ],
          }).then(function(datas) {
            if (datas['orders']){
               self.$('.table_view_pr').html(QWeb.render('TrialBalanceSubOrderTable', {
                  filter: datas['filters'],
                  order: datas['orders'],
                  report_lines: datas['report_lines'],
                  report_lines_previous: datas['previous'],
                  main_lines: datas['report_main_line']
               }));
           }


             if (initial_render) {
                self.$('.filter_view_pr').html(QWeb.render('TrialBalanceSubFilterView', {
                   filter_data: datas['filters'],
                }));
               //  self.$el.find('.report_type').select2({
               //     placeholder: ' Report Type...',
               //  });
             



            if(datas['accounts']){
               $('.account_name').select2('destroy'); 
               var elms = "<option value=''></option>";
               datas['accounts'].forEach(item => {
                  elms = elms + "<option value='"+item.code+"'>"+item.code+" - "+item.name+"</option>";            
                });
                console.log(elms);
               $('#selection_account_name').html(elms);
               $('.account_name').select2({
                  placeholder: ' Accounts...',
               });
             }



             $('.level').select2('destroy'); 
             $('.level').select2({
               placeholder: ' المستوي...',
            });


         }

            setTimeout(() => {
               let x = document.querySelectorAll(".currency");
               for (let i = 0, len = x.length; i < len; i++) {
                 let num = Number(x[i].innerHTML).toLocaleString('en');
                 x[i].innerHTML = num;
                 //x[i].classList.add("currSign");
               }
             }, 2000);
             //adjust the table pagination
         //     $('table.paginated').each(function () {
         //       var currentPage = 0;
         //       var numPerPage = 200; // number of items 
         //       var $table = $(this);
         //       //var $tableBd = $(this).find("tbody");
       
         //       $table.bind('repaginate', function () {
         //           $table.find('tbody tr').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
         //       });
         //       $table.trigger('repaginate');
         //       var numRows = $table.find('tbody tr').length;
         //       var numPages = Math.ceil(numRows / numPerPage);
         //       var $pager = $('<div class="pager"></div>');
         //       for (var page = 0; page < numPages; page++) {
         //           $('<span class="page-number"></span>').text(page + 1).bind('click', {
         //               newPage: page
         //           }, function (event) {
         //               currentPage = event.data['newPage'];
         //               $table.trigger('repaginate');
         //               $(this).addClass('active').siblings().removeClass('active');
         //           }).appendTo($pager).addClass('clickable');
         //       }
         //       if (numRows > numPerPage) {
         //           $pager.insertAfter($table).find('span.page-number:first').addClass('active');
         //       }
         //   });



         $('table.paginated').each(function () {
            var currentPage = 0;
            var numPerPage = 25; // number of items 
            var $table = $(this);
            var $tableBd = $(this).find("tbody");
        
            $table.bind('repaginate', function () {
                var startIndex = currentPage * numPerPage;
                var endIndex = startIndex + numPerPage;
                $tableBd.find('tr').hide().slice(startIndex, endIndex).show();
            });
            $table.trigger('repaginate');
            var numRows = $tableBd.find('tr').length;
            var numPages = Math.ceil(numRows / numPerPage);
            var $pager = $('<div class="pager"></div>');
        
            // First page button
            $('<span class="page-link">First</span>').bind('click', function () {
                if (currentPage !== 0) {
                    currentPage = 0;
                    $table.trigger('repaginate');
                    updatePager();
                }
            }).appendTo($pager).addClass('clickable');
      
   
            // Previous button
            $('<span class="page-link">&laquo; Previous</span>').bind('click', function () {
                if (currentPage > 0) {
                    currentPage--;
                    $table.trigger('repaginate');
                    updatePager();
                }
            }).appendTo($pager).addClass('clickable');
      
   
            // Current page number
            $('<span class="page-number"></span>').text(currentPage + 1).addClass('active').appendTo($pager);
      
   
            // Next button
            $('<span class="page-link">Next &raquo;</span>').bind('click', function () {
                if (currentPage < numPages - 1) {
                    currentPage++;
                    $table.trigger('repaginate');
                    updatePager();
                }
            }).appendTo($pager).addClass('clickable');
      
   
            // Last page button
            $('<span class="page-link">Last</span>').bind('click', function () {
                if (currentPage !== numPages - 1) {
                    currentPage = numPages - 1;
                    $table.trigger('repaginate');
                    updatePager();
                }
            }).appendTo($pager).addClass('clickable').append($('<span class="last-page-number"> &nbsp; [' + numPages + ']</span>'));
   
            
            // Input box for entering desired page number
            var $pageNumberInput = $('<input type="number" class="page-number-input" placeholder="Page No." min="1" max="' + numPages + '">')
            .appendTo($pager)
            .on('keyup', function () {
               var pageNumber = parseInt($(this).val()) - 1;
               if (!isNaN(pageNumber) && pageNumber >= 0 && pageNumber < numPages) {
                  currentPage = pageNumber;
                  $table.trigger('repaginate');
                  updatePager();
               }
            });
        
            function updatePager() {
                $pager.find('.page-number').text(currentPage + 1);
               //  $pageNumberInput.val(currentPage + 1);
            }
        
            if (numRows > numPerPage) {
                $pager.insertAfter($table);
                updatePager();
            }
        });
          })
       },
      
   print_pdf: function(e) {
          e.preventDefault();

          return $("#table2excel").table2excel({
              // exclude CSS class
              exclude: ".noExl",
              name: "ميزان المراجعة الفرعى",
              filename: "ميزان المراجعة الفرعى", //do not include extension
              fileext: ".xlsx" // file extension
            }); 
        
       },
       button_view_order: function(event) {
          event.preventDefault();
          var self = this;
          var context = {};
          this.do_action({
             name: _t("Purchase Order"),
             type: 'ir.actions.act_window',
             res_model: 'purchase.order',
             view_type: 'form',
             domain: [
                ['id', '=', $(event.target).closest('.view_purchase_order').attr('id')]
             ],
             views: [
               
   [false, 'list'],
                [false, 'form']
             ],
             target: 'current'
          });
       },
       //
       apply_filter: function() {
          var self = this;
          self.initial_render = false;
          var filter_data_selected = {};
          if (this.$el.find('.datetimepicker-input[name="date_from"]').val()) {
             filter_data_selected.date_from = moment(this.$el.find('.datetimepicker-input[name="date_from"]').val(), "DD-MM-YYYY").locale('en').format('YYYY-MM-DD');
          }
          if (this.$el.find('.datetimepicker-input[name="date_to"]').val()) {
             filter_data_selected.date_to = moment(this.$el.find('.datetimepicker-input[name="date_to"]').val(), "DD-MM-YYYY").locale('en').format('YYYY-MM-DD');
          }
         //  if ($(".report_type").length) {
         //     console.log()
         //     var report_res = document.getElementById("report_res")
         //     filter_data_selected.report_type = $(".report_type")[1].value
         //     report_res.value = $(".report_type")[1].value
         //     report_res.innerHTML = report_res.value.replaceAll('_', ' ');
         //     if ($(".report_type")[1].value == "") {
         //        report_res.innerHTML = "report_by_order";
         //     }
         //  }
         

          if ($(".account_name").length) {
            //var report_res = document.getElementById("report_res_account_name");
            //report_res.value =  $(".account_name option:selected").val();
            //report_res.innerHTML =  $(".account_name option:selected").text();
            $(".report_code").val($(".account_name option:selected").val());
           // if ($(".account_name option:selected").val() == "") {
           //    report_res.innerHTML = "None";
            //}
         }


         if ($(".level").length) {
            //var report_res = document.getElementById("report_res_level");
            //report_res.value =  $(".level option:selected").val();
            //report_res.innerHTML =  $(".level option:selected").text();
            filter_data_selected.level = $(".level option:selected").val();
            //if ($(".level option:selected").val() == "") {
            //   report_res.innerHTML = "None";
            //}
         }


         if ($(".report_code").val().length > 0) {
            var report_res = $(".report_code").val();
            filter_data_selected.report_code = report_res;
         }

          rpc.query({
             model: 'dynamic.trial.balance.sub',
            method: 'write',
             args: [
                self.wizard_id, filter_data_selected
             ],
          }).then(function(res) {
             self.initial_render = false;
             self.load_data(self.initial_render);
          });
       },
    });
    
  core.action_registry.add("t_b_s", TrialBalanceSub);
    return TrialBalanceSub;
  });
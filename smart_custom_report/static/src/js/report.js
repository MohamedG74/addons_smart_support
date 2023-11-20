odoo.define('smart_custom_report.purchase_report', function(require) {
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
   var PurchaseReport = AbstractAction.extend({
      template: 'PurchaseReport',
      events: {
         'click #apply_filter': 'apply_filter',
         'click #xlsx': 'print_pdf',
         'click #groupButton': 'groupButton',
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
      model: 'dynamic.purchase.report',
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
            model: 'dynamic.purchase.report',
            method: 'purchase_report',
            args: [
               [this.wizard_id]
            ],
         }).then(function(datas) {

           if (datas['orders']){
              self.$('.table_view_pr').html(QWeb.render('PurchaseOrderTable', {
                 filter: datas['filters'],
                 order: datas['orders'],
                 report_lines: datas['report_lines'],
                 main_lines: datas['report_main_line']
              }));
          }

            if (initial_render) {
               self.$('.filter_view_pr').html(QWeb.render('PurchaseFilterView', {
                  filter_data: datas['filters'],
               }));
              //  self.$el.find('.report_type').select2({
              //     placeholder: ' Report Type...',
              //  });
            
            
           if(datas['locations']){
              $('.report_location').select2('destroy'); 
              var elms = "";
              elms = elms + "<option value='all'>Empty</option>"; 
              datas['locations'].forEach(item => {
                 elms = elms + "<option value='"+item.id+"'>"+item.name+"</option>";            
               });
               console.log(elms);
              $('#selectionw').html(elms);
              $('.report_location').select2({
                 placeholder: ' Location...',
              });
            }

            if(datas['products']){
              $('.report_product').select2('destroy'); 
              var elms = "";
              elms = elms + "<option value='all'>All</option>"; 
              datas['products'].forEach(item => {
                 elms = elms + "<option value='"+item.id+"'>"+item.default_code+" - "+item.name+"</option>";            
               });
               console.log(elms);
              $('#selectionproduct').html(elms);
              $('.report_product').select2({
                 placeholder: ' Product...',
              });
            }

            if(datas['groups']){
              $('.main_group').select2('destroy'); 
              var elms = "";
              elms = elms + "<option value='all'>All</option>"; 
              datas['groups'].forEach(item => {
                 elms = elms + "<option value='"+item.name+"'>"+item.name+"</option>";            
               });
               console.log(elms);
              $('#selection_main_group').html(elms);
              $('.main_group').select2({
                 placeholder: ' Main Group...',
              });
              

              
              $('.second_group').select2('destroy'); 
              var elms = "";
              elms = elms + "<option value='all'>All</option>"; 
              datas['groups'].forEach(item => {
                 elms = elms + "<option value='"+item.namear+"'>"+item.namear+"</option>";            
               });
               console.log(elms);
              $('#selection_second_group').html(elms);
              $('.second_group').select2({
                 placeholder: 'Second Group...',
              });
            }

           }
            //adjust the table pagination
        //     $('table.paginated').each(function () {
        //       var currentPage = 0;
        //       var numPerPage = 25; // number of items 
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


  //    $('table.paginated').each(function () {
  //       var currentPage = 0;
  //       var numPerPage = 25; // number of items 
  //       var $table = $(this);
  //       var $tableBd = $(this).find("tbody");
    
  //       $table.bind('repaginate', function () {
  //           var startIndex = currentPage * numPerPage;
  //           var endIndex = startIndex + numPerPage;
  //           $tableBd.find('tr').hide().slice(startIndex, endIndex).show();
  //       });
  //       $table.trigger('repaginate');
  //       var numRows = $tableBd.find('tr').length;
  //       var numPages = Math.ceil(numRows / numPerPage);
  //       var $pager = $('<div class="pager"></div>');
    
  //       // First page button
  //       $('<span class="page-link">First</span>').bind('click', function () {
  //           if (currentPage !== 0) {
  //               currentPage = 0;
  //               $table.trigger('repaginate');
  //               updatePager();
  //           }
  //       }).appendTo($pager).addClass('clickable');
  

  //       // Previous button
  //       $('<span class="page-link">&laquo; Previous</span>').bind('click', function () {
  //           if (currentPage > 0) {
  //               currentPage--;
  //               $table.trigger('repaginate');
  //               updatePager();
  //           }
  //       }).appendTo($pager).addClass('clickable');
  

  //       // Current page number
  //       $('<span class="page-number"></span>').text(currentPage + 1).addClass('active').appendTo($pager);
  

  //       // Next button
  //       $('<span class="page-link">Next &raquo;</span>').bind('click', function () {
  //           if (currentPage < numPages - 1) {
  //               currentPage++;
  //               $table.trigger('repaginate');
  //               updatePager();
  //           }
  //       }).appendTo($pager).addClass('clickable');
  

  //       // Last page button
  //       $('<span class="page-link">Last</span>').bind('click', function () {
  //           if (currentPage !== numPages - 1) {
  //               currentPage = numPages - 1;
  //               $table.trigger('repaginate');
  //               updatePager();
  //           }
  //       }).appendTo($pager).addClass('clickable');


  //       // Input box for entering desired page number
  //       var $pageNumberInput = $('<input type="number" class="page-number-input" min="1" max="' + numPages + '">')
  //       .appendTo($pager)
  //       .on('keyup', function () {
  //          var pageNumber = parseInt($(this).val()) - 1;
  //          if (!isNaN(pageNumber) && pageNumber >= 0 && pageNumber < numPages) {
  //             currentPage = pageNumber;
  //             $table.trigger('repaginate');
  //             updatePager();
  //          }
  //       });
    
  //       function updatePager() {
  //           $pager.find('.page-number').text(currentPage + 1);
  //       }
    
  //       if (numRows > numPerPage) {
  //           $pager.insertAfter($table);
  //           updatePager();
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


      groupButton: function (event) {
        event.preventDefault();
        
        const obj = document.querySelector('#groupFields')
        obj.onchange = _=> {
           obj.insertBefore(obj.options[obj.selectedIndex], obj[0])
        };

        // Create an array to store the selected fields
        var selectedFields = [];
        
        // Get the select element
        var selectElement = document.getElementById("groupFields");
        
        // Loop through the options to find the selected ones
        for (var i = 0; i < selectElement.options.length; i++) {
           if (selectElement.options[i].selected) {
                 selectedFields.push(selectElement.options[i].value);
           }
        }
        var table;
        // var selectedField = document.getElementById("groupFields").value;

        if (!table) {
            // Initialize the table if it hasn't been initialized yet
            table = new Tabulator("#table2excel", {
              //   height: "800px",
              columnCalcs:"table ",
              groupClosedShowCalcs:true,
              maxHeight:"100%",
              //   layout: "fitColumns",
              //   resizableRows:true,
              //   layout:"fitData",
              layout:"fitDataFill",
              movableRows: true,
                columns: [
                    { title: "اسم الصنف", field: "product_name", widthGrow:1 },
                    { title: "المجموعة الفرعية", field: "category_name", widthGrow:1 },
                    { title: "المجموعة الرئيسية", field: "parent_name", widthGrow:1 },

                    { title: "رصيد اول المدة", field: "opening_stock", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                    { title: "أذون إضافة", field: "incoming_from_vendors", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                    { title: "مرتجع المشتريات", field: "outgoing_returned_to_vendors", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                    { title: "مترجع العملاء", field: "incoming_from_customers", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                    { title: "أذون تحويل اليه", field: "incoming_internal", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                    { title: "أذون صرف", field: "outgoing_to_customers", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                    { title: "أذون تحويل منه", field: "outgoing_internal", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                    // { title: "رصيد نهاية المدة", field: "price_subtotal", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                ],
            });
        }
  
        // Check if any fields are selected for grouping
        if (selectedFields.length > 0) {
           // Group the table by the selected fields
           table.setGroupBy(selectedFields);
           }
    },





     
  print_pdf: function(e) {
         e.preventDefault();

         return $("#table2excel").table2excel({
             // exclude CSS class
             exclude: ".noExl",
             name: "تقرير المخزون خلال فترة",
             filename: "Warehouse Analysis Report", //do not include extension
             fileext: ".xlsx" // file extension
           }); 
         var self = this;
         var action_title = self._title;
         self._rpc({
            model: 'dynamic.purchase.report',
            method: 'purchase_report',
            args: [
               [self.wizard_id]
            ],
         }).then(function(data) {
            var action = {
               'type': 'ir.actions.report',
               'report_type': 'qweb-pdf',
               'report_name': 'smart_custom_report.purchase_order_report',
               'report_file': 'smart_custom_report.purchase_order_report',
               'data': {
                  'report_data': data
               },
               'context': {
                  'active_model': 'purchase.report',
                  'landscape': 1,
                  'purchase_order_report': true
               },
               'display_name': 'Purchase Order',
            };
            return self.do_action(action);
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
            var selectedDateTo = moment(this.$el.find('.datetimepicker-input[name="date_to"]').val(), "DD-MM-YYYY").locale('en').format('YYYY-MM-DD');
            if (moment(selectedDateTo).isAfter("2023-10-20")) {
               alert("You should enter a date on or before 20-10-2023");
               return;
            }
            filter_data_selected.date_to = selectedDateTo;
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
         if ($(".report_location").length) {
           //  var report_res = document.getElementById("report_res_location");
            filter_data_selected.report_location = $(".report_location option:selected").val();
           //  report_res.value =  $(".report_location option:selected").val();
           //  report_res.innerHTML =  $(".report_location option:selected").text();
           //  if ($(".report_location option:selected").val() == "") {
           //     report_res.innerHTML = "None";
           //  }
         }

         if ($(".report_product").length) {
           // var report_res = document.getElementById("report_res_product");
           filter_data_selected.report_product = $(".report_product option:selected").val();
           // report_res.value =  $(".report_product option:selected").val();
           // report_res.innerHTML =  $(".report_product option:selected").text();
           // if ($(".report_product option:selected").val() == "") {
           //    report_res.innerHTML = "None";
           // }
        }

        if ($(".main_group").length) {
           // var report_res = document.getElementById("report_res_main_group");
           filter_data_selected.main_group = $(".main_group option:selected").val();
           filter_data_selected.second_group = $(".second_group option:selected").val();
           // report_res.value =  $(".main_group option:selected").val();
           // report_res.innerHTML =  $(".main_group option:selected").text();
           // if ($(".main_group option:selected").val() == "") {
           //    report_res.innerHTML = "None";
           // }
        }
        
         rpc.query({
            model: 'dynamic.purchase.report',
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
   
 core.action_registry.add("p_r", PurchaseReport);
   return PurchaseReport;
 });
odoo.define('smart_custom_report.sales_invoice_return', function(require) {
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
    var SalesInvoiceReturn = AbstractAction.extend({
       template: 'SalesInvoiceReturn',
       events: {
          'click #apply_filter': 'apply_filter',
          'click #groupingxlsx': 'download-xlsx',
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
   $("head").append("<link href='/smart_custom_report/static/src/css/tabulator.css' type='text/css' rel='stylesheet'/>");
   
    var self = this;
    self.initial_render = true;
    rpc.query({
       model: 'dynamic.sales.invoice.return',
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
             model: 'dynamic.sales.invoice.return',
             method: 'purchase_report',
             args: [
                [this.wizard_id]
             ],
          }).then(function(datas) {
            if (datas['orders']){
               self.$('.table_view_pr').html(QWeb.render('SalesInvoiceReturnOrderTable', {
                  filter: datas['filters'],
                  order: datas['orders'],
                  report_lines: datas['report_lines'],
                  main_lines: datas['report_main_line']
               }));
           }

             if (initial_render) {
                self.$('.filter_view_pr').html(QWeb.render('SalesInvoiceReturnFilterView', {
                   filter_data: datas['filters'],
                }));
               //  self.$el.find('.report_type').select2({
               //     placeholder: ' Report Type...',
               //  });
             
             
            // if(datas['locations']){
            //    $('.report_location').select2('destroy'); 
            //    var elms = "";
            //    datas['locations'].forEach(item => {
            //       elms = elms + "<option value='"+item.id+"'>"+item.name+"</option>";            
            //     });
            //     console.log(elms);
            //    $('#selectionw').html(elms);
            //    $('.report_location').select2({
            //       placeholder: ' Location...',
            //    });
            //  }

            //  if(datas['products']){
            //    $('.report_product').select2('destroy'); 
            //    var elms = "";
            //    elms = elms + "<option value='all'>All</option>"; 
            //    datas['products'].forEach(item => {
            //       elms = elms + "<option value='"+item.id+"'>"+item.default_code+" - "+item.name+"</option>";            
            //     });
            //     console.log(elms);
            //    $('#selectionproduct').html(elms);
            //    $('.report_product').select2({
            //       placeholder: ' Product...',
            //    });
            //  }
            
             $('.invoice_type').select2('destroy'); 
             $('.invoice_type').select2({
               placeholder: ' Invoice type...',
            });


             if(datas['branch']){
               $('.report_location').select2('destroy'); 
               var elms = "";
               elms = elms + "<option value='all'>All</option>"; 
               datas['branch'].forEach(item => {
                  elms = elms + "<option value='"+item.name+"'>"+item.name+"</option>";            
                });
                console.log(elms);
               $('#selection_branch').html(elms);
               $('.report_location').select2({
                  placeholder: ' Branch...',
               });
             }



             if(datas['user']){
               $('.res_user').select2('destroy'); 
               var elms = "";
               elms = elms + "<option value='all'>All</option>"; 
               datas['user'].forEach(item => {
                  elms = elms + "<option value='"+item.name+"'>"+item.name+"</option>";            
                });
                console.log(elms);
               $('#selection_res_user').html(elms);
               $('.res_user').select2({
                  placeholder: ' User...',
               });
             }


             if(datas['partner']){
               $('.res_partner').select2('destroy'); 
               var elms = "";
               elms = elms + "<option value='all'>All</option>"; 
               datas['partner'].forEach(item => {
                  elms = elms + "<option value='"+item.name+"'>"+item.name+"</option>";            
                });
                console.log(elms);
               $('#selection_res_partner').html(elms);
               $('.res_partner').select2({
                  placeholder: ' Partner...',
               });
             }


             if(datas['employee']){
               $('.hr_employee').select2('destroy'); 
               var elms = "";
               elms = elms + "<option value='all'>All</option>"; 
               datas['employee'].forEach(item => {
                  elms = elms + "<option value='"+item.name+"'>"+item.name+"</option>";            
                });
                console.log(elms);
               $('#selection_hr_employee').html(elms);
               $('.hr_employee').select2({
                  placeholder: ' Employee...',
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

      // old_paginted

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
      //       }).appendTo($pager).addClass('clickable').append($('<span class="last-page-number"> &nbsp; [' + numPages + ']</span>'));
      
            
      //       // Input box for entering desired page number
      //       var $pageNumberInput = $('<input type="number" class="page-number-input" placeholder="Page No." min="1" max="' + numPages + '">')
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
      //          //  $pageNumberInput.val(currentPage + 1);
      //       }
        
      //       if (numRows > numPerPage) {
      //           $pager.insertAfter($table);
      //           updatePager();
      //       }
      //   });

         var numPerPage = datas['limited'];
         if (isNaN(numPerPage)){
            numPerPage = 25;
         }

         var number_of_pages = Math.ceil(parseInt(datas['count'].total_rows) / numPerPage);
         var numPages = Math.ceil(number_of_pages);
         var currentPage = Math.ceil(parseInt($(".pgnum").val() / numPerPage));
         
         var $pager = $('<div class="pager"></div>');


         var total_rows = parseInt(datas['count'].total_rows)
         var buttonElement = '<button type="button" class="btn btn-secondary" disabled style="font-size: 14px; color: #000; font-weight: bold;">عدد الصفوف الكلي: ' + total_rows + '</button>';
         $('#totalRowCount').html(buttonElement);

         
         // First page button
         $('<span class="page-link">First</span>').bind('click', function () {
             if (currentPage !== 0) {
                 currentPage = 0;
                 $(".pgnum").val(currentPage);
                 updatePager();
                 $("#apply_filter").click();
             }
         }).appendTo($pager).addClass('clickable');
         
         // Previous button
         $('<span class="page-link">&laquo; Previous</span>').bind('click', function () {
             if (currentPage > 0) {
                 currentPage--;
                 $(".pgnum").val(currentPage*numPerPage);
                 updatePager();
                 $("#apply_filter").click();
             }
         }).appendTo($pager).addClass('clickable');
         
         // Current page number
         $('<span class="page-number"></span>').text(currentPage + 1).addClass('active').appendTo($pager);
         
         // Next button
         $('<span class="page-link">Next &raquo;</span>').bind('click', function () {
             if (currentPage < numPages - 1) {
                 currentPage++;
                 $(".pgnum").val(currentPage*numPerPage);
                 updatePager();
                 $("#apply_filter").click();
             }
         }).appendTo($pager).addClass('clickable');
         
         // Last page button with number in square brackets
         $('<span class="page-link">Last</span>').bind('click', function () {
             if (currentPage !== numPages - 1) {
                 currentPage = numPages - 1;
                 $(".pgnum").val(currentPage*numPerPage);
                 updatePager();
                 $("#apply_filter").click();
             }
         }).appendTo($pager).addClass('clickable').append($('<span class="last-page-number">[' + numPages + ']</span>'));
         
         // Input box for entering desired page number
         var $pageNumberInput = $('<input type="number" class="pgnum" placeholder="Page No." min="1" max="' + numPages + '">')
             .appendTo($pager)
             .on('keyup', function () {
                 var pageNumber = parseInt($(this).val()) - 1;
                 if (!isNaN(pageNumber) && pageNumber >= 0 && pageNumber < numPages) {
                     currentPage = pageNumber;
                     $(".pgnum").val(currentPage*numPerPage);
                     updatePager();
                     $("#apply_filter").click();
                 }
             });
         
         function updatePager() {
             $pager.find('.page-number').text(currentPage + 1);
             $pageNumberInput.val(currentPage + 1);            
         }
         
         if (numPages >= 1) {
            $(".pager").empty();
            $pager.appendTo('body');
            updatePager();

         }


          })
       },




      groupButton: function (event) {
      // event.preventDefault();

         const objSelect = document.getElementById('groupFields')
               objSelect.onchange =_=>
               {
               let
                  optSelected = objSelect.querySelector(`option[value="${objSelect.value}"]`)
               , optFirst    = objSelect.querySelector(`option`)
                  ;
               objSelect.insertBefore( optSelected, optFirst )
               }


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
            columnCalcs:"table ",
            groupClosedShowCalcs:true,
            maxHeight:"100%",
            layout:"fitDataStretch",
            groupStartOpen:false,
            movableRows: true,
               columns: [
                  { title: "رقم الفاتورة", field: "invoice_number", widthGrow:1 },
                  { title: "نوع الفاتورة", field: "invoice_type", widthGrow:1 },
                  { title: "تاريخ الفاتورة", field: "invoice_date", widthGrow:1 },
                  { title: "الفرع", field: "report_location", widthGrow:1 },
                  { title: "البائع", field: "user_name", widthGrow:1 },
                  { title: "مندوب المبيعات", field: "employee_name", widthGrow:1 },
                  { title: "اسم العميل", field: "partner_name", widthGrow:1 },

                  { title: "قيمة الخصم", field: "stot_disc", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,} },
                  { title: "الصافي", field: "amount_untaxed", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                  { title: "الضريبة", field: "amount_tax", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                  { title: "الصافي مع الضريبة", field: "amount_total", widthGrow:1,  bottomCalc:"sum", bottomCalcParams:{precision:3,}},
                  
               ],
            });
            
      }
      // Check if any fields are selected for grouping
      if (selectedFields.length > 0) {
         // Group the table by the selected fields
         table.setGroupBy(selectedFields);
      }

         var exportButton = document.getElementById("download-xlsx");
         exportButton.addEventListener("click", function downloadOnce() {
            table.download("xlsx", "تقرير فواتير و مرتجعات المبيعات.xlsx", {sheetName: "Item Sales Returns"});
            
            // Remove the event listener after the first click
            exportButton.removeEventListener("click", downloadOnce);
         });

   },
        
      
   print_pdf: function(e) {
          e.preventDefault();

          return $("#table2excel").table2excel({
              // exclude CSS class
              exclude: ".noExl",
              name: "تقرير فواتير و مرتجعات المبيعات",
              filename: "Sales Invoices Returns", //do not include extension
              fileext: ".xlsx" // file extension
            }); 
          var self = this;
          var action_title = self._title;
          self._rpc({
             model: 'dynamic.sales.invoice.return',
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
          if ($(".report_location").length) {
            //  var report_res = document.getElementById("report_res_location");
             filter_data_selected.report_location = $(".report_location option:selected").val();
            //  report_res.value =  $(".report_location option:selected").val();
            //  report_res.innerHTML =  $(".report_location option:selected").text();
            //  if ($(".report_location option:selected").val() == "") {
            //     report_res.innerHTML = "None";
            //  }
          }

         filter_data_selected.counting = $(".pgnum").val();
         //  if ($(".report_product").length) {
         //    var report_res = document.getElementById("report_res_product");
         //    filter_data_selected.report_product = $(".report_product option:selected").val();
         //    report_res.value =  $(".report_product option:selected").val();
         //    report_res.innerHTML =  $(".report_product option:selected").text();
         //    if ($(".report_product option:selected").val() == "") {
         //       report_res.innerHTML = "None";
         //    }
         // }




         if ($(".invoice_type").length) {
            // var report_res = document.getElementById("report_res_invoice_type");
            filter_data_selected.invoice_type = $(".invoice_type option:selected").val();
            // report_res.value =  $(".invoice_type option:selected").val();
            // report_res.innerHTML =  $(".invoice_type option:selected").text();
            // if ($(".invoice_type option:selected").val() == "") {
            //    report_res.innerHTML = "None";
            // }
         }


         if ($(".invoice_number").val().length > 0) {
            var report_res = $(".invoice_number").val();
            filter_data_selected.invoice_number = report_res;
         }else{
            filter_data_selected.invoice_number = "all";
         }

         if ($(".limited").val().length > 0) {
            var report_res = $(".limited").val();
            filter_data_selected.limited = report_res;
         }else{
            filter_data_selected.limited = "all";
         }



         if ($(".res_user").length) {
            // var report_res = document.getElementById("report_res_res_user");
            filter_data_selected.res_user = $(".res_user option:selected").val();
            // report_res.value =  $(".res_user option:selected").val();
            // report_res.innerHTML =  $(".res_user option:selected").text();
            // if ($(".res_user option:selected").val() == "") {
            //    report_res.innerHTML = "None";
            // }
         }



         if ($(".res_partner").length) {
            // var report_res = document.getElementById("report_res_res_partner");
            filter_data_selected.res_partner = $(".res_partner option:selected").val();
            // report_res.value =  $(".res_partner option:selected").val();
            // report_res.innerHTML =  $(".res_partner option:selected").text();
            // if ($(".res_partner option:selected").val() == "") {
            //    report_res.innerHTML = "None";
            // }
         }

         if ($(".hr_employee").length) {
            // var report_res = document.getElementById("report_res_hr_employee");
            filter_data_selected.hr_employee = $(".hr_employee option:selected").val();
            // report_res.value =  $(".hr_employee option:selected").val();
            // report_res.innerHTML =  $(".hr_employee option:selected").text();
            // if ($(".hr_employee option:selected").val() == "") {
            //    report_res.innerHTML = "None";
            // }
         }

         
          rpc.query({
             model: 'dynamic.sales.invoice.return',
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
    
  core.action_registry.add("s_i_r", SalesInvoiceReturn);
    return SalesInvoiceReturn;
  });
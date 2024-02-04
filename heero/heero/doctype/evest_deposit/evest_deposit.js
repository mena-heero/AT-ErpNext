// Copyright (c) 2024, Heero and contributors
// For license information, please see license.txt

frappe.ui.form.on("Evest Deposit", {
	refresh:function (frm) {
        frm.add_custom_button(__('Update'), function() {
            frappe.call({
              method: 'heero.heero.doctype.evest_deposit.evest_deposit.fetch_and_update_evest_deposits',
              args: {
                docname: frm.doc.name
              },
              callback: function(response) {
                frappe.msgprint(response.message);
                frm.refresh
              }
            });
          }, __("New"));

	},
});

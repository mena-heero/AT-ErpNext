frappe.ui.form.on("Advertiser", "refresh", function(frm) {
	frm.add_custom_button(__('Transfer to Lead'), function(){
        // Your code for the "Transfer to Lead" button
        frappe.call({
            method: 'heero.heero.doctype.advertiser.advertiser.transfer_to_lead',
            args: {
                docname: frm.doc.name
            },
            callback: function(response) {
                // Show success or error message
                frappe.msgprint(response.message);
            }
        });
    }, __("Actions"));
   
});
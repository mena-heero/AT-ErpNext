frappe.ui.form.on("Influencers", "refresh", function(frm) {
    frm.add_custom_button(__('Update  YT Subscribers'), function(){
        // Your code for the "Update Subscriber Count" button
        frappe.call({
            method: 'heero.heero.doctype.influencers.influencers.update_subscriber_count',
            args: {
                docname: frm.doc.name
            },
            callback: function(response) {
                // Show success or error message
                frappe.msgprint(response.message);
                frm.refresh_field('subcs');
            }
        });
    }, __("Actions"));

    frm.add_custom_button(__('Transfer to Lead'), function(){
        // Your code for the "Transfer to Lead" button
        frappe.call({
            method: 'heero.heero.doctype.influencers.influencers.transfer_to_lead',
            args: {
                docname: frm.doc.name
            },
            callback: function(response) {
                // Show success or error message
                frappe.msgprint(response.message);
            }
        });
    }, __("Actions"));

    frm.add_custom_button(__('Update Instagram Followers'), function(){
        // Your code for the "Update Instagram Followers" button
        frappe.call({
            method: 'heero.heero.doctype.influencers.influencers.update_instagram_followers_count',
            args: {
                docname: frm.doc.name
            },
            callback: function(response) {
                // Show success or error message
                frappe.msgprint(response.message);
                frm.refresh_field('insta_followers');
            }
        });
    }, __("Actions"));
});

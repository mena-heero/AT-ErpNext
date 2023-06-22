// Copyright (c) 2023, Heero and contributors
// For license information, please see license.txt
// heero/heero/doctype/influencers/influencers.js

frappe.ui.form.on('Influencers', {
    refresh: function(frm) {
        // Add a click event listener to your custom button
        frm.add_custom_button(__('Update Subscriber Count'), function() {
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
        });
    }
});

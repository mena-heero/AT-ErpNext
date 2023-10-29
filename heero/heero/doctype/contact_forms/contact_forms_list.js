frappe.listview_settings['Contact Forms'] = {
    button: {
        show(doc) {
            // Log the value of doc.contacted for debugging
            console.log('doc.contacted:', doc.contacted);
            
            // Define conditions when the button should be shown
            return !doc.contacted; // Show the button only for uncontacted records
        },
        get_label() {
            // Set the label for the button
            return 'Send Email';
        },
        get_description(doc) {
            return __('Send {0}', [`${doc.website} ${doc.email}`]);
        },
        action(doc) {
            // Define the action to be executed when the button is clicked
            frappe.call({
                method: 'heero.heero.doctype.contact_forms.contact_forms.send_email_to_uncontacted_party',
                args: { docname: doc.name },
                callback: function (r) {
                    if (r.message) {
                        frappe.msgprint(r.message);
                        cur_list.refresh(); // Refresh the list view
                    }
                }
            });
        }
    },
};

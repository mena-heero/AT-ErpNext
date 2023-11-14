frappe.listview_settings['Flagedu-Lead'] = {

    get_indicator(doc) {
            // customize indicator color
            if (doc.status=="Cancel") {
                return [__("Cancel"), "red", "status,=,cancel"];
            } else  if (doc.status=="In Progress") {
                return [__("In Progress"), "yellow", "status,=,In Progress"];
            }
            else  if (doc.status=="New") {
                return [__("New"), "green", "status,=,New"];
            }
            
            
        },
    
    
    }
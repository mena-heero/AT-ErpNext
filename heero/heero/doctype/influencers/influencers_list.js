frappe.listview_settings['Influencers'] = {

    get_indicator(doc) {
            // customize indicator color
            if (doc.status=="Cancel") {
                return [__("Cancel"), "red", "status,=,cancel"];
            } else  if (doc.status=="Follow Up") {
                return [__("Follow Up"), "yellow", "status,=,Follow Up"];
            }
            else  if (doc.status=="New") {
                return [__("New"), "green", "status,=,New"];
            }
            
        },
    
    
    }
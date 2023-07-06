frappe.ui.form.on('Influencers', {
    refresh: function(frm) {
      frm.add_custom_button(__('YouTube'), function() {
        frappe.call({
          method: 'heero.heero.doctype.influencers.influencers.update_subscriber_count',
          args: {
            docname: frm.doc.name
          },
          callback: function(response) {
            frappe.msgprint(response.message);
            frm.refresh_field('subcs');
          }
        });
      }, __("Subscribers"));
  
      frm.add_custom_button(__('Transfer to Lead'), function() {
        frappe.call({
          method: 'heero.heero.doctype.influencers.influencers.transfer_to_lead',
          args: {
            docname: frm.doc.name
          },
          callback: function(response) {
            frappe.msgprint(response.message);
          }
        });
      }, __("Actions"));
      frm.add_custom_button(__('Facebook'), function() {
        frappe.call({
          method: 'heero.heero.doctype.influencers.util.update_facebook_followers_count',
          args: {
            docname: frm.doc.name
          },
          callback: function(response) {
            frappe.msgprint(response.message);
            frm.refresh_field('facebook_followers');
          }
        });
      }, __("Subscribers"));
  
  
      frm.add_custom_button(__('Instagram'), function() {
        frappe.call({
          method: 'heero.heero.doctype.influencers.influencers.update_instagram_followers_count',
          args: {
            docname: frm.doc.name
          },
          callback: function(response) {
            frappe.msgprint(response.message);
            frm.refresh_field('insta_followers');
          }
        });
      }, __("Subscribers"));
      frm.add_custom_button(__('Tiktok'), function() {
        frappe.call({
          method: 'heero.heero.doctype.influencers.influencers.update_tiktok_followers_count',
          args: {
            docname: frm.doc.name
          },
          callback: function(response) {
            frappe.msgprint(response.message);
            frm.refresh_field('tiktok_followers');
          }
        });
      }, __("Subscribers"));
      frm.add_custom_button(__('Snapchat'), function() {
        frappe.call({
          method: 'heero.heero.doctype.influencers.influencers.update_snapchat_followers_count',
          args: {
            docname: frm.doc.name
          },
          callback: function(response) {
            frappe.msgprint(response.message);
            frm.refresh_field('snapchat_followers');
          }
        });
      }, __("Subscribers"));
  
      frm.add_custom_button(__('Update Channels'), function() {
        var doc = frm.doc;
        frappe.call({
            method: 'heero.heero.doctype.influencers.channels.update_channels',
            args: {
                doc: doc
            },
            callback: function(response) {
                if (response.message) {
                    // Success
                    frm.refresh_field('channels');
                    frappe.msgprint('Channels updated successfully.');
                } else {
                    // Error
                    frappe.msgprint('Failed to update channels.');
                }
            }
        });
    }, __("Actions"));
    frm.add_custom_button(__('Attach Images'), function() {
      frappe.call({
          method: 'heero.heero.doctype.influencers.download.download_images_for_influencer',
          args: {
              influencer_docname: frm.doc.name
          },
          callback: function(response) {
              frappe.msgprint(response.message);
              frm.reload_doc();
          }
      });
  }, __("Actions"));
  
    
    
    }
  });
  
  
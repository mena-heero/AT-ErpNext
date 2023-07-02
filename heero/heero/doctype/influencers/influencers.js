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
        var channelLinks = frm.doc.channel_link.split('\n');
        var childTable = frm.doc.influencer_channels || [];
  
        for (var i = 0; i < channelLinks.length; i++) {
          var channelLink = channelLinks[i].trim();
          if (channelLink) {
            var platform = getPlatformFromLink(channelLink);
            var existingChannel = childTable.find(row => row.channel_link === channelLink);
  
            if (!existingChannel) {
              var childRow = frappe.model.add_child(frm.doc, 'Influencer Channels', 'influencer_channels');
              childRow.channel_link = channelLink;
              childRow.platform = platform;
            }
          }
        }
  
        frm.refresh_field('influencer_channels');
      }, __("Actions"));
    }
  });
  
  function getPlatformFromLink(link) {
    if (link.includes('youtube.com') || link.includes('youtu.be')) {
      return 'YouTube';
    } else if (link.includes('facebook.com')) {
      return 'Facebook';
    } else if (link.includes('instagram.com')) {
      return 'Instagram';
    } else if (link.includes('tiktok.com')) {
      return 'TikTok';
    } else if (link.includes('snapchat.com')) {
      return 'Snapchat';
    } else if (link.includes('twitter.com')) {
      return 'Twitter';
    } else {
      return '';
    }
  }
  
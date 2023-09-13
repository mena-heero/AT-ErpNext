from frappe import _

def execute(filters=None):
    topic_route = filters.get("topic_route")
    topic_data = frappe.call('heero.api.get_topic_detail', topic_route)
    
    context = {
        'topic': topic_data['topic']
    }

    html = frappe.render_template('topic_detail.html', context)
    return html

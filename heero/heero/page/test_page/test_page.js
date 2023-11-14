frappe.pages['test-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Home',
		single_column: true
	});
	page.set_title('My Page')
	page.set_title_sub('Subtitle')
	page.set_indicator('Pending', 'orange')
	let $btn = page.set_primary_action('New', () => create_new(), 'octicon octicon-plus')
	let $list = page.add_inner_button('List', () => list(), 'octicon octicon-list')
}
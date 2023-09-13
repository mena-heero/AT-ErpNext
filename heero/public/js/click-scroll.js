$(document).ready(function() {
    // Function to update the active navigation link based on the URL
    function updateActiveLink() {
        var currentURL = window.location.href;
        var sectionID = currentURL.split('#')[1]; // Get the section ID from the URL's hash
        
        $('.navbar-nav .nav-item .nav-link').removeClass('active');
        $('.navbar-nav .nav-item .nav-link').addClass('inactive');
        
        if (sectionID) {
            $('a.nav-link[href="#' + sectionID + '"]').addClass('active');
            $('a.nav-link[href="#' + sectionID + '"]').removeClass('inactive');
        }
    }
    
    // Call the function on page load
    updateActiveLink();
    
    // Call the function whenever the hash in the URL changes (e.g., through clicks or navigation)
    $(window).on('hashchange', function() {
        updateActiveLink();
    });
    
    // Smooth scroll to the section when a navigation link is clicked
    $('.click-scroll').click(function(e) {
        e.preventDefault();
        var sectionID = $(this).attr('href');
        var offsetClick = $(sectionID).offset().top - 75;
        
        $('html, body').animate({
            scrollTop: offsetClick
        }, 300);
        
        // Update the URL without triggering the hashchange event
        history.pushState(null, null, sectionID);
        
        // Update the active navigation link
        updateActiveLink();
    });
});

$(document).ready(function() {

    // Show/Hide filter options in Home screen
    $("#nav-filter").click(function() {
        $("#recipe-filter").slideToggle(500);
    });

    // Scroll Top button
    window.onscroll = function() { scrollFunction() };

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            $('#back-btn').fadeIn(100);
        }
        else {
            $('#back-btn').fadeOut(100);
        }
    }
    $("#back-btn").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "fast");
    });
    
    // Login Page - Create new login account
    $('#createNewAccount').on('click',function() {
        $(".login").hide(0);
        $(".create_account").show(0);
    });
    $('#cancelNewAccount').on('click',function() {
        $(".create_account").hide(0);
        $(".login").show(0);
    });

    // Recipe Cuisine & SAVE RECIPE button - updates DB.users with recipe id for saved_recipes
    $(".recipe-row").mouseenter(function() {
        $(this).children('#save-section').children('.save-option').hide();
        $(this).children('#save-section').children('.save-recipe').show(100);
        $(this).children('#save-section').css({ "background-color": "#007bff", "transition": "background-color 0.5s ease" })
    });
    $(".save-recipe").mouseenter(function() {
        $(this).parent(".save-section").css({
            "outline": "3px solid #fff",  "transition": "outline-color 0.5s ease"
        })
    });
    $(".recipe-row").mouseleave(function() {
        $(this).children('#save-section').children('.save-recipe').hide(100);
        $(this).children('#save-section').children('.save-option').show(100);
        $(this).children('#save-section').css({ "background-color": "#5b9bd5", "transition": "background-color 0.5s ease" })
    });
    $(".save-recipe").mouseleave(function() {
        $(this).parent(".save-section").css({
            "outline": "none",  "transition": "outline-color 0.5s ease"
        })
    });

    // REMOVE RECIPE button - updates DB.users with recipe id for remove_recipes
    $(".saved-recipe-row").mouseenter(function() {
        $(this).children('#remove-section').children('.remove-option').hide();
        $(this).children('#remove-section').children('.remove-recipe').show(100);
        $(this).children('#remove-section').css({ "background-color": "#ff303b", "transition": "background-color 0.5s ease" })
    });
    $(".remove-recipe").mouseenter(function() {
        $(this).parent("#remove-section").css({
            "outline": "3px solid #fff",  "transition": "outline-color 0.5s ease"
        })
    });
    $(".saved-recipe-row").mouseleave(function() {
        $(this).children('#remove-section').children('.remove-recipe').hide(100);
        $(this).children('#remove-section').children('.remove-option').show(100);
        $(this).children('#remove-section').css({ "background-color": "#5b9bd5", "transition": "background-color 0.5s ease" })
    });
    $(".remove-recipe").mouseleave(function() {
        $(this).parent("#remove-section").css({
            "outline": "none",  "transition": "outline-color 0.5s ease"
        })
    });

    // Add Recipe Page - Preview Image
    $('#prevImg').on('click', function() {
        var url = $('#photoUrl').val()
        $('#photo-preview img').prop('src', url);
        $('#photo-preview img').prop('alt', 'Please make sure the URL is correct');
    });
    $('#clearImg').on('click', function() {
        $('#photoUrl').val("")
        $('#photo-preview img').prop('src', "");
        $('#photo-preview img').prop('alt', "");
    });

    // View/Edit Page - Toggle View & Edit page mode
    $('#edit-btn').click(function() {
        if ($(this).html() == 'Cancel') {
            $(this).html('Edit');
            $('#edit-mode').hide();
            $('#next-btn').hide();
            $('#view-mode').show();
            $('#save-btn').show();
            $('.page-header').html('View Recipe')
        }
        else {
            $(this).html('Cancel');
            $('#edit-mode').show();
            $('#next-btn').show();
            $('#view-mode').hide();
            $('#save-btn').hide();
            $('.page-header').html('Edit Recipe')
        }
    });

    function allergyPopup() {
        $('#submit-btn').click();
    }
    
    $('#save-confirm').on('click',function() {
        $("#save-alert").remove()
    });

});



window.onload = function() {

    $('.save-recipe').each(function() {
        var recipeID = $(this).attr("id");
        var recipeLink = $(this).attr("href")
        recipeLink = recipeLink.replace('REPLACE', recipeID);
        $(this).attr("href", recipeLink);
    });
    $('.remove-recipe').each(function() {
        var recipeID = $(this).attr("id");
        var recipeLink = $(this).attr("href")
        recipeLink = recipeLink.replace('REPLACE', recipeID);
        $(this).attr("href", recipeLink);
    });
    $('.view-recipe').each(function() {
        var recipeID = $(this).attr("id");
        var recipeLink = $(this).attr("href")
        recipeLink = recipeLink.replace('REPLACE', recipeID);
        $(this).attr("href", recipeLink);
    });


}

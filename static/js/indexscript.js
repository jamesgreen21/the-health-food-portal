$(document).ready(function() {

    fetch('/get_recipes')
        // Build each recipe entry in the Home screen
        .then((response) => response.json())
        .then(function(data) {
            for (var i = 0; i < data.length; i++) {

                var recipeRow = [
                    '<div class="row recipe-row">',
                    '<div id="cuisine-section" class="col-12 col-md-1 cuisine-section">',
                    '<div class="cuisine-content">' + data[i].cuisine + '</div>',
                    '<a id="save-recipe" style="display:none">Save Recipe</a>',
                    '</div>',
                    '<div class="col-4 col-md-2 photo-section">',
                    '<img src="' + data[i].photo_id + '" class="photo-content"></img>',
                    '</div>',
                    '<div class="col-8 col-md-7 recipe-section">',
                    '<h4 class="recipe-title">' + data[i].recipe_name + '</h4>',
                    '<p class="recipe-description">' + data[i].recipe_description + '</p>',
                    '<p class="recipe-time">' + data[i].cook_time + ' Minutes</p>',
                    '<a id="view-recipe" name="' + data[i].id + '">View Recipe</a>',
                    '</div>',
                    '<div class="col-12 col-md-2 nutrition-section">',
                    '<div class="nutrition-calories">',
                    '<span>' + data[i].calories + '</span>',
                    '</div>',
                    '<div class="nutrition-protein">' + data[i].protein + ' grams</div>',
                    '</div>',
                    '</div>'
                ].join("\n");

                // Add all html to container
                $('#recipe-data').append(recipeRow);

                // View Recipe - Update the href link with url_for
                var recipeLink = $('#temp-link-view').attr("href")
                var url = recipeLink.replace('REPLACE', data[i].id);
                var recipeAnchor = document.getElementsByName([name = data[i].id]);
                recipeAnchor[0].setAttribute('href', url);

                // // Save Recipe - Update the href link with url_for
                var saveLink = $('#temp-link-save').attr("href")
                url = saveLink.replace('REPLACE', data[i].i);
                var allAnchors = document.getElementsByName([name = data[i].id]);
                // for (var i = 0; i < allAnchors.length; i++) {
                //     if (allAnchors[i].attr('name') == data[i].id) {
                //         console.log(allAnchors[i]);
                //         // saveAnchors = allAnchors[i];
                //     }
                // }
                // saveAnchors.setAttribute('href', url);

            }

            // Recipe Cuisine / SAVE RECIPE button - updates DB.users with recipe id for saved_recipes
            $(".cuisine-section").mouseenter(function() {
                $(this).children('.cuisine-content').hide();
                $(this).children('a').show(100);
                $(this).css({ "background-color": "#5b9bd5", "transition": "background-color 0.5s ease" })
            });
            $(".cuisine-section").mouseleave(function() {
                $(this).children('a').hide();
                $(this).children('.cuisine-content').show(100);
                $(this).css({ "background-color": "#000", "transition": "background-color 0.5s ease" })
            });

            // Remove temp-links from HTML
            ("#temp-link").remove();
        })
        // .then(function(data) {

        //     let filteredData = '';
        //     function filterCuisine(data, selectedCuisine) {
        //         for (var i = 0; i < data.length; i++) {
        //             if (data[i].cuisine == selectedCuisine) {
        //                 filteredData += data[i];
        //             }
        //         }
        //     }

        //     function myFunction() {
        //         document.getElementById("demo").innerHTML = ages.filter(filterCuisine);
        //     }

        // })
        .catch(function(error) {
            console.log(error);
        });

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


});

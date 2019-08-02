$(document).ready(function() {

    fetch('/get_recipes')
        // Build each recipe entry in the Home screen
        .then((response) => response.json())
        .then(function(data) {
            var divContainer = document.getElementById('recipe-data');
            for (var i = 0; i < data.length; i++) {
                var recipeRow = ''

                recipeRow += '<div class="row recipe-row">'
                recipeRow += '<div id="cuisine-section" class="col-12 col-md-1 cuisine-section">'
                recipeRow += '<div class="cuisine-content">'
                recipeRow += data[i].cuisine
                recipeRow += '</div><span style="display:none">Save Recipe</span></div><div class="col-4 col-md-2 photo-section"><img src="'
                recipeRow += data[i].photo_id
                recipeRow += '" class="photo-content"></img></div>'
                recipeRow += '<div class="col-8 col-md-7 recipe-section"><h4 class="recipe-title">'
                recipeRow += data[i].recipe_name
                recipeRow += '</h4><p class="recipe-description">'
                recipeRow += data[i].recipe_description
                recipeRow += '</p><p class="recipe-time">'
                recipeRow += data[i].cook_time
                recipeRow += '</p></div><div class="col-12 col-md-2 nutrition-section">'
                recipeRow += '<div class="nutrition-calories"><span>'
                recipeRow += data[i].calories
                recipeRow += ' Cals</span></div><div class="nutrition-protein">'
                recipeRow += data[i].protein
                recipeRow += ' grams</div></div></div>'

                $('#recipe-data').append(recipeRow);
            }

            $(".cuisine-section").mouseenter(function() {
                $(this).children('.cuisine-content').hide();
                $(this).children('span').show(100);
                $(this).css({ "background-color": "#5b9bd5", "transition": "background-color 0.5s ease" })
            });
            $(".cuisine-section").mouseleave(function() {
                $(this).children('span').hide();
                $(this).children('.cuisine-content').show(100);
                $(this).css({ "background-color": "#000", "transition": "background-color 0.5s ease" })
            });

        })
        .catch(function(error) {
            console.log(error);
        });

    $("#nav-filter").click(function() {
        // Show / hide filter options in Home screen
        $("#recipe-filter").slideToggle(500);
    });

});

{"filter":false,"title":"myscript.js","tooltip":"/static/js/myscript.js","undoManager":{"mark":2,"position":2,"stack":[[{"start":{"row":0,"column":0},"end":{"row":5,"column":0},"action":"remove","lines":["$(document).ready(function() {","    ","","","});",""],"id":2},{"start":{"row":0,"column":0},"end":{"row":55,"column":0},"action":"insert","lines":["    $(document).ready(function() {","","        fetch('/get_recipes')","            // Build each recipe entry in the Home screen","            .then((response) => response.json())","            .then(function(data) {","                var divContainer = document.getElementById('recipe-data');","                for (var i = 0; i < data.length; i++) {","                    var recipeRow = ''","","                    recipeRow += '<div class=\"row recipe-row\">'","                    recipeRow += '<div id=\"cuisine-section\" class=\"col-12 col-md-1 cuisine-section\">'","                    recipeRow += '<div class=\"cuisine-content\">'","                    recipeRow += data[i].cuisine","                    recipeRow += '</div><span style=\"display:none\">Save Recipe</span></div><div class=\"col-4 col-md-2 photo-section\"><img src=\"'","                    recipeRow += data[i].photo_id","                    recipeRow += '\" class=\"photo-content\"></img></div>'","                    recipeRow += '<div class=\"col-8 col-md-7 recipe-section\"><h4 class=\"recipe-title\">'","                    recipeRow += data[i].recipe_name","                    recipeRow += '</h4><p class=\"recipe-description\">'","                    recipeRow += data[i].recipe_description","                    recipeRow += '</p><p class=\"recipe-time\">'","                    recipeRow += data[i].cook_time","                    recipeRow += '</p></div><div class=\"col-12 col-md-2 nutrition-section\">'","                    recipeRow += '<div class=\"nutrition-calories\"><span>'","                    recipeRow += data[i].calories","                    recipeRow += ' Cals</span></div><div class=\"nutrition-protein\">'","                    recipeRow += data[i].protein","                    recipeRow += ' grams</div></div></div>'","","                    $('#recipe-data').append(recipeRow);","                }","","                $(\".cuisine-section\").mouseenter(function() {","                    $(this).children('.cuisine-content').hide();","                    $(this).children('span').show(100);","                    $(this).css({ \"background-color\": \"#5b9bd5\", \"transition\": \"background-color 0.5s ease\" })","                });","                $(\".cuisine-section\").mouseleave(function() {","                    $(this).children('span').hide();","                    $(this).children('.cuisine-content').show(100);","                    $(this).css({ \"background-color\": \"#000\", \"transition\": \"background-color 0.5s ease\" })","                });","","            })","            .catch(function(error) {","                console.log(error);","            });","","        $(\"#nav-filter\").click(function() {","            // Show / hide filter options in Home screen","            $(\"#recipe-filter\").slideToggle(500);","        });","","    });",""]}],[{"start":{"row":55,"column":0},"end":{"row":55,"column":4},"action":"insert","lines":["    "],"id":3}],[{"start":{"row":0,"column":0},"end":{"row":0,"column":4},"action":"remove","lines":["    "],"id":4},{"start":{"row":2,"column":0},"end":{"row":2,"column":4},"action":"remove","lines":["    "]},{"start":{"row":3,"column":0},"end":{"row":3,"column":4},"action":"remove","lines":["    "]},{"start":{"row":4,"column":0},"end":{"row":4,"column":4},"action":"remove","lines":["    "]},{"start":{"row":5,"column":0},"end":{"row":5,"column":4},"action":"remove","lines":["    "]},{"start":{"row":6,"column":0},"end":{"row":6,"column":4},"action":"remove","lines":["    "]},{"start":{"row":7,"column":0},"end":{"row":7,"column":4},"action":"remove","lines":["    "]},{"start":{"row":8,"column":0},"end":{"row":8,"column":4},"action":"remove","lines":["    "]},{"start":{"row":10,"column":0},"end":{"row":10,"column":4},"action":"remove","lines":["    "]},{"start":{"row":11,"column":0},"end":{"row":11,"column":4},"action":"remove","lines":["    "]},{"start":{"row":12,"column":0},"end":{"row":12,"column":4},"action":"remove","lines":["    "]},{"start":{"row":13,"column":0},"end":{"row":13,"column":4},"action":"remove","lines":["    "]},{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"remove","lines":["    "]},{"start":{"row":15,"column":0},"end":{"row":15,"column":4},"action":"remove","lines":["    "]},{"start":{"row":16,"column":0},"end":{"row":16,"column":4},"action":"remove","lines":["    "]},{"start":{"row":17,"column":0},"end":{"row":17,"column":4},"action":"remove","lines":["    "]},{"start":{"row":18,"column":0},"end":{"row":18,"column":4},"action":"remove","lines":["    "]},{"start":{"row":19,"column":0},"end":{"row":19,"column":4},"action":"remove","lines":["    "]},{"start":{"row":20,"column":0},"end":{"row":20,"column":4},"action":"remove","lines":["    "]},{"start":{"row":21,"column":0},"end":{"row":21,"column":4},"action":"remove","lines":["    "]},{"start":{"row":22,"column":0},"end":{"row":22,"column":4},"action":"remove","lines":["    "]},{"start":{"row":23,"column":0},"end":{"row":23,"column":4},"action":"remove","lines":["    "]},{"start":{"row":24,"column":0},"end":{"row":24,"column":4},"action":"remove","lines":["    "]},{"start":{"row":25,"column":0},"end":{"row":25,"column":4},"action":"remove","lines":["    "]},{"start":{"row":26,"column":0},"end":{"row":26,"column":4},"action":"remove","lines":["    "]},{"start":{"row":27,"column":0},"end":{"row":27,"column":4},"action":"remove","lines":["    "]},{"start":{"row":28,"column":0},"end":{"row":28,"column":4},"action":"remove","lines":["    "]},{"start":{"row":30,"column":0},"end":{"row":30,"column":4},"action":"remove","lines":["    "]},{"start":{"row":31,"column":0},"end":{"row":31,"column":4},"action":"remove","lines":["    "]},{"start":{"row":33,"column":0},"end":{"row":33,"column":4},"action":"remove","lines":["    "]},{"start":{"row":34,"column":0},"end":{"row":34,"column":4},"action":"remove","lines":["    "]},{"start":{"row":35,"column":0},"end":{"row":35,"column":4},"action":"remove","lines":["    "]},{"start":{"row":36,"column":0},"end":{"row":36,"column":4},"action":"remove","lines":["    "]},{"start":{"row":37,"column":0},"end":{"row":37,"column":4},"action":"remove","lines":["    "]},{"start":{"row":38,"column":0},"end":{"row":38,"column":4},"action":"remove","lines":["    "]},{"start":{"row":39,"column":0},"end":{"row":39,"column":4},"action":"remove","lines":["    "]},{"start":{"row":40,"column":0},"end":{"row":40,"column":4},"action":"remove","lines":["    "]},{"start":{"row":41,"column":0},"end":{"row":41,"column":4},"action":"remove","lines":["    "]},{"start":{"row":42,"column":0},"end":{"row":42,"column":4},"action":"remove","lines":["    "]},{"start":{"row":44,"column":0},"end":{"row":44,"column":4},"action":"remove","lines":["    "]},{"start":{"row":45,"column":0},"end":{"row":45,"column":4},"action":"remove","lines":["    "]},{"start":{"row":46,"column":0},"end":{"row":46,"column":4},"action":"remove","lines":["    "]},{"start":{"row":47,"column":0},"end":{"row":47,"column":4},"action":"remove","lines":["    "]},{"start":{"row":49,"column":0},"end":{"row":49,"column":4},"action":"remove","lines":["    "]},{"start":{"row":50,"column":0},"end":{"row":50,"column":4},"action":"remove","lines":["    "]},{"start":{"row":51,"column":0},"end":{"row":51,"column":4},"action":"remove","lines":["    "]},{"start":{"row":52,"column":0},"end":{"row":52,"column":4},"action":"remove","lines":["    "]},{"start":{"row":54,"column":0},"end":{"row":54,"column":4},"action":"remove","lines":["    "]},{"start":{"row":55,"column":0},"end":{"row":55,"column":4},"action":"remove","lines":["    "]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":49,"column":18},"end":{"row":49,"column":18},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":7,"state":"start","mode":"ace/mode/javascript"}},"timestamp":1564681738234,"hash":"57955ae8527ed90d61c9acf3298cb0ab9ee77eb2"}
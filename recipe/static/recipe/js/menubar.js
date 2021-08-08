mealApp = {};
mealApp.recipe_ids=[];
mealApp.recipe_names=[];
mealApp.addToMeal = function(t,id,name){
    console.log(id);
    if (mealApp.recipe_ids.includes(id)){
        $('#removeFromMeal-'+id).click()
    } else{
        mealApp.recipe_ids.push(id);
        mealApp.recipe_names.push(name);
        $(t).html('-');
        $('#menu-recipes').append(
            `<li>
                
                <button id="removeFromMeal-`+id+`" class="btn btn-danger me-3" onclick="mealApp.removeFromMeal(this,`+id+`)"> X </button>
                <a href=/recipe/`+id+`>`
                + name +
                `</a>
            </li>`       
        );
    }
    document.cookie = "mealIds="+mealApp.recipe_ids.join(",")+";path=/"
    document.cookie = "mealNames="+mealApp.recipe_names.join(",")+";path=/"
}
mealApp.removeFromMeal = function(t,id){
    $(t).parent().remove();
    $('#addToMeal-'+id).html('+');
    let index = mealApp.recipe_ids.indexOf(id)
    mealApp.recipe_ids.splice(index,1);
    mealApp.recipe_names.splice(index,1);
    document.cookie = "mealIds="+mealApp.recipe_ids.join(",")+";path=/"
    document.cookie = "mealNames="+mealApp.recipe_names.join(",")+";path=/"
}
mealApp.setup = function(){
    let cookies = document.cookie.split(";");
    let recipe_ids =[];
    let recipe_names=[];
    for(let i=0; i<cookies.length;i++){
        let key = cookies[i].split("=")[0].trim();
        if(key=='mealIds'){
            recipe_ids=cookies[i].split("=")[1].split(",").map(function (e){
                return parseInt(e.trim());
            })
        } else if (key=='mealNames'){
            recipe_names=cookies[i].split("=")[1].split(",").map(function(e){return e.trim()});
        }
    }
    for(let i=0; i<recipe_ids.length;i++){
        let id = recipe_ids[i];
        if(id){
            mealApp.addToMeal('#addToMeal-'+id,recipe_ids[i],recipe_names[i]);
        }
       
    }
}
mealApp.goToMeal = function(){
    window.location.href = '/meal/'+mealApp.recipe_ids.join(",")
}
mealApp.goToShoppingList = function(){
    window.location.href = '/meal/'+mealApp.recipe_ids.join(",")+"/shopping-list"
}
window.onload = function(){
    mealApp.setup()
}
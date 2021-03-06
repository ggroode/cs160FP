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
        // $(t).html('-');
        $(t).html('<img class="plus" style="width: 100%;aspect-ratio:1 / 1 color:black;max-height:100%" src=\'https://icons-for-free.com/iconfiles/png/512/x+icon-1320166903649367557.png\' />')
        $('#menu-recipes').append(
            `<li>
                <button id="removeFromMeal-`+id+`" class="btn-exit btn-close me-3" style="height:20px;width:30px; margin-top: 2%" onclick="mealApp.removeFromMeal(this,`+id+`)"></button>
                <a href="/recipe/`+id+`"style="color:black">`
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
    // $('#addToMeal-'+id).html('+');
    $('#addToMeal-'+id).html('<img class="plus" style="width: 100%;aspect-ratio:1 / 1;max-height:100%" src=\'https://icons-for-free.com/iconfiles/png/512/plus+icon-1320166903617346293.png\' />')
    let index = mealApp.recipe_ids.indexOf(id)
    mealApp.recipe_ids.splice(index,1);
    mealApp.recipe_names.splice(index,1);
    document.cookie = "mealIds="+mealApp.recipe_ids.join(",")+";path=/"
    document.cookie = "mealNames="+mealApp.recipe_names.join(",")+";path=/"
    document.cookie = "servings-"+id+"= ;expires = Thu, 01 Jan 1970 00:00:00 GMT;path=/"
}
mealApp.setup = function(){
    let cookies = document.cookie.split(";");
    let recipe_ids =[];
    let recipe_names=[];
    for(let i=0; i<cookies.length;i++){
        let key = cookies[i].split("=")[0].trim();
        let value=cookies[i].split("=")[1].trim()
        if(key=='mealIds'){
            recipe_ids=value.split(",").map(function (e){
                return parseInt(e.trim());
            })
        } else if (key=='mealNames'){
            recipe_names=value.split(",").map(function(e){return e.trim()});
        } else if (/^servings-\d+/.test(key)){
            const id = Number(key.split("-")[1])
            $("#servings-"+id).val(Number(value));
            $("#servings-"+id).click();
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
    if (mealApp.recipe_ids.length){
        window.location.href = '/meal/'+mealApp.recipe_ids.join(",")
    } else{
        alert("You need to add something to your list first");
    }
    
}
mealApp.goToShoppingList = function(){
    if (mealApp.recipe_ids.length){
        window.location.href = '/meal/'+mealApp.recipe_ids.join(",")+"/shopping-list"
    }else{
        alert("You need to add something to your list first");
    }
    
}
mealApp.saveMeal = function(uid,url){
    if (uid == -1) {
        alert("Please Sign In to Save Meals!");
        return;
    }
    let name = $("#meal-name").val();
    $.post(url,{name:name},
        function(data,status,JqXHR) {
            window.location.href = url;
        }
    ) 
    
}
mealApp.mealLink = function(ids,names){
    document.cookie = "mealIds="+ids+";path=/"
    document.cookie = "mealNames="+String(names).replace(/[^\w,]/,"")+";path=/"
}
window.onload = function(){
    mealApp.setup()
}
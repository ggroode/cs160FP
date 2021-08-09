// additions
const steps = [];
const ingredients = [];
let tags = [];
let priva = true;
let recipeType = "Entree";
let recipeName = "";
let recipeDesc = "";
let recipeCT = 0;
let recipeServings = 0;
let recipeServingSize = "";

let stepsJSON = "";
let ingJSON = "";
let tagsJSON = "";

// removals
const removedSteps = [];
const removedIngredients = [];
const removedTags = [];

// HTML strings
const ingredientItem = `
<li>
  <span name="ingli">
    <input type="text" value="" placeholder="ingredient" class="border" style="width:35%">
    <input type="text" value="" placeholder="amount" class="border" style="width:15%">
    <input type="text" value="" placeholder="unit" class="border" style="width:25%">
  </span>
  <button type="button" class="btn btn-danger" onClick="removeIngredient(this.parentNode)">X</button>
</li>`;
const stepItem = `
  <li>
    <span name="stepspan" class="text-decoration-underline" contenteditable>instruction</span>
    <button type="button" class="btn btn-danger" onClick="removeStep(this.parentNode)">X</button>
  </li>`;

// create XMLHttpRequest
function addStep() {
  document.getElementById('steps').innerHTML += stepItem;
}

function addIngredient() {
  $('#ingredients').append(ingredientItem);
}

function pushSteps() {
  steps.length = 0;
  for (let step of $('span[name=stepspan]')) {
    steps.push(
      step.innerHTML.replace(/&nbsp;|<br>/g," ")
    )
  }
}

function pushIngredients() {
  ingredients.length = 0;
  let inps = $('span[name=ingli]').children();
  for (let i = 0; i < inps.length; i+=3) {
    ingredients.push([inps[i].value, Number(inps[i + 1].value), inps[i + 2].value]);
  }
  ingJSON = JSON.stringify(ingredients);
}

function setBasicInfo() {
  recipeName = $('#name').val();
  recipeDesc = $('#description').val();
  recipeCT = Number($('#ct').val());
  recipeServings = Number($('#servings').val());
  recipeServingSize = $('#servingSize').val();
}

function pushTags() {
  tags = $('#tags').val().split(/[^\w]/);
  // tagsJSON = JSON.stringify(tags);
}

function setRecipeInfo() {
  pushSteps();
  pushIngredients();
  pushTags();
  setBasicInfo();
}

function sendRecipeInfo() {
  // TODO: finish
  setRecipeInfo();
  const message = createFD();
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "#", true);
  // xhr.onload = function () {
  //   window.location.href = xhr.responseURL;
  // };
  xhr.send(message);

}

function removeStep(item) {
  removedSteps.push(item.children[0].innerHTML.replace(/&nbsp;|<br>/g," "));
  item.remove();
}

function removeIngredient(item) {
  removedIngredients.push([item.children[0].children[0].value, item.children[0].children[1].value, item.children[0].children[2].value]);
  item.remove();
}

function removeTags(item) {
  // TODO: finish
  item.remove();
}

function createDict() {
  const message = new FormData();

  message["name"] = recipeName;
  message["description"] = recipeDesc;
  message["cookingTime"] = recipeCT;
  message["image"] = document.getElementById('upload').files[0];
  message["classification"] = recipeType;
  message["servings"] = recipeServings;
  message["servingSize"] = recipeServingSize;
  message["author"] = uid;
  message["private"] = priva;
  message["ingredients"] = ingJSON;
  message["steps"] = steps;
  message["tags"] = tags;
  message["removedSteps"] = removedSteps;
  message["removedIngredients"] = removedIngredients;
  message["removedTags"] = removedTags;

  return message;
}

function createFD() {
  const message = new FormData();

  message.append("name", recipeName);
  message.append("description", recipeDesc);
  message.append("cookingTime", recipeCT);
  message.append("files[]", document.getElementById('upload').files[0]);
  message.append("classification", recipeType);
  message.append("servings", recipeServings);
  message.append("servingSize", recipeServingSize);
  message.append("author", uid);
  message.append("private", priva);
  message.append("ingredients", ingJSON);
  message.append("steps", steps);
  message.append("tags", tags);
  // message.append("removedSteps", removedSteps);
  // message.append("removedIngredients", removedIngredients);
  // message.append("removedTags", removedTags);

  return message;
}

// very cool image js
/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
    });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById( 'upload' );
var infoArea = document.getElementById( 'upload-label' );

input.addEventListener( 'change', showFileName );
function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

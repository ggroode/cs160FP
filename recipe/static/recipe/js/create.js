// additions
const steps = [];
const ingredients = [];
const tags = [];
let priva = true;
let recipeType = "Entree";
let recipeName = "";
let recipeDesc = "";
let recipeCT = 0;
let recipeServings = 0;
let recipeServingSize = "";

// removals
const removedSteps = [];
const removedIngredients = [];
const removedTags = [];

// HTML strings
const ingredientItem = `
<li>
  <span name="ingli">
    <input type="text" value="" placeholder="ingredient" class="border">
    <input type="text" value="" placeholder="amount" class="border">
    <input type="text" value="" placeholder="unit" class="border">
  </span>
  <button type="button" class="btn btn-danger" onClick="removeIngredient(this.parentNode)">X</button>
</li>`;
const stepItem = `
  <li>
    <span name="stepspan" class="text-decoration-underline" contenteditable>instruction</span>
    <button type="button" class="btn btn-danger" onClick="removeStep(this.parentNode)">X</button>
  </li>`;


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
    ingredients.push([inps[i].value, inps[i + 1].value, inps[i + 2].value]);
  }
}

function setBasicInfo() {
  recipeName = $('#name').val();
  recipeDesc = $('description').val();
  recipeCT = $('ct').val();
  recipeServings = $('servings').val();
  recipeServingSize = $('servingSize').val();
}

function pushTags() {
  // TODO: finish
  return;
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
  const message = createJSON();
  return;
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

function createJSON() {
  const message = {};

  message["name"] = recipeName;
  message["description"] = recipeDesc;
  message["cookingTime"] = recipeCT;
  message["image"];
  message["classification"] = recipeType;
  message["servings"] = recipeServings;
  message["servingSize"] = recipeServingSize;
  message["author"] = uid;
  message["private"] = priva;
  message["ingredients"] = ingredients;
  message["steps"] = steps;
  message["tags"] = tags;
  message["removedSteps"] = removedSteps;
  message["removedIngredients"] = removedIngredients;
  message["removedTags"] = removedTags;

  return JSON.stringify(message);
}

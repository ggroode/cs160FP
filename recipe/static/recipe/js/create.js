function addStep() {
  document.getElementById('steps').innerHTML += `
    <li>
      <textarea></textarea>
    </li>`;
}

function addIngredient() {
  document.getElementById('ingredients').innerHTML += `
  <li>
  <input type="text" value="" placeholder="ingredient" class="border">
  <input type="text" value="" placeholder="amount" class="border">
  <input type="text" value="" placeholder="unit" class="border">
  </li>`
}

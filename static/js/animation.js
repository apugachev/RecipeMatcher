var modals = document.getElementsByClassName('modal');

// Get the button that opens the modal
var btns = document.getElementsByClassName("btn btn-sm btn-outline-secondary");

// Get the <span> element that closes the modal
var spans = document.getElementsByClassName("close");

// When the user clicks the button, open the modal
for (let i = 0; i < btns.length; i++) {
   btns[i].onclick = function() {
      modals[i].style.display = "block";
   }
}

// When the user clicks on <span> (x), close the modal
for (let i = 0; i < spans.length; i++) {
    spans[i].onclick = function() {
       modals[i].style.display = "none";
    }
 }

window.onclick = function(event) {
    for (let i = 0; i < spans.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
    }
  }
};

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    for (let i = 0; i < spans.length; i++) {
       modals[i].style.display = "none"
    }
  }
});
// Adds the class "late" to the rows which due date has been exceeded 
function lateToRed(){
    var rowElts = document.querySelectorAll("tbody tr");

    rowElts.forEach(element => {
        var dueDateElt = element.querySelector('.duedate');   
        var date = new Date(dueDateElt.textContent);
    
        if (date < Date.now()) {
            element.classList.add("late")
        }
    });
}

// When the page is entirely loaded
window.addEventListener("load", function() {
    lateToRed();
});



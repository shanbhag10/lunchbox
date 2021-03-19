function openPage(evt, page) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(page).style.display = "block";
    evt.currentTarget.className += " active";
}

function openItemForm() {
    var x = document.getElementById("item_form");
    return openCollapsible(x)
}

function openUserForm() {
    var x = document.getElementById("user_form");
    return openCollapsible(x)
}

function openCollapsible(x) {
    (x.style.display != "block") ? (x.style.display = "block") : (x.style.display = "none");
    return false;
}

function openTab(id) {
    document.getElementById(id).click()
}
function myFunction() {
    // Declare variables
    var input, filter, ul, li, a, i, h;
    input = document.getElementById('search_bar');
    filter = input.value.toUpperCase();
    ul = document.getElementById('myUL')
    li = ul.getElementsByClassName('friends_container');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        a = li[i]
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
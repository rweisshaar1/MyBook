function loadMore(event) {
    console.log('Load More button clicked');
    var hiddenBooks = document.getElementsByClassName('hidden-books');
    for (var i = 0; i < hiddenBooks.length; i++) {
        hiddenBooks[i].style.display = 'block';
    }
    event.target.style.display = 'none';  // Hide the "Load More" button
}
document.getElementById('loadMore').addEventListener('click', function() {
    console.log('Load More button clicked');
    var hiddenBooks = document.getElementsByClassName('hidden-books');
    for (var i = 0; i < hiddenBooks.length; i++) {
        hiddenBooks[i].style.display = 'block';
    }
    this.style.display = 'none';  // Hide the "Load More" button
});
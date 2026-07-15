// Navigation & Search functionality
document.addEventListener('DOMContentLoaded', function() {
  // Mobile nav toggle
  document.querySelectorAll('.nav-toggle').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelector('.nav-list').classList.toggle('open');
    });
  });

  // Load featured articles on homepage from local index
  var featuredGrid = document.getElementById('featured-grid');
  if (featuredGrid) {
    loadFeaturedArticles();
  }

  // Search on articles page
  var searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      filterArticles(this.value);
    });
  }
});

function loadFeaturedArticles() {
  var grid = document.getElementById('featured-grid');
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/articles/index.html');
  xhr.onload = function() {
    if (xhr.status === 200) {
      var parser = new DOMParser();
      var doc = parser.parseFromString(xhr.responseText, 'text/html');
      var list = doc.querySelector('#article-list');
      if (list) {
        var items = list.querySelectorAll('li');
        var html = '';
        var count = 0;
        items.forEach(function(item) {
          if (count >= 6) return;
          var link = item.querySelector('a');
          var desc = item.querySelector('.desc');
          if (link) {
            var title = link.textContent;
            var href = link.getAttribute('href');
            var description = desc ? desc.textContent : title;
            html += '<article class="post-card">' +
              '<div class="post-card-body">' +
              '<h3><a href="' + href + '">' + title + '</a></h3>' +
              '<p>' + description.substring(0, 120) + '</p>' +
              '</div></article>';
            count++;
          }
        });
        if (html) grid.innerHTML = html;
      }
    }
  };
  xhr.send();
}

function filterArticles(query) {
  var items = document.querySelectorAll('#article-list li');
  query = query.toLowerCase().trim();
  items.forEach(function(item) {
    var text = item.textContent.toLowerCase();
    item.style.display = (!query || text.indexOf(query) > -1) ? '' : 'none';
  });
}

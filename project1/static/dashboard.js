document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Mobile sidebar toggle ---------- */
  var menuBtn = document.getElementById('dashMenuBtn');
  var sidebar = document.getElementById('dashSidebar');
  var backdrop = document.getElementById('dashBackdrop');

  function openSidebar() {
    sidebar.classList.add('is-open');
    backdrop.classList.add('is-open');
    menuBtn.setAttribute('aria-expanded', 'true');
  }
  function closeSidebar() {
    sidebar.classList.remove('is-open');
    backdrop.classList.remove('is-open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }
  if (menuBtn && sidebar && backdrop) {
    menuBtn.addEventListener('click', function () {
      sidebar.classList.contains('is-open') ? closeSidebar() : openSidebar();
    });
    backdrop.addEventListener('click', closeSidebar);
  }

  /* ---------- Profile dropdown ---------- */
  var profile = document.getElementById('dashProfile');
  var profileBtn = document.getElementById('dashProfileBtn');
  if (profile && profileBtn) {
    profileBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = profile.classList.toggle('is-open');
      profileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!profile.contains(e.target)) {
        profile.classList.remove('is-open');
        profileBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- Mobile search bar toggle ---------- */
  var searchToggle = document.getElementById('dashSearchToggle');
  var searchBar = document.getElementById('dashSearchBar');
  if (searchToggle && searchBar) {
    searchToggle.addEventListener('click', function () {
      searchBar.classList.toggle('is-open');
      if (searchBar.classList.contains('is-open')) {
        var input = searchBar.querySelector('input');
        if (input) input.focus();
      }
    });
  }

  /* ---------- My Books status filter tabs ----------
     Client-side only for now — swap for a real request (or an
     HTMX/fetch call against a filtered `my_books` endpoint) once
     server-side filtering is wired up. */
  var filterTabs = document.querySelectorAll('.filter-tab');
  var bookCards = document.querySelectorAll('.my-book-card');

  filterTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      filterTabs.forEach(function (t) {
        t.classList.remove('is-active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('is-active');
      tab.setAttribute('aria-selected', 'true');

      var filter = tab.getAttribute('data-filter');
      bookCards.forEach(function (card) {
        var status = card.getAttribute('data-status');
        var matches =
          filter === 'all' ||
          (filter === 'favorites' && card.querySelector('.my-book-card__fav.is-active')) ||
          status === filter;
        card.style.display = matches ? '' : 'none';
      });
    });
  });

  /* ---------- Book action buttons (placeholders) ----------
     These are not wired to endpoints yet — replace with fetch() calls
     to your Django views (e.g. POST to a `toggle_favorite` /
     `mark_completed` / `remove_from_library` URL) once they exist. */
  document.querySelectorAll('[data-action]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var action = btn.getAttribute('data-action');
      var bookId = btn.getAttribute('data-book-id');
      console.log('TODO: wire up "' + action + '" for book', bookId);
    });
  });

});
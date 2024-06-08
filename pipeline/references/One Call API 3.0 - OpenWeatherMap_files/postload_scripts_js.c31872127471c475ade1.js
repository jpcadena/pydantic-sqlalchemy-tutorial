var openMenu = false;
var navigation = document.getElementById("nav-website");
var userDropdown = document.getElementById('user-dropdown-menu');
var supportDropdown = document.getElementById('support-dropdown-menu');

function unfoldMenu() {
  navigation.classList.add('visible');
}

function foldMenu() {
  navigation.classList.remove('visible')
}

function toggleDropdown(el) {
  el.classList.contains('dropdown-visible') ? el.classList.remove('dropdown-visible') : el.classList.add('dropdown-visible')
}

function closePopUps() {
    userDropdown && userDropdown.classList.remove('dropdown-visible')
    supportDropdown.classList.remove('dropdown-visible')
}

function toggleMenu (e) {
    e.stopImmediatePropagation();
    if (e.target) {
      if (e.target.id === 'hamburger' || e.target.parentNode.id === 'hamburger') {
        openMenu = !openMenu;
        openMenu ? unfoldMenu() : foldMenu();
      } else if (!e.target.nodeName === 'input') {
        openMenu = false;
        foldMenu();
      } else if (e.target.id === 'user-dropdown' || e.target.parentNode.id === 'user-dropdown') {
        supportDropdown.classList.remove('dropdown-visible')
        toggleDropdown(userDropdown)
      } else if (e.target.id === 'support-dropdown') {
        userDropdown && userDropdown.classList.remove('dropdown-visible')
        toggleDropdown(supportDropdown)
      } else {
        closePopUps()
      }
    }
  }

// footer
function toggleFooterSection (e) {
    if (e.target && (e.target.className === 'section-heading' || e.target.parentNode.className === 'section-heading')) {
      //locate section
      let section = e.target.className === 'section-heading' ? e.target.parentNode : e.target.parentNode.parentNode;
      if (section.classList.contains('visible')) {
        section.classList.remove('visible')
      } else {
        section.classList.add('visible')
      }
    }
  }
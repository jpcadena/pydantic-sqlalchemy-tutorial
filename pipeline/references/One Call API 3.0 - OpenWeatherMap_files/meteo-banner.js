document.addEventListener('DOMContentLoaded', function () {
  const myPopUp = document.getElementById("meteo-banner");
  const span = document.getElementsByClassName("close-btn")[0];
  const popUpButton = document.getElementById("meteo-banner-button");

  function showPopUp() {
    if (localStorage.getItem('popUpClosed') === 'true') {
      return;
    }
    myPopUp.style.display = "block";
    gtag('event', 'banner_view', {
      'event_category': 'Pop-up',
      'event_label': 'Pop Up Viewed'
    });
  }

  span.onclick = function () {
    myPopUp.style.display = "none";
    localStorage.setItem('popUpClosed', 'true');
    gtag('event', 'banner_close', {
      'event_category': 'Pop-up',
      'event_label': 'Pop Up Closed'
    });
  };


  popUpButton.onclick = function () {
    gtag('event', 'banner_click', {
      'event_category': 'Pop-up',
      'event_label': 'Pop Up Button Clicked'
    });
  };


  window.onscroll = function () {
    if (!myPopUp.style.display || myPopUp.style.display === 'none') {
      if (document.body.scrollTop > 350 || document.documentElement.scrollTop > 350) {
        showPopUp();
      }
    }
  };
});

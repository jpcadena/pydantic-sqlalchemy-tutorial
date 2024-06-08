
var bannerClosed = "owm_banner_android_closed"

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value) {
  var expires = new Date();
  expires.setTime(expires.getTime() + (5 * 1000 * 60 * 60 * 24));
  document.cookie = name + '=' + escape(value) + '; expires=' + expires.toGMTString() + '; path=/';
}

function bannerClose() {
  document.getElementById("banner_android").style.display = "none";
  setCookie(bannerClosed, true);
}

document.onload = function (bannerClosed) {
  if ((document.cookie.indexOf(bannerClosed) === -1) && /Android/i.test(window.navigator.userAgent)) {
    document.getElementById("banner_android").style.display = 'flex';
  }
}(bannerClosed);


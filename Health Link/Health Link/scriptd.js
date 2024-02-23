
function togglePasswordVisibility() {

  var passwordInput = document.getElementById("password");

  var passwordToggle = document.querySelector(".password-toggle");

 

  if (passwordInput.type === "password") {

    passwordInput.type = "text";

    passwordToggle.style.backgroundImage = "url('slashs.png')";

  } else {

    passwordInput.type = "password";

    passwordToggle.style.backgroundImage = "url('eye.png')";

  }

}
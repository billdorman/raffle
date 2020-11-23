  $('#toggle-password').click(function(event) {
    console.log("password toggle");
    let toggleButton = $('#toggle-password');
    let passwordField = $('#password');

    if (passwordField.attr('type') === "password") {
      toggleButton.val("Hide");
      passwordField.attr('type', 'text');
    } else {
      toggleButton.val("Show");
      passwordField.attr('type', 'password');
    }
  });

  // Setup our formatted phone number fields
  let phone = new Cleave('#phone', {
    numericOnly: true,
    blocks: [0, 3, 0, 3, 4],
    delimiters: ["(", ")", " ", "-"],
  });
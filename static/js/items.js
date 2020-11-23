$(document).ready(function() {

  // Check to see if checkout_complete was passed in as a query param. If so, clear our cart from local storage
  // and display a success message
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const checkoutComplete = urlParams.get('checkout_complete');
  if (checkoutComplete && getCartItemCount() > 0) {
    clearCart();
    Swal.fire({
      title: 'Order Placed',
      text: 'Thank you for your support! It may take a few minutes for the order to appear under your account.',
      icon: 'success',
      confirmButtonText: 'Close'
    });
  }

  // Setup our input spinners
  $(".input-spinner").inputSpinner();

  $(".input-spinner").on("change", (event) => {
    let quantity = parseInt(event.target.value);
    let id = parseInt(event.target.getAttribute("data-id"));

    addItemToCart(id, quantity);
  });

  // Display saved cart values from local storage
  let cart = getCartFromLocalStorage();
  cart.forEach(item => {
    $(`.input-spinner[data-id="${item.id}"]`).val(item.quantity);
  });
});
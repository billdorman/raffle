$(document).ready(function() {
  updateCartBadge();
});

function getCartFromLocalStorage() {
  if ("cart" in localStorage)
    return JSON.parse(localStorage.getItem('cart'));
  else {
    return []
  }
}

function clearCart() {
  localStorage.removeItem('cart');
  updateCartBadge();
}

function updateCartBadge() {
  let count = getCartItemCount();
  $('#cart-badge').text(count);
}

function addItemToCart(id, quantity) {
  // Get our shopping cart from local storage
  let cart = getCartFromLocalStorage();

  // Check to see if this item has already been added to the cart. If so, update
  let itemIndex = cart.findIndex(x => x.id === id);

  if (itemIndex >= 0) {
    // Existing item, update
    cart[itemIndex].quantity = quantity;
  }
  else {
    // New item, add to cart
    cart.push({id: id, quantity: quantity});
  }

  // Update local storage
  localStorage.setItem('cart', JSON.stringify(cart));

  updateCartBadge();
}

function startCheckout() {
  let cart = getCartFromLocalStorage();
  let cartCount = getCartItemCount();

  if (cartCount <= 0) {
    alert("Please add at least one item to your cart to proceed.");
    return;
  }

  $.ajax({
    url: '/checkout/start',
    type: 'post',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify({cart: cart}),
    success: function(data) {
      if (data.success) {
        // Redirect to the payment url
        window.location = data.checkout_url
      } else {
        // Error building payment url
        alert(data.errors[0].detail)
      }
    },
    error: function(data) {
      alert("Error loading checkout page. Please try again later.");
    }

  });
}

function getCartItemCount() {
  let cart = getCartFromLocalStorage();
  return cart.reduce((accumulator, current) => accumulator + current.quantity, 0);
}
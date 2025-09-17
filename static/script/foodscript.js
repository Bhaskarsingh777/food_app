// Select modal elements
const loginModal = document.getElementById("loginModal");
const signupModal = document.getElementById("signupModal");
const orderModal = document.getElementById("orderModal");

// Buttons
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const closeLogin = document.getElementById("closeLogin");
const closeSignup = document.getElementById("closeSignup");
const closeOrder = document.getElementById("closeOrder");

// Switch between login/signup
const toSignup = document.getElementById("toSignup");
const toLogin = document.getElementById("toLogin");

// Order buttons
const orderBtns = document.querySelectorAll(".orderBtn");
const orderItemInput = document.getElementById("orderItem");

// Open modals
loginBtn && loginBtn.addEventListener("click", () => loginModal.style.display = "block");
signupBtn && signupBtn.addEventListener("click", () => signupModal.style.display = "block");

// Close modals
closeLogin && closeLogin.addEventListener("click", () => loginModal.style.display = "none");
closeSignup && closeSignup.addEventListener("click", () => signupModal.style.display = "none");
closeOrder && closeOrder.addEventListener("click", () => orderModal.style.display = "none");

// Switch forms
toSignup && toSignup.addEventListener("click", () => {
  loginModal.style.display = "none";
  signupModal.style.display = "block";
});
toLogin && toLogin.addEventListener("click", () => {
  signupModal.style.display = "none";
  loginModal.style.display = "block";
});

// Handle order buttons
orderBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const item = btn.getAttribute("data-item");
    orderItemInput.value = item;
    orderModal.style.display = "block";
  });
});

// Close modal if click outside
window.onclick = function(event) {
  if (event.target === loginModal) loginModal.style.display = "none";
  if (event.target === signupModal) signupModal.style.display = "none";
  if (event.target === orderModal) orderModal.style.display = "none";
};

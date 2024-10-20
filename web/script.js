$(document).ready(function() {
    $('#contactForm').on('submit', function(event) {
      let isValid = true;
      const name = $('#name').val();
      const email = $('#email').val();
  
      if (!name) {
        alert("Name is required");
        isValid = false;
      }
  
      const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
      if (!email.match(emailPattern)) {
        alert("Enter a valid email");
        isValid = false;
      }
  
      if (!isValid) {
        event.preventDefault();
      }
    });
  });
  
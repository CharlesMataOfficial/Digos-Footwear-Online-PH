document.getElementById('login-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = '';

  try {
    const response = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    
        const text = await response.text();  // read raw text once

        let data;
        try {
            data = JSON.parse(text);  // try to parse JSON manually
        } catch {
            console.error("Response is not valid JSON:", text);
            errorMessage.textContent = 'Server error: unexpected response.';
            return;
        }

        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            const userRole = data.user.role.toLowerCase();
            if (userRole === 'buyer') {
                window.location.href = 'buyers/dashboard/';  // adjust to your buyer page URL
            } else if (userRole === 'seller') {
                window.location.href = '/seller/dashboard/';  // adjust as needed
            } else {
                window.location.href = '/dashboard/';  // fallback/default page
            }
        } else {
            errorMessage.textContent = data.detail || 'Login failed';
        }
    } catch (error) {
        errorMessage.textContent = 'An error occurred. Please try again.';
        console.error('Login error:', error);
    }
});

function openSignupModal() {
    document.getElementById('signup-modal').style.display = 'block';
}

function closeSignupModal() {
    document.getElementById('signup-modal').style.display = 'none';
}

document.getElementById('signup-modal').addEventListener('submit', async function (e) {
    e.preventDefault();  // Prevent the page from reloading

    // Get form field values
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const password2 = document.getElementById('signup-password2').value;
    const role = document.getElementById('signup-role').value;
    const address = document.getElementById('signup-address').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Sending JSON data
            },
            body: JSON.stringify({
                username,
                email,
                password,
                password2,
                role,
                address,
            })
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message || "Registered successfully!");
            // You can redirect the user or reset the form here
        } else {
            const errors = await response.json();
            console.error(errors);
            alert("Registration failed. See console for details.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Try again later.");
    }
  });
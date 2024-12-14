// Fetch users and populate the table
async function fetchUsers() {
    const response = await fetch('/users/');
    const users = await response.json();
    const tableBody = document.getElementById('user-table-body');
    
    tableBody.innerHTML = '';  // Clear any existing rows

    // Add each user to the table
    users.forEach(user => {
        const row = `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.is_active ? 'Yes' : 'No'}</td>
                <td>${user.is_admin ? 'Yes' : 'No'}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Load users when the page is loaded
window.onload = fetchUsers;

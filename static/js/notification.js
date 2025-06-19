const CSRF_TOKEN = document.getElementById('csrfToken').value
document.getElementById('markAllRead').addEventListener('click', function() {
    fetch("{% url 'mark_all_notifications_as_read' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelectorAll('.today-notif-container').forEach(el => {
                el.classList.remove('unread');
                el.classList.add('read');
            });
        }
    })
    .catch(err => console.error('Error:', err));
});

// scripts.js

document.querySelectorAll('.filter-button').forEach(button => {
    button.addEventListener('click', () => {
        const status = button.getAttribute('data-status');
        document.querySelectorAll('.filter-button').forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        document.querySelectorAll('.data-row').forEach(row => {
            row.style.display = (status === 'todos' || row.getAttribute('data-status') === status) ? '' : 'none';
        });
    });
});

document.querySelectorAll('.show-details').forEach(link => {
    link.addEventListener('click', () => {
        const detailsRow = link.closest('.data-row').nextElementSibling;
        if (detailsRow && detailsRow.classList.contains('details-row')) {
            detailsRow.style.display = detailsRow.style.display === 'none' || detailsRow.style.display === '' ? 'table-row' : 'none';
        }
    });
});

$(document).ready(function() {
    var table = $('#grilleTable').DataTable({
        dom: 'Bfrtip',
        buttons: [
            { extend: 'csvHtml5', text: 'CSV', className: 'd-none', exportOptions: {columns: ':visible'} },
            { extend: 'excelHtml5', text: 'Excel', className: 'd-none', exportOptions: {columns: ':visible'} },
            { extend: 'pdfHtml5', text: 'PDF', className: 'd-none', exportOptions: {columns: ':visible'} },
            { extend: 'print', text: 'Imprimer', className: 'd-none', exportOptions: {columns: ':visible'} }
        ],
        language: {
            url: "/static/i18n/fr-FR.json"
        },
        paging: false, // Masque la pagination
        info: false    // Masque le texte "Showing x to x of x entries"
    });

    // Exports custom buttons
    $('#export-csv').on('click', function() { table.button(0).trigger(); });
    $('#export-excel').on('click', function() { table.button(1).trigger(); });
    $('#export-pdf').on('click', function() { table.button(2).trigger(); });

    // Filtres dynamiques
    $('#filter-matricule, #filter-nom, #filter-contact').on('input', function() {
        var matricule = $('#filter-matricule').val().toLowerCase();
        var nom = $('#filter-nom').val().toLowerCase();
        var contact = $('#filter-contact').val().toLowerCase();

        $('#grilleTable tbody tr').each(function() {
            var tds = $(this).find('td');
            var show = true;
            if (matricule && !tds.eq(0).text().toLowerCase().includes(matricule)) show = false;
            if (nom && !tds.eq(1).text().toLowerCase().includes(nom)) show = false;
            if (contact && !tds.eq(2).text().toLowerCase().includes(contact)) show = false;
            $(this).toggle(show);
        });
    });
});
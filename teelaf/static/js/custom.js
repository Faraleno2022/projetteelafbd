$(document).ready(function() {
    // --- Validation en temps réel sur tous les champs du formulaire ---
    $('.form-control').on('input', function() {
        if ($(this).val().trim().length > 0) {
            $(this).removeClass('is-invalid');
        }
    });

    // Validation en temps réel sur les champs de type date
    $('input[type="date"]').on('change', function() {
        if ($(this).val()) {
            $(this).removeClass('is-invalid');
        }
    });

    // --- Initialisation DataTable pour la liste des clients individuels ---
    if ($('#table-clients').length) {
        var table = $('#table-clients').DataTable({
            dom: 'Bfrtip',
            buttons: [
                { extend: 'excelHtml5', className: 'd-none', title: 'Clients Individuels' },
                { extend: 'pdfHtml5', className: 'd-none', title: 'Clients Individuels' },
                { extend: 'csvHtml5', className: 'd-none', title: 'Clients Individuels' }
            ],
            lengthChange: false,
            paging: true,
            info: true,
            searching: true,
            language: {
                search: "Rechercher&nbsp;:",
                paginate: {
                    previous: "Précédent",
                    next: "Suivant"
                },
                info: "Affichage de _START_ à _END_ sur _TOTAL_ clients",
                infoEmpty: "Aucun client à afficher",
                zeroRecords: "Aucun résultat trouvé"
            }
        });

        // Lier les boutons custom aux boutons DataTables
        $('#btn-excel').on('click', function() {
            table.button('.buttons-excel').trigger();
        });
        $('#btn-pdf').on('click', function() {
            table.button('.buttons-pdf').trigger();
        });
        $('#btn-csv').on('click', function() {
            table.button('.buttons-csv').trigger();
        });
    }

    // --- Initialisation DataTable pour la liste des entreprises (si besoin) ---
    if ($('#table-clients-entreprises').length) {
        var tableEnt = $('#table-clients-entreprises').DataTable({
            dom: 'Bfrtip',
            buttons: [
                { extend: 'excelHtml5', className: 'd-none', title: 'Clients Entreprises' },
                { extend: 'pdfHtml5', className: 'd-none', title: 'Clients Entreprises' },
                { extend: 'csvHtml5', className: 'd-none', title: 'Clients Entreprises' }
            ],
            lengthChange: false,
            paging: false, // Pagination Django pour entreprises
            info: false,
            searching: true,
            language: {
                search: "Rechercher :",
                paginate: {
                    previous: "Précédent",
                    next: "Suivant"
                },
                info: "Affichage de _START_ à _END_ sur _TOTAL_ entreprises",
                infoEmpty: "Aucune entreprise à afficher",
                zeroRecords: "Aucun résultat trouvé"
            }
        });

        // Lier les boutons custom aux boutons DataTables (si présents)
        $('#btn-excel-entreprises').on('click', function() {
            tableEnt.button('.buttons-excel').trigger();
        });
        $('#btn-pdf-entreprises').on('click', function() {
            tableEnt.button('.buttons-pdf').trigger();
        });
        $('#btn-csv-entreprises').on('click', function() {
            tableEnt.button('.buttons-csv').trigger();
        });
    }
});
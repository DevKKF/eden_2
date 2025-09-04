$(document).ready(function () {
    $('#sessions_datatables').DataTable();
    $('#certificat_sessions_datatables').DataTable();
    $('#cours_sessions_datatables').DataTable();
    $('#cheminant_sessions_datatables').DataTable();
    $('#table_reponses').DataTable();
    $('#example2').DataTable({
        'paging': true,
        'lengthChange': false,
        'searching': false,
        'ordering': true,
        'info': true,
        'autoWidth': false
    });
});
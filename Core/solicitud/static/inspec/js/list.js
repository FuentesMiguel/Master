/*Script que funciona para listar las Solicitudes*/
$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { data: 'Sembrador_user__id' }, // Campo relacionado
            { data: 'Sembrador_user__username' }, // Campo relacionado
            { data: 'Sembrador_user__first_name' }, // Campo relacionado
            { data: 'Sembrador_user__last_name' }, // Campo relacionado
            { data: 'Sembrador_user__cedula' }, // Campo relacionado
            { data: 'nombre_unidad' },
            { data: "Opciones"},
        
        ],
        columnDefs: [

            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/user/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/user/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
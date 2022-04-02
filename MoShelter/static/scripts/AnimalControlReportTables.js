// // Call the dataTables jQuery plugin
// $(document).ready(function () {
//     $('#DogDashboard').DataTable({
//         "ajax": "/restApi/Dog/GetDashboard",
//         "columnDefs": [
//             {
//                 "targets": [0],
//                 "visible": false,
//                 "searchable": false
//             },
//             {
//                 "targets": [1],
//                 "data": [1],
//                 "render": function (data, type, row, meta) {
//                     return '<a href="/DogDetail?dogId=' + row[0] + '">' + data + '</a>';
//                 }
//             },
//             {
//                 "targets": [3],
//                 "data": [3],
//                 "render": function (data, type, row, meta) {
//                     if (data == 1)
//                         return 'True'
//                     else
//                         return 'False'
//                 }
//             },
//             {
//                 "targets": [7],
//                 "data": [7],
//                 "render": function (data, type, row, meta) {
//                     if (data == 1)
//                         return '<div class="alert alert-success" role="alert">Adoptable</div>'
//                     else
//                         return '<div class="alert alert-danger" role="alert">NotAdoptable</div>'
//                 }
//             }
//         ],
//         "order": []
//     });

//     var pendingData = $('#PendingApplicationDashboard').DataTable({
//         "ajax": "/restApi/Application/GetApplications?type=pending",
//         "columnDefs": [
//             {
//                 "targets": 0,
//                 "class": "details-control",
//                 "orderable": false,
//                 "data": null,
//                 "defaultContent": ""
//             },
//             { "targets": 1, "data": [0] },
//             { "targets": 2, "data": [1] },
//             { "targets": 3, "data": [2] },
//             { "targets": 4, "data": [3] },
//             { "targets": 5, "data": [4] },
//             { "targets": 6, "data": [5] },
//             {
//                 "targets": -1,
//                 "orderable": false,
//                 "data": null,
//                 "defaultContent": "<button class=\"btn btn-success Approve\"><i class=\"fas fa-check\"></i></button>\
//                     <button class=\"btn btn-danger Reject\"><i class=\"fas fa-times\"></i></button>"
//             }
//         ],
//         "order": []
//     });

//     var approvedData = $('#ApprovedApplicationDashboard').DataTable({
//         "ajax": "/restApi/Application/GetApplications?type=approved",
//         "columnDefs": [
//             {
//                 "targets": 0,
//                 "class": "details-control",
//                 "orderable": false,
//                 "data": null,
//                 "defaultContent": ""
//             },
//             { "targets": 1, "data": [0] },
//             { "targets": 2, "data": [1] },
//             { "targets": 3, "data": [2] },
//             { "targets": 4, "data": [3] },
//             { "targets": 5, "data": [4] },
//             { "targets": 6, "data": [5] }
//         ],
//         "order": []
//     });

//     var rejectedData = $('#RejectedApplicationDashboard').DataTable({
//         "ajax": "/restApi/Application/GetApplications?type=rejected",
//         "columnDefs": [
//             {
//                 "targets": 0,
//                 "class": "details-control",
//                 "orderable": false,
//                 "data": null,
//                 "defaultContent": ""
//             },
//             { "targets": 1, "data": [0] },
//             { "targets": 2, "data": [1] },
//             { "targets": 3, "data": [2] },
//             { "targets": 4, "data": [3] },
//             { "targets": 5, "data": [4] },
//             { "targets": 6, "data": [5] }
//         ],
//         "order": []
//     });

//     $('#PendingApplicationDashboard tbody').on('click', 'button', function () {
//         var data = pendingData.row($(this).parents('tr')).data();

//         revtype = "";
//         if (this.classList.contains("Approve"))
//             revtype = "Approve";
//         else
//             revtype = "Reject";
//         $.ajax({
//             url: '/restApi/Application/ReviewApplication',
//             type: 'POST',
//             data: {
//                 'appNo': data[1],
//                 'type': revtype,
//                 'email': data[4]
//             },
//             dataType: 'json',
//             success: function (result) {
//                 location.reload();
//             },
//             error: function (request, error) {
//                 alert("Request: Was Not Accepted");
//             }
//         });

//     });

//     function format(d) {
//         str = 'Co-Applicant Name: ';
//         if (d[10]){
//             str = str + d[10] + ' ' + d[11] + '<br>';
//         }
//         return 'Applicant Address: ' + d[6] + ' ' + d[7] + ', ' + d[8] + ' '+ d[9] +'<br>' + str;
//     }

//     $('#PendingApplicationDashboard tbody').on('click', 'td.details-control', function () {
//         var tr = $(this).closest('tr');
//         var row = pendingData.row(tr);

//         if (row.child.isShown()) {
//             // This row is already open - close it
//             row.child.hide();
//             tr.removeClass('shown');
//         }
//         else {
//             // Open this row
//             row.child(format(row.data())).show();
//             tr.addClass('shown');
//         }
//     });
//     $('#ApprovedApplicationDashboard tbody').on('click', 'td.details-control', function () {
//         var tr = $(this).closest('tr');
//         var row = approvedData.row(tr);

//         if (row.child.isShown()) {
//             // This row is already open - close it
//             row.child.hide();
//             tr.removeClass('shown');
//         }
//         else {
//             // Open this row
//             row.child(format(row.data())).show();
//             tr.addClass('shown');
//         }
//     });
//     $('#RejectedApplicationDashboard tbody').on('click', 'td.details-control', function () {
//         var tr = $(this).closest('tr');
//         var row = rejectedData.row(tr);

//         if (row.child.isShown()) {
//             // This row is already open - close it
//             row.child.hide();
//             tr.removeClass('shown');
//         }
//         else {
//             // Open this row
//             row.child(format(row.data())).show();
//             tr.addClass('shown');
//         }
//     });

//     // Table structure for animal control report -> surrendered dogs
//     var surrenderData = $('#SurrenderedDogMonth1').DataTable({
//         "ajax": "/Report/GetAnimalControlReport1?type=surrender",
//         "columnDefs": [
//             { "targets": 0, "data": [1] },
//             { "targets": 1, "data": [2] },
//             { "targets": 2, "data": [3] },
//             { "targets": 3, "data": [4] },
//             { "targets": 4, "data": [5] },
//             { "targets": 5, "data": [6] }
//         ],
//         "order": []
//     });

//     // var surrenderData_1 = surrenderData
//     //     .column(0)
//     //     .data()
//     //     .filter( function (value, index) {
//     //         return value == 6 ? true : false;
//     //     });


//     var surrenderData_2 = $('#SurrenderedDogMonth2').DataTable({
//         "ajax": "/Report/GetAnimalControlReport2?type=surrender",
//         "columnDefs": [
//             { "targets": 0, "data": [1] },
//             { "targets": 1, "data": [2] },
//             { "targets": 2, "data": [3] },
//             { "targets": 3, "data": [4] },
//             { "targets": 4, "data": [5] },
//             { "targets": 5, "data": [6] }
//         ],
//         "order": []
//     });

//     // Table structure for animal control report -> dog expenses
//     var expenseData_1 = $('#ExpenseMonth1').DataTable({
//         "ajax": "/Report/GetAnimalControlReport1?type=expense",
//         "columnDefs": [
//             { "targets": 0, "data": [1] },
//             { "targets": 1, "data": [2] },
//             { "targets": 2, "data": [3] },
//             { "targets": 3, "data": [4] },
//             { "targets": 4, "data": [5] },
//             { "targets": 5, "data": [6] },
//             { "targets": 6, "data": [7] }
//         ],
//         "order": []
//     });

//     var expenseData_2 = $('#ExpenseMonth2').DataTable({
//         "ajax": "/Report/GetAnimalControlReport2?type=expense",
//         "columnDefs": [
//             { "targets": 0, "data": [1] },
//             { "targets": 1, "data": [2] },
//             { "targets": 2, "data": [3] },
//             { "targets": 3, "data": [4] },
//             { "targets": 4, "data": [5] },
//             { "targets": 5, "data": [6] },
//             { "targets": 6, "data": [7] }
//         ],
//         "order": []
//     });

// });

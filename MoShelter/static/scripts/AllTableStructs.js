// Call the dataTables jQuery plugin
$(document).ready(function () {

    $('#searchMe').click(function () {
        $('#appNum').val('');
        $('#applicantName').val('');
        $('#coApplicantName').val('');
        $('#applicantEmail').val('');
        $('#applicantPhone').val('');
        $('#applicantAddress').val('');
        applicantsNamesForAdopt.ajax.reload();
    });

    $('#searchVolunteer').click(function () {
        volunteerLookupData.ajax.reload();
    });

    $('#DogDashboard').DataTable({
        "ajax": "/restApi/Dog/GetDashboard",
        "columnDefs": [
            {
                "targets": [0],
                "visible": false,
                "searchable": false
            },
            {
                "targets": [1],
                "data": [1],
                "render": function (data, type, row, meta) {
                    return '<a href="/DogDetail?dogId=' + row[0] + '">' + data + '</a>';
                }
            },
            {
                "targets": [3],
                "data": [3],
                "render": function (data, type, row, meta) {
                    if (data == 1)
                        return 'True'
                    else
                        return 'False'
                }
            },
            {
                "targets": [4],
                "data": [5]
            },
            {
                "targets": [5],
                "data": [6]
            },
            {
                "targets": [6],
                "data": null,
                "render": function (data, type, row, meta) {
                    if (data[7] == 1)
                        return '<div class="alert alert-success" role="alert">Adoptable</div>'
                    else
                        return '<div class="alert alert-danger" role="alert">Not Adoptable</div>'
                }
            }
        ],
        "order": []
    });

    var pendingData = $('#PendingApplicationDashboard').DataTable({
        "ajax": "/restApi/Application/GetApplications?type=pending",
        "columnDefs": [
            {
                "targets": 0,
                "class": "details-control",
                "orderable": false,
                "data": null,
                "defaultContent": ""
            },
            { "targets": 1, "data": [0] },
            { "targets": 2, "data": [1] },
            { "targets": 3, "data": [2] },
            { "targets": 4, "data": [3] },
            { "targets": 5, "data": [4] },
            { "targets": 6, "data": [5] },
            {
                "targets": -1,
                "orderable": false,
                "data": null,
                "defaultContent": "<button class=\"btn btn-success Approve\"><i class=\"fas fa-check\"></i></button>\
                    <button class=\"btn btn-danger Reject\"><i class=\"fas fa-times\"></i></button>"
            }
        ],
        "order": []
    });

    var approvedData = $('#ApprovedApplicationDashboard').DataTable({
        "ajax": "/restApi/Application/GetApplications?type=approved",
        "columnDefs": [
            {
                "targets": 0,
                "class": "details-control",
                "orderable": false,
                "data": null,
                "defaultContent": ""
            },
            { "targets": 1, "data": [0] },
            { "targets": 2, "data": [1] },
            { "targets": 3, "data": [2] },
            { "targets": 4, "data": [3] },
            { "targets": 5, "data": [4] },
            { "targets": 6, "data": [5] }
        ],
        "order": []
    });

    var approvedAdoptionData = $('#ApprovedApplicationAdoption').DataTable({
        "ajax": "/restApi/Application/GetApplications?type=approved",
        "columnDefs": [
            {
                "targets": 0,
                "class": "details-control",
                "orderable": false,
                "data": null,
                "defaultContent": ""
            },
            { "targets": 1, "data": [0] },
            { "targets": 2, "data": [1] },
            { "targets": 3, "data": [2] },
            { "targets": 4, "data": [3] },
            { "targets": 5, "data": [4] },
            { "targets": 6, "data": [5] }
        ],
        "order": []
    });

    var rejectedData = $('#RejectedApplicationDashboard').DataTable({
        "ajax": "/restApi/Application/GetApplications?type=rejected",
        "columnDefs": [
            {
                "targets": 0,
                "class": "details-control",
                "orderable": false,
                "data": null,
                "defaultContent": ""
            },
            { "targets": 1, "data": [0] },
            { "targets": 2, "data": [1] },
            { "targets": 3, "data": [2] },
            { "targets": 4, "data": [3] },
            { "targets": 5, "data": [4] },
            { "targets": 6, "data": [5] }
        ],
        "order": []
    });

    var expensesData = $('#getDogExpensesTable').DataTable({
        "ajax": "/restApi/Dog/GetExpenses?dogId=" + $('#dogId').val(),
        "columnDefs": [
            {
                "targets": 0,
                "class": "details-control",
                "orderable": false,
                "data": null,
                "defaultContent": ""
            },
            { "targets": 1, "data": [0] },
            { "targets": 2, "data": [1] },
            { "targets": 3, "data": [2] }
        ],
        "order": []
    });

    var applicantsNamesForAdopt = $('#getApplicantNames').DataTable({
        "ajax":{
            "url": "/restApi/Application/GetApplicantInfoForAdoption",
            "data": function (d) {
                d.name = $('#nameSearch').val();
            },
        },
        "columnDefs": [
            {
                "targets": 0,
                "class": "details-control",
                "orderable": false,
                "data": null,
                "defaultContent": ""
            },
            { "targets": 1, "data": [0] },
            { "targets": 2, "data": [1] },
            {
                "targets": 3,
                "data": [3],
                "render": function (data, type, row, meta) {
                    return row[2] + ' ' + data
                }
            },
            {
                "targets": 4,
                "data": [5],
                "render": function (data, type, row, meta) {
                    return row[4] + ' ' + data
                }
            },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] },
            {
                "targets": -1,
                "orderable": false,
                "data": null,
                "defaultContent": "<button type=\"button\" class=\"btn btn-primary\">Select</button>"
            }
        ],
        "order": []
    });

    $('#getApplicantNames tbody').on('click', 'button', function () {
        var data = applicantsNamesForAdopt.row($(this).parents('tr')).data();
        if ($(this).closest('tr').hasClass('selected')) {
            $(this).closest('tr').removeClass('selected');
            $('#appNum').val('');
            $('#applicantName').val('');
            $('#coApplicantName').val('');
            $('#applicantEmail').val('');
            $('#applicantPhone').val('');
            $('#applicantAddress').val('');
        }
        else {
            applicantsNamesForAdopt.$('tr.selected').removeClass('selected');
            $(this).closest('tr').addClass('selected');
            $('#appNum').val(data[1]);
            $('#applicantName').val(data[2] + ' ' + data[3]);
            $('#coApplicantName').val(data[4] + ' ' + data[5]);
            $('#applicantEmail').val(data[6]);
            $('#applicantPhone').val(data[7]);
            $('#applicantAddress').val(data[8] + ' ' + data[9] + ', ' + data[10] + ' ' + data[11]);
        }

    });

    $('#PendingApplicationDashboard tbody').on('click', 'button', function () {
        var data = pendingData.row($(this).parents('tr')).data();

        revtype = "";
        if (this.classList.contains("Approve"))
            revtype = "Approve";
        else
            revtype = "Reject";
        $.ajax({
            url: '/restApi/Application/ReviewApplication',
            type: 'POST',
            data: {
                'appNo': data[1],
                'type': revtype,
                'email': data[4]
            },
            dataType: 'json',
            success: function (result) {
                location.reload();
            },
            error: function (request, error) {
                alert("Request: Was Not Accepted");
            }
        });

    });

    $('#ApprovedApplicationAdoption tbody').on('click', 'button', function () {
        var data = approvedAdoptionData.row($(this).parents('tr')).data();
        var dogId = $('#dogId').val();
        revtype = data[1];
        $.ajax({
            url: '/restApi/Application/AddAdoption',
            type: 'POST',
            data: {
                'appNo': data[1],
                'dogId': dogId
            },
            dataType: 'json',
            success: function (result) {
                location.reload();
            },
            error: function (request, error) {
                alert("Request: Was Not Accepted");
            }
        });

    });

    function format(d) {
        str = 'Co-Applicant Name: ';
        if (d[10]){
            str = str + d[10] + ' ' + d[11] + '<br>';
        }
        return 'Applicant Address: ' + d[6] + ' ' + d[7] + ', ' + d[8] + ' '+ d[9] +'<br>' + str;
    }

    function format2(d) {
        return 'Optional Description: ' + d[3];
    }

    function format3(d) {
        return 'Applicant Address: ' + d[8] + ' ' + d[9] + ', ' + d[10] + ' ' + d[11] + '<br>';
    }

    $('#getApplicantNames tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = applicantsNamesForAdopt.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format3(row.data())).show();
            tr.addClass('shown');
        }
    });

    $('#PendingApplicationDashboard tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = pendingData.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
    $('#ApprovedApplicationDashboard tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = approvedData.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
    $('#ApprovedApplicationAdoption tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = approvedAdoptionData.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
    $('#RejectedApplicationDashboard tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = rejectedData.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
    $('#getDogExpensesTable tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = expensesData.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format2(row.data())).show();
            tr.addClass('shown');
        }
    });

    // Table structure for animal control report -> surrendered dogs
    var surrenderData_1 = $('#SurrenderedDogMonth1').DataTable({
        "ajax": "/Report/GetAnimalControlReport1?type=surrender",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] }
        ],
        "order": []
    });

    var surrenderData_2 = $('#SurrenderedDogMonth2').DataTable({
        "ajax": "/Report/GetAnimalControlReport2?type=surrender",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] }
        ],
        "order": []
    });

    var surrenderData_3 = $('#SurrenderedDogMonth3').DataTable({
        "ajax": "/Report/GetAnimalControlReport3?type=surrender",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] }
        ],
        "order": []
    });

    var surrenderData_4 = $('#SurrenderedDogMonth4').DataTable({
        "ajax": "/Report/GetAnimalControlReport4?type=surrender",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] }
        ],
        "order": []
    });

    var surrenderData_5 = $('#SurrenderedDogMonth5').DataTable({
        "ajax": "/Report/GetAnimalControlReport5?type=surrender",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] }
        ],
        "order": []
    });

    var surrenderData_6 = $('#SurrenderedDogMonth6').DataTable({
        "ajax": "/Report/GetAnimalControlReport6?type=surrender",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] }
        ],
        "order": []
    });

    var surrenderData_7 = $('#SurrenderedDogMonth7').DataTable({
        "ajax": "/Report/GetAnimalControlReport7?type=surrender",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] }
        ],
        "order": []
    });

    // Table structure for animal control report -> dog expenses
    var expenseData_1 = $('#ExpenseMonth1').DataTable({
        "ajax": "/Report/GetAnimalControlReport1?type=expense",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var expenseData_2 = $('#ExpenseMonth2').DataTable({
        "ajax": "/Report/GetAnimalControlReport2?type=expense",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var expenseData_3 = $('#ExpenseMonth3').DataTable({
        "ajax": "/Report/GetAnimalControlReport3?type=expense",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var expenseData_4 = $('#ExpenseMonth4').DataTable({
        "ajax": "/Report/GetAnimalControlReport4?type=expense",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var expenseData_5 = $('#ExpenseMonth5').DataTable({
        "ajax": "/Report/GetAnimalControlReport5?type=expense",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var expenseData_6 = $('#ExpenseMonth6').DataTable({
        "ajax": "/Report/GetAnimalControlReport6?type=expense",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var expenseData_7 = $('#ExpenseMonth7').DataTable({
        "ajax": "/Report/GetAnimalControlReport7?type=expense",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    // Table structure for animal control report -> dog rescue
    var rescueData_1 = $('#RescueMonth1').DataTable({
        "ajax": "/Report/GetAnimalControlReport1?type=rescue",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var rescueData_2 = $('#RescueMonth2').DataTable({
        "ajax": "/Report/GetAnimalControlReport2?type=rescue",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var rescueData_3 = $('#RescueMonth3').DataTable({
        "ajax": "/Report/GetAnimalControlReport3?type=rescue",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var rescueData_4 = $('#RescueMonth4').DataTable({
        "ajax": "/Report/GetAnimalControlReport4?type=rescue",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var rescueData_5 = $('#RescueMonth5').DataTable({
        "ajax": "/Report/GetAnimalControlReport5?type=rescue",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var rescueData_6 = $('#RescueMonth6').DataTable({
        "ajax": "/Report/GetAnimalControlReport6?type=rescue",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    var rescueData_7 = $('#RescueMonth7').DataTable({
        "ajax": "/Report/GetAnimalControlReport7?type=rescue",
        "columnDefs": [
            { "targets": 0, "data": [1] },
            { "targets": 1, "data": [2] },
            { "targets": 2, "data": [3] },
            { "targets": 3, "data": [4] },
            { "targets": 4, "data": [5] },
            { "targets": 5, "data": [6] },
            { "targets": 6, "data": [7] }
        ],
        "order": []
    });

    // Table structure for expense analysis report
    var expenseAnalysisData = $('#ExpenseAnalysis').DataTable({
        "ajax": "/Report/GetExpenseAnalysisReport",
        "columnDefs": [
            { "targets": 0, "data": [0] },
            { "targets": 1, "data": [1] }
        ],
        "order": []
    });

    // Table structure for volunteer lookup report
    var volunteerLookupData = $('#VolunteerLookup').DataTable({
        "ajax": {
            "url": "/Report/GetVolunteerLookupReport",
            "data": function (d) {
                d.name = $('#nameSearch').val();
            },
        },
        "columnDefs": [
            { "targets": 0, "data": [0] },
            { "targets": 1, "data": [1] },
            { "targets": 2, "data": [2] },
            { "targets": 3, "data": [3] }
        ],
        "order": []
    });

    $('#MonthlyAdoption').DataTable({
        "ajax": "/Report/GetMonthlyAdoptionReport",
        "columnDefs": [
            { "targets": 0, "data": [0] },
            { "targets": 1, "data": [1] },
            { "targets": 2, "data": [2] },
            { "targets": 3, "data": [3] },
            { "targets": 4, "data": [4] },
            { "targets": 5, "data": [5] },
            { "targets": 6, "data": [6] }
        ],
        "order": []
    });

});

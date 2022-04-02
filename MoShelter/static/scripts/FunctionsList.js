$(document).ready(function () {
    var typingTimer;                //timer identifier
    var doneTypingInterval = 50000; 
    $('#emailValidationShow').hide();

    $('#breed').selectpicker();

    $('#breed').change(function () {
        ValidateDogName($('#dogName').val());
        if ($('#breed').val() != '') {
            $('#breedInputCheck').prop('required', false);
        }
        else {
            $('#breedInputCheck').prop('required', true);
        }
    });

    $('#vendor').selectpicker();

    $("#state").change(function () {
        $('#realstate').val($('#state').val())
    });

    $('#addAdoptionFormSub').click( function () {
        var validate = true
        $('input:required').each(function () {
            if ($(this).val() === '') {
                validate = false;
                return false;
            }
        });
        if (validate == true) {
            $.ajax({
                url: '/restApi/Application/AddAdoption',
                type: 'POST',
                data: $("#applicationForm").serialize(),
                dataType: 'json',
                success: function (result) {
                    var href = $('#dogDetailHref').attr("href");
                    $('#dogDetailHref').attr("href", href + result);
                    $('#addedBody').text("Please make sure all of the required fields have been populated");
                    $('#added').modal('show');
                },
                error: function (request, error) {
                    alert("Request: Was Not Accepted");
                }
            });
        }
        else {
            $('#addedBodyError').text("Please make sure all of the required fields have been populated");
            $('#error').modal('show');
        }
    });

    $('#addDog').click(function () {
        var validate = true
        $('input:required, textarea:required, select:required').each(function () {
            if ($(this).val() === '') {
                validate = false;
                return false;
            }
        });
        if (validate == true) {
            $.ajax({
                url: '/restApi/Dog/AddDog',
                type: 'POST',
                data: $("#addDogForm").serialize(),
                dataType: 'json',
                success: function (result) {
                    var href = $('#dogDetailHref').attr("href");
                    $('#dogDetailHref').attr("href", href + result);
                    $('#addedBody').text("The new dog information has been successfully entered into the system");
                    $('#added').modal({ backdrop: 'static', keyboard: false });
                    $('#added').modal('show');
                },
                error: function (request, error) {
                    alert("Request: Was Not Accepted");
                }
            });
        }
        else {
            $('#addedBodyError').text("Please make sure all of the required fields have been populated");
            $('#error').modal('show');
        }
    });

    $('#editDog').click(function () {
        var validate = true
        $('input:required, textarea:required, select:required').each(function () {
            if ($(this).val() === '') {
                validate = false;
                return false;
            }
        });
        if (validate == true) {
            $.ajax({
                url: '/restApi/Dog/EditDog',
                type: 'POST',
                data: $("#editDogForm").serialize(),
                dataType: 'json',
                success: function (result) {
                    $('#addedBody').text(result);
                    $('#added').modal({ backdrop: 'static', keyboard: false });
                    $('#added').modal('show');
                },
                error: function (request, error) {
                    alert("Request: Was Not Accepted");
                }
            });
        }
        else {
            $('#addedBodyError').text("Please make sure all of the required fields have been populated");
            $('#error').modal('show');
        }
    });

    $("#addApplication").click(function () {
        var validate = true
        $('input:required,  select:required').each(function () {
            if ($(this).val() === '') {
                validate = false;
                return false;
            }
        });
        if (validate == true) {
            $.ajax({
                type: "POST",
                url: "/restApi/Application/AddApplication",
                data: $("#applicationForm").serialize(),
                success: function (response) {
                    $('.readOnlyFields').prop("readonly", false);
                    $('#state').prop("disabled", false);
                    $('#firstName').val("");
                    $('#lastName').val("");
                    $('#street').val("");
                    $('#city').val("");
                    $('#state').val("");
                    $('#realstate').val("");
                    $('#zipCode').val("");
                    $('#phone').val("");
                    $('#hasBeenRetrieved').val("false")
                    $('#ApplicantEmail').val("");
                    $('#datePick').val("");
                    $('#emailValidationShow').hide();
                    $('#addedBody').text("Application Number: " + response + "  was successfully created");
                    $('#added').modal('show');

                }
            });
        }
        else {
            $('#addedBodyError').text("Please make sure all of the required fields have been populated");
            $('#error').modal('show');
        }
    });

    $('#addExpense').click(function () {
        var validate = true
        $('input:required, textarea:required, select:required').each(function () {
            if ($(this).val() === '') {
                validate = false;
                return false;
            }
        });
        if (validate == true) {
            $.ajax({
                url: '/restApi/Dog/AddExpense',
                type: 'POST',
                data: $("#addExpenseForm").serialize(),
                dataType: 'json',
                success: function (result) {
                    var href = $('#dogDetailHref').attr("href");
                    $('#dogDetailHref').attr("href", href + result);
                    $('#addedBody').text("The new dog expense has been successfully entered into the system");
                    $('#added').modal({ backdrop: 'static', keyboard: false });
                    $('#added').modal('show');
                },
                error: function (request, error) {
                    alert("Request: Was Not Accepted");
                }
            });
        }
        else {
            $('#addedBodyError').text("Please make sure all of the required fields have been populated");
            $('#error').modal('show');
        }
    });

    $('#addAdoption').click(function () {
        var validate = true
        $('input:required, textarea:required, select:required').each(function () {
            if ($(this).val() === '') {
                validate = false;
                return false;
            }
        });
        if (validate == true) {
            $.ajax({
                url: '/restApi/Dog/AddAdoption',
                type: 'POST',
                data: $("#addAdoptionForm").serialize(),
                dataType: 'json',
                success: function (result) {
                    var href = $('#dogDetailHref').attr("href");
                    $('#dogDetailHref').attr("href", href + $('#dogId').val());
                    $('#addedBody').text(result);
                    $('#added').modal({ backdrop: 'static', keyboard: false });
                    $('#added').modal('show');
                },
                error: function (request, error) {
                    alert("Request: Was Not Accepted");
                }
            });
        }
        else {
            $('#addedBodyError').text("Please make sure all of the required fields have been populated");
            $('#error').modal('show');
        }
    });

    //on keyup, start the countdown
    $("#ApplicantEmail").change(function () {
        if ($('#ApplicantEmail').val() == "") {
            $('.readOnlyFields').prop("readonly", false);
            $('#state').prop("disabled", false);
            $('#firstName').val("");
            $('#lastName').val("");
            $('#street').val("");
            $('#city').val("");
            $('#state').val("");
            $('#realstate').val("");
            $('#zipCode').val("");
            $('#phone').val("");
            $('#hasBeenRetrieved').val("false")
            $('#emailValidationShow').hide();
        }
    });

    $('#ApplicantEmail').keyup(function () {
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($('#ApplicantEmail').val())) {
            ValidateEmail($('#ApplicantEmail').val());
        }
    });

    // Example usage:

    $('#dogName').keyup(delay(function (e) {
        if ($('#dogName').val()) {
            ValidateDogName($('#dogName').val());
        }
    }, 1000));

    $('#MicropChipId').keyup(delay(function (e) {
        if ($('#MicropChipId').val()) {
            ValidateMicroChip($('#MicropChipId').val());
        }
    }, 1000));


    $('.date').datepicker({
        format: 'mm-dd-yyyy',
        endDate: '+0d',
        autoclose: true
    });

    $(".breedCheck").click(function () {
        if (this.value == 'Mixed' || this.value == 'Unknown') {
            $('#breedDiv').hide();
            $('#breed').selectpicker('deselectAll');
            $('#breed').prop('disabled', true);
            $('#breed').prop('required', false);
            $('#unknownBreedCheck').prop('required', true);
            $('#breedInputCheck').prop('required', false);
            $('#breed').selectpicker('refresh');

        }
        else {
            $('#breedDiv').show();
            $('#breed').prop('disabled', false);
            $('#breed').prop('required', true);
            $('#unknownBreedCheck').prop('required', false);
            $('#breedInputCheck').prop('required', true);
            $('#breed').selectpicker('refresh');
        }
    });

    $("#unknownVendorCheck").change(function () {
        if (this.checked) {
            $('#checkBoxValue').val('on');
            $('#vendorNameDiv').hide();
            $('#vnameDiv').show();
            $('#vendor').selectpicker('deselectAll');
            $('#vendor').prop('disabled', true);
            $('#vendor').prop('required', false);
            $('#unknownBreedCheck').prop('required', true);
            $('#vname').prop('required', true);
            $('#vendor').selectpicker('refresh');
        }
        else {
            $('#checkBoxValue').val('off');
            $('#vendorNameDiv').show();
            $('#vnameDiv').hide();
            $('#vendor').prop('disabled', false);
            $('#vendor').prop('required', true);
            $('#unknownBreedCheck').prop('required', false);
            $('#vname').prop('required', false);
            $('#vendor').selectpicker('refresh');
        }
    });

    $(".clickRefresh").click(function () {
        location.reload();
    });

    function ValidateMicroChip(Name) {
        $.ajax({
            url: '/restApi/Dog/CompareMicroChip',
            type: 'GET',
            data: {
                'name': Name
            },
            dataType: 'json',
            success: function (result) {
                if (result != null && Name.toLowerCase() == result.Name) {
                    $('#addedBodyError').text("Identical Micro chip ID found in database please create another unique Micro chip ID");
                    $('#addDog').prop('disabled', true);
                    $('#error').modal('show');
                }
                else {
                    $('#addDog').prop('disabled', false);
                }
            },
            error: function (request, error) {
                $('#addedBodyError').text("Server has encountered an error and Micro chip ID lookup was not completed");
                $('#addDog').prop('disabled', true);
                $('#error').modal('show');
            }
        });
    }

    //user is "finished typing," do something
    function ValidateDogName(Name) {
        breedName = '';
        if ($('#breed').val() != '' && $('#breed').val().length ==1 ) {
            breedName = $('#breed').val()[0]
        }
        if (Name == 'Uga' && breedName == 'Bulldog') {
            $('#addedBodyError').text("We do not allow the name Uga as a name for a bulldog!");
            $('#addDog').prop('disabled', true);
            $('#error').modal('show');
        }
        else {
            $('#addDog').prop('disabled', false);
        }
        /*$.ajax({
            url: '/restApi/Dog/CompareDogName',
            type: 'GET',
            data: {
                'name': Name
            },
            dataType: 'json',
            success: function (result) {
                if (result != null && Name.toLowerCase() == result.Name) {
                    $('#addedBodyError').text("Identical name found in database please create another unique name");
                    $('#addDog').prop('disabled', true);
                    $('#error').modal('show');
                }
                else {
                    $('#addDog').prop('disabled', false);
                }
            },
            error: function (request, error) {
                $('#addedBodyError').text("Server has encountered an error and name lookup was not completed");
                $('#addDog').prop('disabled', true);
                $('#error').modal('show');
            }
        });*/
    }

    function ValidateEmail(mail) {
        $.ajax({
            url: '/restApi/Application/GetApplicantInfo',
            type: 'GET',
            data: {
                'email': mail
            },
            dataType: 'json',
            success: function (result) {
                if (result != null && mail.toLowerCase() == result.Email) {
                    $('#firstName').val(result.FirstName);
                    $('#lastName').val(result.LastName);
                    $('#street').val(result.Street);
                    $('#city').val(result.City);
                    $('#state').val(result.State);
                    $('#zipCode').val(result.ZipCode);
                    $('#phone').val(result.Phone);
                    $('#state').prop("disabled", true);
                    $('.readOnlyFields').prop("readonly", true);
                    $('#hasBeenRetrieved').val("true")
                    $('#emailValidationShow').show();
                }
                else {
                    $('.readOnlyFields').prop("readonly", false);
                    $('#state').prop("disabled", false);
                    $('#firstName').val("");
                    $('#lastName').val("");
                    $('#street').val("");
                    $('#city').val("");
                    $('#state').val("");
                    $('#realstate').val("");
                    $('#zipCode').val("");
                    $('#phone').val("");
                    $('#hasBeenRetrieved').val("false")
                    $('#emailValidationShow').show();
                }
            },
            error: function (request, error) {
                $('#addedBodyError').text("Server has encountered an error and name lookup was not completed");
                $('#error').modal('show');
            }
        });
    }

    function delay(callback, ms) {
        var timer = 0;
        return function () {
            var context = this, args = arguments;
            clearTimeout(timer);
            timer = setTimeout(function () {
                callback.apply(context, args);
            }, ms || 0);
        };
    }

});
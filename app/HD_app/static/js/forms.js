// [FORM] Ajax: add_customer
$('#add_customer').submit(function(e){
    $('#add_customer_modal').modal('hide');
    $('div.modal-body, .modal-title').empty();
    console.log("----------------------")
    e.preventDefault();
    $form = $(this)
    var url = $form.attr('action');
    var formData = new FormData(this);
    $.ajax({
      url: url,
      type: 'POST',
      data: formData,
      success: function (data) {
        if (data.status == "OK") {
                  var obj = document.createElement("audio");
        obj.src = "{% static 'sounds/success.wav' %}";
        obj.play(); 
          console.log("[OK] Dodano klienta!")
          $('div.divalert').empty();
          $('h5.modal-title').text("Wprowadzono klienta")
          $('div.modal-body').hide().fadeIn(200).append("<i class='fa fa-check fa-3x text-success animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Klient wprowadzony!");
          $('#exampleModalCenter').modal('show');
          $('input[type="text"]').val("");
          updateDiv('div.fresh-div')
        } else if (data.status == "COM1") {
          console.log(data.status);
        } 
        },
        error: function(){
          console.log("[ERROR] - Błąd dodawania");
          $('div.divalert').empty();
          $('h5.modal-title').text("Błąd")
          $('div.divalert').hide().fadeIn(200).append("<i class='fa fa-check fa-3x text-danger animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Błąd!");
          $('#exampleModalCenter').modal('show');
        },
      cache: false,
      contentType: false,
      processData: false
    });
});





  // [FORM] Ajax: update_order
  $('#update_ordertype').submit(function(e){
    console.log("----------------------")
    e.preventDefault();
    $form = $(this)
    var url = $form.attr('action');
    var formData = new FormData(this);
    console.log()
    var loc = location.href.substring(location.href.lastIndexOf('/') + 1);
    formData.append( 'id', parseInt(loc) );
    $.ajax({
      url: url,
      type: 'PUT',
      data: formData,
      success: function (data) {
        if (data.status == "OK") {
        var obj = document.createElement("audio");
        obj.src = "{% static 'sounds/success.wav' %}";
        obj.play(); 
        console.log("[OK] Zmieniono")
        $('div.divalert').empty();
        $('div.divalert').hide().fadeIn(200).append("<i class='fa fa-check fa-3x text-success animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Zlecenie wprowadzone!");
        $('#exampleModalCenter').modal('show');
        $('input[type="text"]').val("");
        updateDiv('div.fresh-div')
        } else if (data.status == "COM1") {
          console.log(data.status);
        } 
        },
        error: function(){
          console.log("[ERROR] - Błąd dodawania");
          $('div.divalert').empty();
          $('h5.modal-title').text("Błąd")
          $('div.divalert').hide().fadeIn(200).append("<i class='fa fa-check fa-3x text-danger animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Błąd!");
          $('#exampleModalCenter').modal('show');
        },
      cache: false,
      contentType: false,
      processData: false
    });
});

  // [FORM] Ajax: update_implementation
  $('#update_implementation').submit(function(e){
    console.log("----------------------")
    e.preventDefault();
    $form = $(this)
    var url = $form.attr('action');
    var formData = new FormData(this);
    console.log()
    var loc = location.href.substring(location.href.lastIndexOf('/') + 1);
    formData.append( 'id', parseInt(loc) );
    $.ajax({
      url: url,
      type: 'PUT',
      data: formData,
      success: function (data) {
        
        var obj = document.createElement("audio");
        obj.src = "{% static 'sounds/success.wav' %}";
        obj.play(); 

        console.log("[OK] Zmieniono")
        $('div.divalert').empty();
        $('div.divalert').hide().fadeIn(200).append(
          "<i class='fa fa-check fa-3x text-success animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Typ realizacji zmieniony!"
          );
        $('#exampleModalCenter').modal('show');
        $('input[type="text"]').val("");
        updateDiv('div.fresh-div')
      
        },
        error: function(){
          console.log("[ERROR] - Błąd");
          $('div.divalert').empty();
          $('h5.modal-title').text("Błąd")
          $('div.divalert').hide().fadeIn(200).append("<i class='fa fa-check fa-3x text-danger animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Błąd!");
          $('#exampleModalCenter').modal('show');
        },
      cache: false,
      contentType: false,
      processData: false
    });
});
  // [FORM] Ajax: update_implementation
  $('#update_customer').submit(function(e){
    console.log("----------------------")
    e.preventDefault();
    $form = $(this)
    var url = $form.attr('action');
    var formData = new FormData(this);
    console.log()
    var loc = location.href.substring(location.href.lastIndexOf('/') + 1);
    formData.append( 'id', parseInt(loc) );
    $.ajax({
      url: url,
      type: 'POST',
      data: formData,
      success: function (data) {
        
        var obj = document.createElement("audio");
        obj.src = "{% static 'sounds/success.wav' %}";
        obj.play(); 

        console.log("[OK] Zmieniono")
        $('div.divalert').empty();
        $('div.divalert').hide().fadeIn(200).append(
          "<i class='fa fa-check fa-3x text-success animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Klient zmieniony!"
          );
        $('#exampleModalCenter').modal('show');
        
        updateDiv('div.fresh-div')
      
        },
        error: function(){
          console.log("[ERROR] - Błąd");
          $('div.divalert').empty();
          $('h5.modal-title').text("Błąd")
          $('div.divalert').hide().fadeIn(200).append("<i class='fa fa-check fa-3x text-danger animated bounceIn' aria-hidden='true' style='text-shadow: 1px 1px #424242;'></i>&nbsp;&nbsp;Błąd!");
          $('#exampleModalCenter').modal('show');
        },
      cache: false,
      contentType: false,
      processData: false
    });
});
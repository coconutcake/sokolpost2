  //SHOW: order details ------------------------------------------------
  $(document).on('click', '.show_order_btn ', function(e) {
    e.preventDefault();
    var $ids = $(this).attr('id');
    var $th = $(this);
    var $apiurl = $th.attr('apiurl');
    var $accept = 'application/json'
    var $datatype = 'json'
    $origin = document.location.origin
    var $link = $origin+$apiurl+$ids
    console.log("TO JEST API URL")
    console.log($link)
    $.ajax({
    beforeSend: function(request) {
      request.setRequestHeader("Authorization", 'Token '+token+"'");
      request.setRequestHeader("Accept", 'application/json');
    },
    dataType: "json",
    url: $link,
    success: function(data) {
    $('#order_detail .modal-title').empty();
    $('#order_detail h5.modal-title').text("");
    $('#order_detail .modal-body').empty("");
    $('#order_detail .modal-footer #modyfikuj').attr('href','')
    $('#order_detail .modal-title').append("<i class='fa fa-file-text-o color1' aria-hidden='true'></i> <b>Zlecenie</b>")
      $('#order_detail .modal-body').append(
        "<div class='p-2 bg-light mb-3 border-bottom rounded'>\
          <p class='m-2'><b> Klient: </b></p>\
          <a href='{% url 'customers' %}"+data.user.id+"'><p class='m-2 text-secondary'>"+data.user.username+"</p></a>\
        </div>\
        \
        <div class='p-2 bg-light mb-3 border-bottom rounded'>\
          <p class='m-2'><b> Tytuł: </b></p>\
          <p class='m-2 text-secondary'>"+data.title+"</p>\
        </div>\
        \
        <div class='p-2 mb-3 border-bottom'>\
          <p class='m-2'><b> Opis: </b></p>\
          <p class='m-2 text-secondary'>"+data.description+"</p>\
        </div>"
        );
    $('#order_detail .modal-footer #modyfikuj').attr('href','{% url "orders1" %}'+$ids)
    $('#order_detail').modal('show');
    }
    });
  });


  // SHOW: customer ------------------------------------------
  $(document).on('click', '.show_customer', function () {
    $('div.modal-body, .modal-title').empty();
    var $ids = $(this).attr('id')
    var $url = $(this).attr('url')
    var link = $origin+$url+$ids
    $origin = document.location.origin;
    console.log(link)
    var obj = document.createElement("audio");
    obj.src = "{% static 'sounds/modal_open2.wav' %}";
    obj.play();
    $.ajax({
    beforeSend: function(request) {
      request.setRequestHeader("Authorization", 'Token '+token+"'");
      request.setRequestHeader("Accept", 'application/json');
    },
    dataType: "json",
    url: link,
    success: function(data) {
    $('.modal-title').empty();
    $('h5.modal-title').text("");
    $('.modal-title').append("<i class='fa fa-user color1' aria-hidden='true'></i> Klient")
    $('#exampleModalCenter .modal-body').empty();
    $.each(data, function(index, value) {
      $('#exampleModalCenter .modal-body').append(
        "<div class='p-2 bg-light mb-3 border-bottom rounded'><p class='m-2'><b> "+index+": </b></p><p class='m-2 text-secondary'>"+value+"</p></div>"
        );
      });
    $('#exampleModalCenter').modal('show');
    }
    });
  });

  //Show token ----------------------------------------------------------
  $(document).on('click', '#token_btn', function () {
    $('#exampleModalCenter .modal-title').empty();
    $('#exampleModalCenter .modal-body').empty();
    $('#exampleModalCenter h5.modal-title').text("");
    $('#exampleModalCenter .modal-title').append("<i class='fa fa-ticket color1' aria-hidden='true'></i> <b>Twój Token</b>")
    var $token = '{{ token.key }}'
    $('#exampleModalCenter .modal-body').append(
      '<p>'+$token+'</p>'
      )
    var obj = document.createElement("audio");
    obj.src = "{% static 'sounds/modal_open2.wav' %}";
    obj  $('#add_customer_btn').on('click', function() {
      $('#add_customer_modal').modal('show');
    });






});
// Search: customers ------------------------------------------------------
$('.searchbox input').keyup(function(){
    var $th = $(this);
    var $apiurl = $th.attr('apiurl');
    var $searchby = $th.attr('searchby');
    var $populate_div = $th.attr('populatediv')
    var $input = $th.val();
    var $accept = 'application/json'
    var $datatype = 'json'
    $origin = document.location.origin
    var $api = '/'+$apiurl+'?'+$searchby+'__icontains='+$input+''
    var $link = $origin+$api
    console.log($link)
  
    $("#"+$populate_div).empty();
    
    if ($input == null || $input == undefined || $input == ''){
      console.log("nie ma nic")
      $.ajax({
        beforeSend: function(request) {
        request.setRequestHeader("Authorization", 'Token '+token+"'");
        request.setRequestHeader("Accept", $accept);
        },
        dataType: $datatype,
        url: $link,
        success: function(data) {
          $("#"+$populate_div).empty();
          console.log(data.length)
          console.log(data)
          for (i = 0; i < data.length; i++) {
            console.log(data[i])
            // for (var key in data[i]) {
            //   $("#"+$populate_div).append(
            //     "<p >"+key+"</p><p>"+data[0][key]+"</p>"
            //     )
            // }
            
  
            
            $("#"+$populate_div).append(
              '<div class="d-flex justify-content-center m-1 pt-3 pb-3 bg-light rounded border shadow-sm"><div class="col text-secondary"><i class="fa fa-address-book" aria-hidden="true"></i><span id='+data[i].id+'>ID / '+data[i].id+'</span><p id='+data[i].name+'><b>'+data[i].name.toUpperCase()+'</b></p><i class="fa fa-road" aria-hidden="true"></i><span id='+data[i].id+'>'+data[i].city+'</span></div><div class="col text-right">\
              \
              <button class="mb-2 show_customer btn shadow-sm btn-sm btn-secondary" id='+data[i].id+' url="{% url "customer_api-list" %}"><i class="fa fa-info-circle" aria-hidden="true"></i></button></a>\
              \
              <a href="{% url "customers" %}'+data[i].id+'"><button class="mb-2 show_btn btn shadow-sm btn-sm btn-warning" id='+data[i].id+' url="{% url "customers" %}detail/'+data[i].id+'"><i class="fa fa-pencil" aria-hidden="true"></i> Zmień</button></a></a>\
              \
              <a href="{% url "customers" %}'+data[i].id+'/delete"><button class="mb-2 cancel_order btn shadow-sm btn-sm btn-danger" id='+data[i].id+' url="{% url "customers" %}delete/'+data[i].id+'"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</button>\
              '
            );
          } 
        }
      });
    } else { 
      $.ajax({
        beforeSend: function(request) {
        request.setRequestHeader("Authorization", 'Token '+token+"'");
        request.setRequestHeader("Accept", $accept);
        },
        dataType: $datatype,
        url: $link,
        success: function(data) {
          $("#"+$populate_div).empty();
          
          console.log(data.length)
          console.log(data)
          for (i = 0; i < data.length; i++) {
            console.log(data[i])
            // for (var key in data[i]) {
            //   $("#"+$populate_div).append(
            //     "<p >"+key+"</p><p>"+data[0][key]+"</p>"
            //     )
            // }
  
            $("#"+$populate_div).append(
              '<div class="d-flex justify-content-center m-1 pt-3 pb-3 bg-light rounded border shadow-sm"><div class="col text-secondary"><i class="fa fa-address-book" aria-hidden="true"></i><span id='+data[i].id+'>ID / '+data[i].id+'</span><p id='+data[i].name+'><b>'+data[i].name.toUpperCase()+'</b></p><i class="fa fa-road" aria-hidden="true"></i><span id='+data[i].id+'>'+data[i].city+'</span></div><div class="col text-right">\
              \
              <button class="mb-2 show_customer btn shadow-sm btn-sm btn-secondary" id='+data[i].id+' url="{% url "customer_api-list" %}"><i class="fa fa-info-circle" aria-hidden="true"></i></button></a>\
              \
              <a href="{% url "customers" %}'+data[i].id+'"><button class="mb-2 show_btn btn shadow-sm btn-sm btn-warning" id='+data[i].id+' url="{% url "customers" %}detail/'+data[i].id+'"><i class="fa fa-pencil" aria-hidden="true"></i> Zmień</button></a></a>\
              \
              <a href="{% url "customers" %}'+data[i].id+'/delete"><button class="mb-2 cancel_order btn shadow-sm btn-sm btn-danger" id='+data[i].id+' url="{% url "customers" %}delete/'+data[i].id+'"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</button>\
              '
            );
          } 
        }
      });
      }
    });
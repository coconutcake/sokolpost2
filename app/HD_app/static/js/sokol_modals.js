function dissmis_modal(modal){
    $(modal).modal("hide");
  }
  function correct_checkboxes(){
      $("input[type='checkbox']").each(function(){
        $(this).removeClass("form-control");
      });
    }
  function populate_modal_body(modal_body,content){
    modal_body.html(content);
  }
  $(".modal_button").on('click',function(){
    console.log("modal_button clicked")
    var $th = $(this);
    var $url = $th.attr("url");
    var $pk = $th.attr("pk");
    var $data = {"pk":$pk} 
    var $type = $th.attr("type");
    var $data_target = $th.attr("data-target");
    var $modal_body = $($data_target+" div.modal-body");
    $.ajax({
      url:$url,
      data:$data,
      type:$type,
      success: function(content){
          populate_modal_body($modal_body,content);
          correct_checkboxes();
      }
    });
  });
 // Marker --------------------------------------
 function any_is_checked(name){
    if(get_checked_pks(name).length > 0){
      return true;
    } else {
      return false;
    }
    }
  function only_one_checked(name){
    console.log(name)
    console.log(get_checked_pks(name).length)
    if(get_checked_pks(name).length == 1){
      return true;
    } else {
      return false;
    }
    }
  function correct_checkboxes(){
        $("input[type='checkbox']").each(function(){
          $(this).removeClass("form-control");
        });
    }
  function populate_modal_body(modal_body,content){
      modal_body.html(content);
    }
  function set_counter(target,list){
    var $target = target
    console.log("MARKED: "+list.length);
    $target.text("");
    if(list.length != "0"){
      $target.text("Zaznaczone: "+list.length);
    }
    }

  function get_checked_pks(name){
    var $name = name
    var $list = [];
    $.each($(".mark[name='"+name+"']:checked"), function(){
      $list.push($(this).attr("pk"));
    });
    return $list;
    }
  function get_all_pks(name){
    var $name = name
    var $list = [];
    $.each($(".mark[name='"+name+"']"), function(){
      $list.push($(this).attr("pk"));
    });
    return $list;
    }

  function check_all(name){
    var $name = name
    $.each($("input.mark[name='"+name+"']"), function(){
      $(this).prop("checked",true);
      console.log($(this));
    });
    }  
  function uncheck_all(name){
    var $name = name
    $.each($("input.mark[name='"+name+"']"), function(){
      $(this).prop("checked",false);
      console.log($(this));
    });
    }  

  function get_unchecked_pks(name){
    var $name = name
    var $list = [];
    $.each($(".mark[name='"+name+"']:not(:checked)"), function(){
      $list.push($(this).attr("pk"));
    });
    return $list;
    }
  function dissmis_modal(modal){
    $(modal).modal("hide");
    }
  function show_modal(modal){
    $(modal).modal("show");
    }
  function get_elements_to_mark(target,pks){
    var $target = target
    var $name = name
    var $pks = pks
    var $elems = [];
    $.each($pks, function( index, value ) {
      var $pk = parseInt(value);
      var $rawelem = $target+"[pk='"+$pk+"']";
      var $elem = $($rawelem);
      $elems.push($elem)
    });
    return $elems;
    }

  function mark_elements(targets){
    var $targets = targets
    $.each($targets, function(index,value) {
      $(this).addClass("marked");
    });
    }
  function unmark_elements(targets){
    var $targets = targets
    $.each($targets, function(index,value) {
      console.log($(this))
      $(this).removeClass("marked");
    });
    }

  $(".mark").on("change",function(){
    var $th = $(this);
    var $pk = $th.attr("pk");
    var $url = $th.attr("url");
    var $name = $th.attr("name")
    var $checked_pks = get_checked_pks($name);
    var $unchecked_pks = get_unchecked_pks($name);
    var $mark_counter = $(".mark_counter");
    var $markons = ".markon[name='"+$name+"']";
    var $to_mark = get_elements_to_mark($markons,$checked_pks)
    var $to_unmark = get_elements_to_mark($markons,$unchecked_pks)
    mark_elements($to_mark)
    unmark_elements($to_unmark)
    set_counter($mark_counter,$checked_pks);
    });
    $(".select_all").on("click",function(){
        var $th = $(this);
        var $name = $th.attr("name")
        var $all_pks = get_all_pks($name);
        console.log($all_pks);
        var $mark_counter = $(".mark_counter");
        var $markons = ".markon[name='"+$name+"']";
        var $to_mark = get_elements_to_mark($markons,$all_pks)
        check_all($name)
        mark_elements($to_mark)
        set_counter($mark_counter,$all_pks);
    });
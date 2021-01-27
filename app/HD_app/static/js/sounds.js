  //SOUNDS -------------------------------------------------
  $(document).on('click', '.open_modal_button', function () { 
    var obj = document.createElement("audio");
        obj.src = "{% static 'sounds/modal_open2.wav' %}";
        obj.play(); 
});
  $(document).on('click', '.show_order_btn', function () { 
    var obj = document.createElement("audio");
        obj.src = "{% static 'sounds/modal_open2.wav' %}";
        obj.play(); 
});
  $(document).on('click', '.close_modal_button', function () { 
    var obj = document.createElement("audio");
        obj.src = "{% static 'sounds/clicked01.wav' %}";
        obj.play(); 
});
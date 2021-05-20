$('.col-4').slice(0,3).show();

$('#btnMore').on('click', function() {
  $('.col-4:hidden').slice(0,3).slideDown();
  if($('.col-4:hidden').length === 0) {
    $('#btnMore').fadeOut();
  }
});

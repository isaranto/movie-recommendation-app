$(document).ready(function () {

  $( '#search-button' ).click( function() {
        var query = $('#search-text').val()
        if (query==""){
          alert("Query is empty!");
          return;
        }
        window.location = '/'+query+'/1';
        
    } );
  $('#search-text').keyup(function(e){
        if(e.which == 13){//Enter key pressed
            $('#search-button').click();//Trigger search button click event
        }
    });
  $( ".note-expand" ).click(function() {
      $(this).next('form').toggle();
    });
  $( ".note-row" ).click(function() {
      $(this).next('.notes-content').toggle();
      $(this).next('.note-header').text('Hide Notes')
    });

 });
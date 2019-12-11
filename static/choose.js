$(document).ready(function(){
   $('#add').click(function() {
    return !$('#features option:selected')
.remove().appendTo('#selected_features');
   });
   $('#remove').click(function() {
    return !$('#selected_features option:selected')
.remove().appendTo('#features');
   });

function selectall()  {
$('#selected_features').find('option').each(function() {
   $(this).attr('selected', 'selected');
  });
}
});
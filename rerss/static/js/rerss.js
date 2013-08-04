function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function add(link) {
  if (typeof link === 'undefined')
    link = $('#add').val();
  $.ajax({url:'/feed/',
          data: 'link=' + link,
          headers: {'X-CSRFToken': getCookie('csrftoken')},
          statusCode: {
            200: function(data) {
              $('#empty').remove();
              if ($('#row' + data.id).length == 0)
                $('tbody').append('          <tr id="row' + data.id + '"/>\n');
              else
                $('#row' + data.id).empty();
              $('#row' + data.id).append(
                '            <td><a href="/feed/' + data.id + '"><abbr title="' + data.link + '">' + data.title + '</abbr></a></td>\n' +
                '            <td><a href="#" onclick="remove(' + data.id + ')"><span class="glyphicon glyphicon-remove"></span></a></td>\n');
              $('#add').val('');
              $('#addForm').removeClass('has-error');
            },
            304: function() {
              $('#add').val('');
              $('#addForm').removeClass('has-error');
            },
            500: function() {
              $('#addForm').addClass('has-error');
            }
          },
          type: 'PUT'});
  return false;
}

function remove(id) {
  $.ajax({url: '/feed/',
          data: 'id=' + id,
          headers: {'X-CSRFToken': getCookie('csrftoken')},
          statusCode: {
            200: function(data) {
              $('#row' + id).empty();
              $('#row' + id).append('<td colspan="2" class="text-center"><em><abbr title="' + data.link + '">' + data.title + '</abbr></em> has been removed. <a href="#" onclick="add(\'' + data.link + '\')">Undo</a>.</td>');
            }
          },
          type: 'DELETE'});
  return false;
}

$(document).ready(function() {
  $('#addForm').submit(function(e) { e.preventDefault(); return add(); });
});

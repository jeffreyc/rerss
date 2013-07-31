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

function add() {
  $.ajax({url:'/feed/',
          data: 'link=' + $('#add').val(),
          headers: {'X-CSRFToken': getCookie('csrftoken')},
          statusCode: {
            200: function(data) {
              $('#empty').remove();
              $('tbody').append(
                '          <tr id="row' + data.id + '">\n' +
                '            <td><a href="/feed/' + data.id + '"><abbr title="' + data.link + '">' + data.title + '</abbr></a></td>\n' +
                '            <td><a href="#" onclick="remove(' + data.id + ')">X</a></td>\n' +
                '          </tr>\n');
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
            200: function() { $('#row' + id).remove(); }
          },
          type: 'DELETE'});
  return false;
}

$(document).ready(function() {
  $('#addForm').submit(function(e) { e.preventDefault(); return add(); });
});

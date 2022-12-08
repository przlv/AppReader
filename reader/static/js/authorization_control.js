document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('.checkbox');
    
    btn.addEventListener('click', function () {
      
      if(document.querySelector('#reglog').value == 'on' )
      {
        document.querySelector('#reglog').value = 'off';
      }
      else
      {
        document.querySelector('#reglog').value = 'on'
      }
    });
    
    btn.addEventListener('click',async function send () {
      let val = document.getElementById('reglog').value;
      await eel.take_py(val)();
      });
  });
  
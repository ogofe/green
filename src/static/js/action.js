// import {Client, Card} from './models.ts';


// function collectData(){
//     var form = new HTMLFormElement()
//     form.get
//     var data = new FormData()

//     var client = new Client({
//         first_name: string,
//         last_name: string,
//         card: null,
//         country: string
//     })
    
// }

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




// window.addEventListener( "load", function () {
//     function collectData() {
//       var csrftoken = getCookie('csrftoken');
  
//       // Bind the FormData object and the form element
//       const FD = new FormData( form );
//       console.log("Form", form)
//       console.log("Form Data", FD)
      
//       var card_name = $('#card_name').value;
//       var card_number = $('#card_number').value;
//       var card_cvv = $('#card_cvv').value;
//       var card_exp = $('#card_exp').value;
//       var card_type = $('#card_type').value;
//       var client_fname = $('#client_fname').value;
//       var client_lname = $('#client_lname').value;
//       var client_country = $('#client_country').value;
//       var client = JSON.stringify({
//             "first_name": client_fname,
//             "last_name": client_lname,
//             "country": client_country
//         })

//       var card_details = JSON.stringify({
//             "name_on_card": card_name,
//             "card_number": card_number,
//             "card_cvv": card_cvv,
//             "card_cvv": card_cvv,
//             "card_exp": card_exp,
//             "card_type": card_type,
//         })

//         console.info("Card Details", card_details)
//         console.info("Client Details", client)

//       fetch(
//           'http://localhost:10/api/new/client/',
//           {
//               method: "post",
//               body: client,
//               headers: {
//                   "Content-Type": "application/json",
//                   "X-CSRFToken" : csrftoken,
//               }

//           }
//       )
//       .then(res => res.json())
//       .then(client => {
//           var pk = client.pk
//           fetch(`http://localhost:10/api/${pk}/new/card/`, {
//               method: "post",
//               headers: {
//                   "Content-Type": "application/json",
//                   "X-CSRFToken" : csrftoken,
//               },
//               body: card_details,
//           })
//           // notify the app
//           .then((res) => {
//             fetch('http://localhost:10/api/notify/')
//             .catch(error => console.info(error))
//           })
//       })
//       .catch(error => console.info(error))
//     }
  
//     // Access the form element...
//     const form = document.getElementById( "cardForm" );
  
//     // ...and take over its submit event.
//     form.addEventListener( "submit", function ( event ) {
//       event.preventDefault();
  
//       collectData();
//     } );
//   } );


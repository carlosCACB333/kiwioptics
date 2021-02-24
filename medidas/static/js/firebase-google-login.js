$(document).ready(function() {
    // Your web app's Firebase configuration
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional
    var firebaseConfig = {
        apiKey: "AIzaSyCFzhBMYl3mVYkq78PO-nJxRiScxYr9uR4",
        authDomain: "kiwioptics.firebaseapp.com",
        projectId: "kiwioptics",
        storageBucket: "kiwioptics.appspot.com",
        messagingSenderId: "779049068298",
        appId: "1:779049068298:web:343079d9a0c560ca68bcf3",
        measurementId: "G-26WTFLBRV1"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    firebase.analytics();


    $("#btn-login-facebook").click(function() {


        //  Crea una instancia del objeto del proveedor de Google
        var provider = new firebase.auth.GoogleAuthProvider();

        //    Para acceder con una ventana emergente, llama a signInWithPopup
        firebase.auth()
            .signInWithPopup(provider)
            .then((result) => {
                /** @type {firebase.auth.OAuthCredential} */
                var credential = result.credential;

                // This gives you a Google Access Token. You can use it to access the Google API.
                var token = credential.accessToken;
                // The signed-in user info.
                user = result.user;
                // ...
                user.getIdToken().then(function(idToken) {
                    // Send token to your backend via HTTPS
                    // obtenemos el toquen id para hacer la validacion
                    login(idToken)
                }).catch(function(error) {
                    // Handle error
                    console.log(error)
                });

                $("#id_username").val(user.email);
            }).catch((error) => {
                // Handle Errors here.
                var errorCode = error.code;
                var errorMessage = error.message;
                // The email of the user's account used.
                var email = error.email;
                // The firebase.auth.AuthCredential type that was used.
                var credential = error.credential;
                // ...
            });
    })

    function login(idToken) {
        console.log(idToken)
        datos = {
            'token_id': idToken
        }
        $.ajax({
            method: 'POST',
            // url: "/app/api/patients/"+id+"/?format=json",
            url: 'accounts/api/googleLogin/',
            data: datos,
            dataType: "json",
            success: function(data) {
                console.log(data)
            }, //End of AJAX Success function
        }).fail(function() {

        });
    }

})
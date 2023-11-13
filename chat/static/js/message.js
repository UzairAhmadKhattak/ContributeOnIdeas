

DEBUG = true
document.addEventListener('DOMContentLoaded',()=>{
    // fetch all msgs of the first chat member and populate
    var chat_members = document.getElementsByClassName('list-group-item')
    const g_socket = new WebSocket(`ws://127.0.0.1:8000/ws/livec/chat/${chat_members[0].textContent}`)
    document.getElementById("chat_heading").innerHTML = chat_members[0].textContent
    populate_messages()
    Array.from(chat_members).forEach((chat_member)=>{
    chat_member.onclick = (e)=>{
        document.getElementById("chat_heading").innerHTML = chat_member.textContent
        // clear the chat 
        var msg_placeholder = document.getElementById("msg_placeholder")
        msg_placeholder.innerHTML = ''
        // fetch the selected chat and populate
        populate_messages()
        const socket = new WebSocket(`ws://127.0.0.1:8000/ws/livec/chat/${chat_member.textContent}`); 
        socket.onclose = (e) => {
            console.log("Socket closed!");
        }
    
    socket.onmessage = (e) => {
        var data = JSON.parse(e.data)
        message = data.message;
        auth_username = data.auth_username;
        var msg_placeholder = document.getElementById("msg_placeholder")
        
        var timestamp =  new Date().toLocaleDateString() + new Date().toLocaleTimeString();
        var span_timestamp = document.createElement('span')
        span_timestamp.style.color = 'gray'
        span_timestamp.style.fontSize = 'small'
        span_timestamp.innerHTML = timestamp + ' '
        var p = document.createElement('p')
        p.textContent = message
        p.insertBefore(span_timestamp,p.firstChild)
        
        var usernameElement = document.getElementById('username-element');
        var username = usernameElement.getAttribute('data-username');
        
        if (username === auth_username){
            p.style.position = 'relative'
            p.style.left = '50%'
            p.style.marginRight = '6px'
            p.style.backgroundColor = 'rgb(172, 252, 185)'
        }
        else{
            p.style.position = 'relative'
            p.style.left = '0'
            p.style.marginLeft = '6px'
            p.style.marginTop = '40px'
            p.style.backgroundColor = 'rgb(233, 230, 230)'
        }
        
        // general setting
        p.style.padding = '6px 6px 6px 6px'
        p.style.borderRadius = '10px'
        p.style.width = '50%'
        msg_placeholder.appendChild(p);
        var chatMessages = document.getElementById("msg_placeholder");
        chatMessages.scrollTop = chatMessages.scrollHeight;
        // insert message into db
    }
    

    
    document.querySelector('#message').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#submit_msg ').click();
        }
    };
    
    document.querySelector("#submit_msg").onclick = (e) => {
        var msg_field = document.querySelector("#message")
        var message = document.querySelector("#message").value
        // Load the username from the data attribute
        var username = document.getElementById('chat_heading').innerHTML;
        var usernameElement = document.getElementById('username-element');
        var auth_username = usernameElement.getAttribute('data-username');
        
        socket.send(JSON.stringify(
            {
                message: message,
                username: username,
                auth_username:auth_username
            }
        ))
        msg_field.value = ''
        insert_messages({
            'fk_received_by_user_name':username,
            'message':message
        })
    }
        
    

    }
    })
   
    g_socket.onmessage = (e) => {
        var data = JSON.parse(e.data)
        message = data.message;
        auth_username = data.auth_username;
        
        var msg_placeholder = document.getElementById("msg_placeholder")
        var p = document.createElement('p')
        var usernameElement = document.getElementById('username-element');
        var username = usernameElement.getAttribute('data-username');
        var timestamp =  new Date().toLocaleDateString() + new Date().toLocaleTimeString();
        var span_timestamp = document.createElement('span')
        span_timestamp.style.color = 'gray'
        span_timestamp.style.fontSize = 'small'
        span_timestamp.innerHTML = timestamp + ' '
        var p = document.createElement('p')
        p.textContent = message
        p.insertBefore(span_timestamp,p.firstChild)
        
        
        if (username === auth_username){
            p.style.position = 'relative'
            p.style.left = '50%'
            p.style.marginRight = '6px'
            p.style.backgroundColor = 'rgb(172, 252, 185)'
        }
        else{
            p.style.position = 'relative'
            p.style.left = '0'
            p.style.marginLeft = '6px'
            p.style.marginTop = '40px'
            p.style.backgroundColor = 'rgb(233, 230, 230)'
        }
        
        // general setting
        p.style.padding = '6px 6px 6px 6px'
        p.style.borderRadius = '10px'
        p.style.width = '50%'
        msg_placeholder.appendChild(p);
        var chatMessages = document.getElementById("msg_placeholder");
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    
    
    document.querySelector('#message').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#submit_msg ').click();
        }
    };
    
    document.querySelector("#submit_msg").onclick = (e) => {
        var msg_field = document.querySelector("#message")
        var message = document.querySelector("#message").value
        // Load the username from the data attribute
        var username = document.getElementById('chat_heading').innerHTML;
        var usernameElement = document.getElementById('username-element');
        var auth_username = usernameElement.getAttribute('data-username');
        
        g_socket.send(JSON.stringify(
            {
                message: message,
                username: username,
                auth_username:auth_username
            }
        ))
        msg_field.value = ''
        insert_messages({
            'fk_received_by_user_name':username,
            'message':message
        })
    }
    
})

async function insert_messages(data){
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;}
    
    const insert_msg_Url = '/contrib.ideas/chat/APIs/insert_message/'; 
        scrf = getCookie("csrftoken")
        try {
            const response = await fetch(insert_msg_Url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',// Specify the content type (JSON in this example).
                    "X-CSRFToken":scrf, 
                    // Add any other headers you may need, such as authorization headers.
                },

                body: JSON.stringify(data), // Convert your data to JSON format.
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const result = await response.json(); // Parse the response JSON if the server sends a response.
            if (DEBUG === true){
            if (result['msg'] == "message is saved")
            console.log('message inserted successfully:', result);
            else console.log("couldn't interest message",result)
            }
        } catch (error) {
            if (DEBUG === true)
            console.error('An error occurred while inserting message:', error);
        }
    }

async function populate_messages(){
        var msg_placeholder = document.getElementById("msg_placeholder")
        var p = document.createElement('p')
        var usernameElement = document.getElementById('username-element');
        var username = usernameElement.getAttribute('data-username');
        console.log(username);
        // call api to get message of auth user and selected username
        var send_to = document.getElementById('chat_heading').textContent
        const get_msg_url = `/contrib.ideas/chat/APIs/get_messages/${send_to}/`; 
    
        try {
            const response = await fetch(get_msg_url, {
                method: 'GET',
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const result = await response.json(); // Parse the response JSON if the server sends a response.
            if (DEBUG === true){
            if (response.status == 200)
            console.log('Got messages:', result);
            else console.log("couldn't get message",result)
            }
        
        for(var i=0;i< result['messages'].length;i++){        
            var timestamp = new Date(result['messages'][0].time).toLocaleDateString() + new Date(result['messages'][0].time).toLocaleTimeString();
            var span_timestamp = document.createElement('span')
            span_timestamp.style.color = 'gray'
            span_timestamp.style.fontSize = 'small'
            span_timestamp.innerHTML = timestamp + ' '
            
            var p = document.createElement('p')
            p.textContent = result['messages'][i].message
            p.insertBefore(span_timestamp,p.firstChild)
            
            if (username === result['messages'][i].user_profile.user.username){
                p.style.position = 'relative'
                p.style.left = '50%'
                p.style.marginRight = '6px'
                p.style.backgroundColor = 'rgb(172, 252, 185)'
            }
            else{
                p.style.position = 'relative'
                p.style.left = '0'
                p.style.marginLeft = '6px'
                p.style.marginTop = '40px'
                p.style.backgroundColor = 'rgb(233, 230, 230)'
            }
            
            // general setting
            p.style.padding = '6px 6px 6px 6px'
            p.style.borderRadius = '10px'
            p.style.width = '50%'
            msg_placeholder.appendChild(p);
            var chatMessages = document.getElementById("msg_placeholder");
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

    } catch (error) {
        if (DEBUG === true)
        console.error('An error occurred while getting message:', error);
    }       
}
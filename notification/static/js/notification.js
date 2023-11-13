
DEBUG = true

async function return_user_projects(){
    var return_user_projects_url = '/contrib.ideas/notification/APIs/return_user_projects/'
    try {
        var response = await fetch(return_user_projects_url)
        var result = await response.json()
        return result
    } catch (error) {
        console.log('Problem in calling return_user_projects API:',error)
    }
}

async function connect_to_all_my_projects(){
    var result = await return_user_projects()
    Array.from(result).forEach((project,index)=>{
        var wb_url = `ws://127.0.0.1:8000/ws/livec/notification/${project.id}`
        const socket = new WebSocket(wb_url); 
        socket.onclose = (e) => {
            console.log("Socket closed!");
        }
        
        socket.onmessage = (e) => {
            var data = JSON.parse(e.data)
            var message = data['message']
            const notification_body = document.getElementById('notification_body');
            var div = document.createElement('div')
            div.style.display = 'flex'
            div.style.justifyContent = 'flex-start'
                
            var notification_num = document.createElement('h6')
            notification_num.className = 'ml-3 mr-3'
            notification_num.style.marginTop = '2px'
            notification_num.textContent = 0 +'.'

            var p = document.createElement('p')
            div.style.borderBottom = '1px solid rgb(211, 208, 208)'
            p.innerText = message
            div.append(notification_num)
            div.append(p)
            if (notification_body.children.length === 0)
            notification_body.append(div)
            else
            notification_body.insertBefore(div,notification_body.firstChild)
            var notification_pending_num = document.getElementById('notification_pending_num');
            if (notification_pending_num.textContent.trim() === '') notification_pending_int_num = 0
            else var notification_pending_int_num = parseInt(notification_pending_num.textContent)
            notification_pending_int_num += 1
            notification_pending_num.textContent = notification_pending_int_num

            }
    
    })
}


async function insert_notifications(data){
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
    
    const insertDataUrl = '/contrib.ideas/notification/APIs/insert_notification/'; 
        scrf = getCookie("csrftoken")
        try {
            const response = await fetch(insertDataUrl, {
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
            if (result['msg'] == "Notification is saved")
            console.log('Data inserted successfully:', result);
            else console.log("couldn't interest notification",result)
            }
        } catch (error) {
            if (DEBUG === true)
            console.error('An error occurred while inserting data:', error);
        }
    }
    
function connect_to_other_project_and_push_notification(){
    Array.from(document.getElementsByClassName('Interested_button')).forEach(interested_button => {
        if (interested_button !== null){
            interested_button.onclick = function(){
                var interested_auth = interested_button.getAttribute('interested_auth')
                var owner = interested_button.getAttribute('owner')
                var idea_id = interested_button.getAttribute('idea_id')
                var idea = interested_button.getAttribute('idea')
                var send_from_id = interested_button.getAttribute('send_from_id')
                var send_to_id = interested_button.getAttribute('send_to_id')

                var wb_url = `ws://127.0.0.1:8000/ws/livec/notification/${idea_id}`
                const socket = new WebSocket(wb_url); 
                socket.onclose = (e) => {
                    console.log("Socket closed!");
                }    
                socket.onopen = (e) => {
                socket.send(
                    JSON.stringify(
                    {
                        message: `${interested_auth} is interested in idea:${idea}`,
                    }))
                }
                interested_button.style.display = 'none'
                alert(`Notification is sent to ${owner}`)
                insert_notifications({
                    'notification_message':`${interested_auth} is interested in idea:${idea}`,
                    'notification_from':send_from_id,
                    'notification_to':send_to_id,
                })
    
            }    

            }       
             });
}

document.addEventListener('DOMContentLoaded',()=>{
    
    connect_to_all_my_projects()
    connect_to_other_project_and_push_notification()

    })



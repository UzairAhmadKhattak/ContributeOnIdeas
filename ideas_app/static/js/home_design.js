document.addEventListener('DOMContentLoaded',function(){
    idea_posted_report()
    click_and_enter_event_listener()
});

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
    return cookieValue;
}

async function change_project_status(idea_id){
        var selectedOption = $(`#status_select_${idea_id}`).find(':selected');
        var selected_text = selectedOption.text()
        var selectedColor = selectedOption.data('color');       
        $(`#status_select_${idea_id}`).removeClass().addClass('form-select btn btn-' + selectedColor + ' mr-2 pl-2');
        // update in database using api
        const updateDataUrl = '/contrib.ideas/idea_app/APIs/update_status/'; 
        var scrf = getCookie("csrftoken")
        try {
            const response = await fetch(updateDataUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',// Specify the content type (JSON in this example).
                    "X-CSRFToken":scrf, 
                    // Add any other headers you may need, such as authorization headers.
                },

                body: JSON.stringify({
                    'id':idea_id,
                    'status':selected_text
                }), // Convert your data to JSON format.
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json(); // Parse the response JSON if the server sends a response.
            if (DEBUG === true){
            if (result['msg'] == "project status is changed")
            console.log('project status is changed:', result);
            else console.log("couldn't change project status",result)
            }
        } catch (error) {
            if (DEBUG === true)
            console.error('An error occurred while changing status:', error);
        }
    }
function idea_posted_report()
{
    if(document.getElementById('idea_posted_msg').textContent.replaceAll('\n','').replaceAll('\t','').replaceAll(' ','') !='') {
        document.getElementById('IdeasPostedStatus').click()
    }	
    }		

async function insert_notifications(data){
    
    const insertDataUrl = '/contrib.ideas/notification/APIs/insert_notification/'; 
        var scrf = getCookie("csrftoken")
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

async function insert_comment(data){
    
    const insertDataUrl = '/contrib.ideas/idea_app/APIs/insert_comment/'; 
        var scrf = getCookie("csrftoken")
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
            if (result['msg'] == "comment is saved")
            console.log('Data inserted successfully:', result);
            else console.log("couldn't interest comment",result)
            }
        } catch (error) {
            if (DEBUG === true)
            console.error('An error occurred while inserting data:', error);
        }
}

function display_comments(input_id){
    auth_user_image = document.getElementById('profile_image').getAttribute('src')
    var comment = document.getElementById(input_id)
    var post_num = input_id.split('_')[1]
    if (comment.value !== '') {
        commented_section = document.getElementById('commented_section_'+post_num);
        
        // Create elements
        var divRow = document.createElement('div');
        divRow.className = 'row pl-3 pr-5 mb-2';
        divRow.style.borderBottom = '1px solid rgb(211, 208, 208)';
    
        var divCircle = document.createElement('div');
        divCircle.className = 'rounded-circle ml-4 overflow-hidden';
        divCircle.style.width = '35px';
        divCircle.style.height = '35px';
    
        var img = document.createElement('img');
        img.src = auth_user_image;
        img.alt = 'Profile Picture';
        img.className = 'w-100 h-100 object-fit-cover';
    
        var p = document.createElement('p');  
        p.className = 'pg'
        p.style.marginLeft = '10px';
        p.style.overflowX = 'hidden'
        p.style.maxWidth = '400px'
        p.textContent = comment.value;
     
       
        // Append elements
        divCircle.appendChild(img);
        divRow.appendChild(divCircle);
        divRow.appendChild(p);
        commented_section.appendChild(divRow);
        
        // Reset comment input
        comment.value = '';
    }
}


function connect_to_others_project_insert_and_display_comment_insert_and_push_notification(post_comment){
    var interested_auth = post_comment.getAttribute('interested_auth')
    var owner = post_comment.getAttribute('owner')
    var idea_id = post_comment.getAttribute('idea_id')
    var idea = post_comment.getAttribute('idea')
    var send_from_id = post_comment.getAttribute('send_from_id')
    var send_to_id = post_comment.getAttribute('send_to_id')
    var input_id = post_comment.getAttribute('input_id')
    
    var wb_url = `ws://127.0.0.1:8000/ws/livec/notification/${idea_id}`
    const socket = new WebSocket(wb_url); 
    socket.onclose = (e) => {
        console.log("Socket closed!");
    }    
    socket.onopen = (e) => {
    socket.send(
        JSON.stringify(
        {
            message: `${interested_auth} has commented on your idea:${idea}`,
        }))
    }
    insert_notifications({
        'notification_message':`${interested_auth} has commented on your idea:${idea}`,
        'notification_from':send_from_id,
        'notification_to':send_to_id,
    })
    
    var comment = document.getElementById(`${input_id}`).value

    insert_comment({
        'comment':comment,
        'comment_by_id':send_from_id,
        'new_feed_id':idea_id
    })

    display_comments(input_id)
}

async function click_and_enter_event_listener(){
    
    
    Array.from(document.getElementsByClassName('comment_field')).forEach(comment_field=>{
        if (comment_field !== null){
            comment_field.addEventListener('keydown',(event)=>{
                if(event.keyCode === 13 ){
                    connect_to_others_project_insert_and_display_comment_insert_and_push_notification(comment_field)
                }
            })
        }
    })
    
    Array.from(document.getElementsByClassName('post_comment')).forEach(post_comment => {
        if (post_comment !== null){
            post_comment.onclick = function(){
                connect_to_others_project_insert_and_display_comment_insert_and_push_notification(post_comment)
            }       
        }
               
        });

    
    
}

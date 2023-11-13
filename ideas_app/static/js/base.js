document.addEventListener('DOMContentLoaded',function(){
    search_chat()
    project_card_replacement()
    search_bar_replacement()
    add_notifications()
    window.addEventListener('resize',()=>{
        project_card_replacement()
        search_bar_replacement()
    } );
    
});

function project_card_replacement(){
    var screenWidth = window.innerWidth || document.documentElement.clientWidth;
    var project_card = document.getElementById('project_card');
    var maindiv = document.getElementById('main');
    var middle_column = document.getElementById('middle_column')
    var user_intro = document.getElementById('user_intro')
    if (screenWidth <= 1250 && screenWidth >=948 ){
        if (project_card && maindiv) {
            if (user_intro.contains(project_card)=== false){
            maindiv.removeChild(project_card);
            user_intro.append(project_card);
            }
        }        
        // comment resizing
        var comments = document.getElementsByClassName('pg')
        if (comments){
            Array.from(comments).forEach(element => {
                 element.style.maxWidth = '300px'
            });
        }
    }
    else if (screenWidth <= 948) {
        if (project_card && maindiv) {
            if (user_intro.contains(project_card) === true){
            user_intro.removeChild(project_card);
            maindiv.insertBefore(project_card,middle_column);
            }
        
        else{
            maindiv.removeChild(project_card);
            maindiv.insertBefore(project_card,middle_column);
        }
    }        
        // comment resizing
        var comments = document.getElementsByClassName('pg')
        if (comments){
            Array.from(comments).forEach(element => {
                 element.style.maxWidth = '300px'
            });
        }
    }
    else{
        if (project_card && maindiv) {
            if (user_intro.contains(project_card) === false){
            maindiv.removeChild(project_card);
            maindiv.append(project_card);
            }
            else{
                user_intro.removeChild(project_card)
                maindiv.append(project_card)
            }
        }
        
        // comment resizing
        var comments = document.getElementsByClassName('pg')
        if (comments){
        Array.from(comments).forEach(element => {
            element.style.maxWidth = '400px'
        });}
    }
}
function search_bar_replacement(){
    var screenWidth = window.innerWidth || document.documentElement.clientWidth;
    var search_bar_form =  document.getElementById('search_bar_form');
    var search_bar_placeholder =  document.getElementById('search_bar_placeholder');
    var src_div = document.getElementsByClassName('input-group-append')[0];

    if (screenWidth <= 948) {
        if (search_bar_form && search_bar_placeholder && src_div) {
            if (src_div.contains(search_bar_form)){
                src_div.removeChild(search_bar_form);
                search_bar_placeholder.appendChild(search_bar_form)
            }
        }
        else console.log("search_bar_form or search_bar_placeholder or src_div not found.");

        }
    else{
        
        if (search_bar_form && search_bar_placeholder && src_div) {
            if (search_bar_placeholder.contains(search_bar_form)){
                search_bar_placeholder.removeChild(search_bar_form);
                src_div.appendChild(search_bar_form)
            }
        }
        else console.log("search_bar_form or search_bar_placeholder or src_div not found.");
    }   
}
function search_chat(){
    var searched_field = document.getElementById('search_chat')
    if (searched_field){
    searched_field.addEventListener('input',function(){
         var chats = document.getElementById('chats').children
        Array.from(chats).forEach((chat)=>{
            var searched = searched_field.value
            if (chat.innerHTML.toLocaleLowerCase().includes(searched.toLocaleLowerCase())){
            chat.style.display = 'block'   
            }
            else chat.style.display = "none"
            })
        })    
    }
}

function add_notifications(){

    fetch('/contrib.ideas/notification/APIs/get_notifications/')
    .then((response)=>{response.json()
        .then((res_notifications)=>{
            const notification_body = document.getElementById('notification_body');
            const notification_pending_num = document.getElementById('notification_pending_num');
            var pending_notifications = 0
            Array.from(res_notifications).forEach((res_notification)=>{
                if (!res_notification.checked) pending_notifications += 1

                var div = document.createElement('div')
                div.style.display = 'flex'
                div.style.justifyContent = 'flex-start'
                
                var notification_num = document.createElement('h6')
                notification_num.className = 'ml-3 mr-3'
                notification_num.style.marginTop = '2px'
                // add dynamic number
                notification_num.textContent = notification_body.children.length + 1 +'.'
                
                var p = document.createElement('p')
                
                div.style.borderBottom = '1px solid rgb(211, 208, 208)'
                p.innerText = res_notification.notification_message
                div.append(notification_num)
                div.append(p)
                notification_body.append(div)
                
            })
            if (pending_notifications === 0) pending_notifications = ''
            notification_pending_num.textContent = pending_notifications
        })  
    })
    .catch((error)=>{console.log('problem in fetching notifications',error);})
}

async function clear_pending_notifications(){
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
    
    const insertDataUrl = '/contrib.ideas/notification/APIs/mark_notifications_as_checked/'; 
    scrf = getCookie("csrftoken")
    try {
        const response = await fetch(insertDataUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',// Specify the content type (JSON in this example).
                "X-CSRFToken":scrf, 
                // Add any other headers you may need, such as authorization headers.
            },

            });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json(); 
        
        if (DEBUG === true){
        if (result['msg'] == "Notifications are checked updated successfully")
        console.log('Notification are checked:', result);
        else console.log("couldn't checked Notifications:",result)
        }
    } catch (error) {
        if (DEBUG === true)
        console.error('An error occurred while updating data:', error);
    }
    document.getElementById('notification_pending_num').textContent = '';
}
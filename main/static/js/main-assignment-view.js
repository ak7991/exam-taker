//on assigned
function generateAssignmentUI(){
    title = currentAssignmentTitle
    _currentClass = currentClass
    _currentSection = currentSection
    let ref = firebase.database().ref("Chat"+'/'+ title+'/'+ _currentSection);
    ref.on('value', function(dataSnapshot){
        console.log(dataSnapshot.val())
    });
}

function viewAssignmentWindow(){
    title = currentAssignmentTitle
    $('#assignment-conduct-title').html(title);
    generateAssignmentUI();
}

function viewAssignment(e){
    let target = e.target.children[0];
    if(target == undefined){
        alert('Sorry there is some error. Please refresh the page or try reopening.')
        return false
    }
    $('.create-task-wrapper').css({'display':'none'});
    $('.assignments-container').css({'display':'none'});
    $('.assignment-window').css({'display':'block'});
    currentAssignmentTitle = target.textContent
    viewAssignmentWindow()
}

$('#section-list').on('change', function(){
    currentSection = $('#section-list').val()
    generateAssignmentUI()
})

function updateViewAssignmentBtn() {
    let viewAssignmentBtn = document.querySelectorAll('.open-view-assignment')
    viewAssignmentBtn.forEach(button => {
       button.addEventListener('click', viewAssignment) 
    })
}

$('#return-view-assignment').click(function(){
    $('.create-task-wrapper').css({'display':'none'});
    $('.assignments-container').css({'display':'block'});
    $('.assignment-window').css({'display':'none'});
})
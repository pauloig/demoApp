
function ApproveReject(event2, newS, id, msgAlert)
{

    event.preventDefault();
  

    if (confirm(msgAlert))
    {
        if (newS > 0)
        {
            window.location.href = "/timesheet/update_status/" + id + "/" + newS;
        }
    }  
    
}
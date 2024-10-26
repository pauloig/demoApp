{

    window.onload = function () {
        validateInputs();
        
        
    }

    // Function to validate Mileage
    function setMilleage(event) {       
        
        const startMileage = Number(document.getElementById("start_mileage").value)
        const endMileage = Number(document.getElementById("end_mileage").value)
        const totalMileage = document.getElementById("total_mileage")
        let   startMileageText = document.getElementById("start_mileage_text")
        let   endMileageText = document.getElementById("end_mileage_text")
        let savebtn = document.getElementById("save_btn");
        let result = false

        if ( startMileage!= 0 || endMileage != 0 )
        {
            if (endMileage <= startMileage)
            {
                startMileageText.innerHTML = "mileage must be smaller than ending mileage"
                endMileageText.innerHTML = "mileage must be greater than starting mileage" 
            }                                       

            if (startMileage <= 0 )
                startMileageText.innerHTML = "mileage must be greater than 0"

            if (endMileage <= 0 )
                endMileageText.innerHTML = "mileage must be greater than 0"   

            if ( startMileage > 0 && endMileage > 0 && endMileage > startMileage)
            {
                result = true
                startMileageText.innerHTML = "" 
                endMileageText.innerHTML = ""  
                totalMileage.value = (endMileage - startMileage ).toString()
            }
            else
                totalMileage.value = 0
                                                        
                                            
        }
        savebtn.disabled = !result 
    // setTime(result) 
                                                        
    }

    // Function to format text to hh24:mm:ss time format
    function num2time (num)
    {

        if (num < 100 && num > 0) num *=100;                                            
        
        let [_,hh,mm] = "0000"

        if (num > 0)
            [_,hh,mm] = num.toString().match(/(\d{1,2})(\d{2})$/)
            
                
        return `${hh.padStart(2,"0")}:${mm}`
    }

    // Function to validate if Time is Valid
    function setTime(event) {
                
        let startTime = document.getElementById("start_time")
        let startLunchTime = document.getElementById("start_lunch_time")
        let endLunchTime =  document.getElementById("end_lunch_time")
        let endTime = document.getElementById("end_time")
        let formStatus = false
        'use strict'
        let result = result2 = result3 = result4 = '' 

        if (event != null)
        {
            if (event.value > 0 && event.value < 100)
                event.value *=100
        }
    
        // Validate Time Format
        if (startTime.value != '')
            result = moment(num2time(startTime.value), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time')
        else 
            result = "Please fill out Clock In"


        if (endTime.value != '')
            result2 = moment(num2time(endTime.value), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time')
        else
            result2 = "Please fill out Clock Out"

        if (startLunchTime.value != '')    
            result3 = moment(num2time(startLunchTime.value), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time')

        if (endLunchTime.value != '')
            result4 = moment(num2time(endLunchTime.value), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time') 
        



        document.getElementById("start_time_text").innerHTML =  result
        document.getElementById("start_lunch_time_text").innerHTML =  result3
        document.getElementById("end_lunch_time_text").innerHTML =  result4
        document.getElementById("end_time_text").innerHTML =  result2

        if (result != 'Invalid Time' || result2 != 'Invalid Time' || result3 != 'Invalid Time' || result4 != 'Invalid Time')
            formStatus = true
        

        
        document.getElementById("save_btn").disabled = !formStatus
        console.log(!formStatus);

    
    }

    function validarCampos()
    {
        console.log("validando campos")
        setMilleage()
        setTime() 
    }




    function validateInputs(event) {

        if (event != null)
        {
            if (event.value > 0 && event.value < 100)
                event.value *=100
        }

        // Get input values
        let startTime = document.getElementById('start_time').value;
        let endTime = document.getElementById('end_time').value;
        let startLunchTime = document.getElementById('start_lunch_time').value;
        let endLunchTime = document.getElementById('end_lunch_time').value;
        
        let isValid = true;
        let result = '' 

       
    
        // Validate start time
        result = moment(num2time(startTime), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time');
        console.log('start',result);
        console.log(startTime);
        console.log(endTime);
        if ( startTime == ''   ) {
            isValid = false;
            document.getElementById("start_time_text").innerHTML = "Please fill Clock In field";
            document.getElementById("start_time_text").className = "error-text";
        }
        else if (result == 'Invalid Time')
        {
            isValid = false;
            document.getElementById("start_time_text").innerHTML = "Start time must be a valid Time Format";
            document.getElementById("start_time_text").className = "error-text";
        }
        else if (Number(startTime) >= Number(endTime))
            {
                isValid = false;
                document.getElementById("start_time_text").innerHTML = "Start time must be smaller than end Time";
                document.getElementById("start_time_text").className = "error-text";
            }
        else
        {
            document.getElementById("start_time_text").innerHTML = result;
            document.getElementById("start_time_text").className = "info-text";
        }

        
        // Validate end time
        result = moment(num2time(endTime), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time');
        console.log('end',result);
        console.log(startTime);
        console.log(endTime);
   
        if (endTime == '')  {
            isValid = false;
            document.getElementById("end_time_text").innerHTML = "Please fill Clock Out field";
            document.getElementById("end_time_text").className = "error-text";
        }
        else if (result == 'Invalid Time')
        {
            isValid = false;
            document.getElementById("end_time_text").innerHTML = "End time must be a valid Time Format";
            document.getElementById("end_time_text").className = "error-text";
        }
        else if (Number(endTime) <= Number(startTime))
        {
            isValid = false;
            document.getElementById("end_time_text").innerHTML = "End time must be greater than start time";
            document.getElementById("end_time_text").className = "error-text";
        }
        else
        {
            isValid = true;
            document.getElementById("end_time_text").innerHTML = result;
            document.getElementById("end_time_text").className = "info-text";
        }
    

        
        // Validate start lunch time if provided
       /* if (startLunchTime != '' || endLunchTime != '') {
            result = moment(num2time(startLunchTime), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time');
            console.log('start L',result);
            if (startLunchTime <= startTime || startLunchTime >= endTime) {
                isValid = false;
                document.getElementById("start_lunch_time_text").innerHTML = "start Lunch time must be a valid Time Format and greater than start time";
                document.getElementById("start_lunch_time_text").className = "error-text";
            }
            else
            {
                isValid = true;
                document.getElementById("start_lunch_time_text").innerHTML = result;
                document.getElementById("start_lunch_time_text").className = "info-text";
            }
    
            // Validate end lunch time if start lunch time is provided
            result = moment(num2time(endLunchTime), 'HH:mm:ss').format('h:mm:ss A').replace('Invalid date','Invalid Time');
            console.log('End L',result);
            if ( endLunchTime <= startTime || endLunchTime <= startLunchTime) {
                isValid = false;
                document.getElementById("end_lunch_time_text").innerHTML = "End time must be a valid Time Format and greater than start time";
                document.getElementById("end_lunch_time_text").className = "error-text";
            }
            else
            {
                isValid = true;
                document.getElementById("end_lunch_time_text").innerHTML = result;
                document.getElementById("end_lunch_time_text").className = "info-text";
            }

        }*/
        

        
        const startMileage = Number(document.getElementById("start_mileage").value);
        const endMileage = Number(document.getElementById("end_mileage").value);
        const totalMileage = document.getElementById("total_mileage");
        let   startMileageText = document.getElementById("start_mileage_text");
        let   endMileageText = document.getElementById("end_mileage_text");
        let savebtn = document.getElementById("save_btn");
        let totalHours = 0;
       
        

        if ( startMileage!= 0 || endMileage != 0 )
        {
            if (endMileage <= startMileage)
            {
                isValid= false
                startMileageText.innerHTML = "mileage must be smaller than ending mileage"
                endMileageText.innerHTML = "mileage must be greater than starting mileage" 
            }       
            else
                isValid= true                                

            if (startMileage <= 0 )
            {
                isValid= false
                startMileageText.innerHTML = "mileage must be greater than 0"
            }                
            else
                isValid= true

            if (endMileage <= 0 )
            {
                isValid= false
                endMileageText.innerHTML = "mileage must be greater than 0"   
            }                
            else
                isValid= true

            if ( startMileage > 0 && endMileage > 0 && endMileage > startMileage)
            {
                isValid= true
                startMileageText.innerHTML = "" 
                endMileageText.innerHTML = ""  
                totalMileage.value = (endMileage - startMileage ).toString()
            }
            else
                isValid= false
                                                        
                                            
        }


        // Enable or disable the save button based on validity
        document.getElementById('save_btn').disabled = !isValid;
        /*if (!isValid)
            document.getElementById('btn btn-success send-btn').style.display = 'none';
        else
            document.getElementsByClassName('btn btn-success send-btn').style.display = 'block';*/


        totalHours = calculateHours(startTime, endTime, startLunchTime, endLunchTime);
        document.getElementById("total_hours").value = totalHours;
    
        return isValid;
    }
    
    function prueba()
    {

        event.preventDefault();

        console.log(document.getElementById("newstatus"));
        if (confirm("Are you sure to Send this timesheet"))
        {
            document.getElementById("estatus").value = 2;
            document.getElementById("newstatus").value = 2;
            document.getElementById("Timesheet").submit();
        }
            
    }

    function updateStatus(event2, newS, msgAlert)
    {

        event.preventDefault();
        result = validateInputs(null);

        const dateSelected = document.getElementById("date").value;
        const Location = document.getElementById("Location").value;
        message = 'Please fill the required fields ';
        
        if (dateSelected.toString().trim().length == 0)
        {
            result = false;
            message = 'Please select a valid date';
            console.log('Date not Selected')
        }
        else
            console.log('date Selected: ',dateSelected);

        if (Location.toString().trim().length == 0)
        {
            result = false;
            message = 'Please select a valid Location';
            console.log('Date not Selected')
        }
        else
            console.log('Location Selected: ',Location);

      
        if (!result)
            alert(message);
        else
        {
            if (confirm(msgAlert))
            {
                if (newS > 0)
                {
                    document.getElementById("estatus").value = newS;
                    document.getElementById("newstatus").value = newS;
                    document.getElementById("Timesheet").submit();
                }
                else
                {
                    
                    document.getElementById("Timesheet").submit();
                }
                
            }  
            
        }

    }


    function validateDecimals(value) {
        try {
            return parseFloat(value.toString()).toFixed(2);
        } catch (e) {
            return 0;
        }
    }
    
    function calculateHours(startTime, endTime, lunchStartTime, lunchEndTime) {

        

        let total = 0;

        if (parseFloat(startTime) > 0 && parseFloat(endTime) > 0 ) {
            if (parseFloat(startTime) > parseFloat(endTime)) {
                total = 0;
            } else {
                
                // convertir a decimal
                startTime = parseFloat(startTime) / 100;
                
                let st_h = Math.floor(startTime);
                let st_m = parseFloat(startTime % 1) * 100;      
                let st_total = parseFloat(st_h + parseFloat(st_m / 60));
                

                endTime = parseFloat(endTime) / 100;
                let et_h = Math.floor(endTime);
                let et_m = parseFloat(endTime % 1) * 100;
                let et_total = parseFloat(et_h + parseFloat(et_m / 60));


                total = et_total - st_total;
            }
        }
    
        let totalLunch = 0;
        if (parseFloat(lunchStartTime) > 0  && parseFloat(lunchEndTime) > 0) {
            lunchStartTime = parseFloat(lunchStartTime) / 100;
            lunchEndTime = parseFloat(lunchEndTime) / 100;
    
            if (lunchStartTime > lunchEndTime) {
                totalLunch = 0;
            } else if (lunchStartTime > endTime || lunchEndTime > endTime) {
                totalLunch = 0;
            } else {
                // convertir a decimal
                let lst_h = Math.floor(lunchStartTime);
                let lst_m = parseFloat(lunchStartTime % 1) * 100;
                let lst_total = parseFloat(lst_h + parseFloat(lst_m / 60));
    
                let let_h = Math.floor(lunchEndTime);
                let let_m = parseFloat(lunchEndTime % 1) * 100;
                let let_total = parseFloat(let_h + parseFloat(let_m / 60));
    
                totalLunch = let_total - lst_total;
            }
        }
    
        let endTotal = total - totalLunch;
        console.log('Total: ', parseFloat(endTotal).toFixed(2));
        return parseFloat(endTotal).toFixed(2);
    }


}

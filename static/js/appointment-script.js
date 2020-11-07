saveButton = document.querySelectorAll(".select-appointment");
deleteButton = document.querySelectorAll(".delete-appointment");
appointmentDate = document.querySelector("#appointment_date");

// window.onload = appointmentDate.min = new Date().today();

assignedDoctor = document.querySelector("#assignedDoctor");
appointmentMessage = document.querySelector("#appointmentMessage");

saveButton.forEach((currentButton) => {
  currentButton.addEventListener("click", () => {
    console.log("APPOINTMENT", currentButton.dataset.appointment);
    date = appointmentDate.value;
    assigned_doctor = assignedDoctor.value;
    sendSelectedAppointment(currentButton.dataset.appointment, date, assigned_doctor, "select");
  });
});

sendSelectedAppointment = (patientId, date, assignedDoctor, action) => {
  let url = "../select_appointment/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      patientId: patientId,
      appointmentDate: date,
      assignedDoctor: assignedDoctor,
      action: action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((result) => {
      toastr.success(result);
      console.log(result);
    });
};

function preventD(element) {
  element.preventDefault();
}

deleteButton.forEach((currentButton) => {
  currentButton.addEventListener("click", () => {
    console.log("DELETE", currentButton.dataset.del);
    sendDeleteAppointment(currentButton.dataset.del, "select");
  });
});


function getDeletedData(e) {
  appDeleteBtn = document.querySelector("#appDeleteBtn");
  appDeleteBtn.dataset.del = e.dataset.appid;
}



sendDeleteAppointment = (appointmentId, action) => {
  let url = "../patients/delete_appointment/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      appointmentId: appointmentId,
      action: action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((result) => {
      // toastr.success(result);
      console.log(result);
      location.reload();
    });
};

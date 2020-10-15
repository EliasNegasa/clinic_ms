saveButton = document.querySelectorAll(".select-appointment");
appointmentDate = document.querySelector("#appointment_date");
appointmentMessage = document.querySelector("#appointmentMessage");

saveButton.forEach((currentButton) => {
  currentButton.addEventListener("click", () => {
    console.log("APPOINTMENT", currentButton.dataset.appointment);
    date = appointmentDate.value;
    sendSelectedAppointment(currentButton.dataset.appointment, date, "select");
  });
});

sendSelectedAppointment = (patientId, date, action) => {
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




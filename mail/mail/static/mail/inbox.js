document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(event, email=undefined) {
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = (email === undefined ? "" : email.sender);
  document.querySelector('#compose-subject').value = 
    (email === undefined ? "" : (email.subject.substring(0,4) === "Re: " ? email.subject : "Re: " + email.subject));
  document.querySelector('#compose-body').value = 
    (email === undefined ? "" : "On " + email.timestamp + " " + email.sender + " wrote:\n" + email.body + "\n");

  // Send Mail
  document.querySelector('#compose-form').onsubmit = ()=> compose();
}

function compose() {
  const email = {
    user: document.querySelector('input').value,
    recipients: document.querySelector('#compose-recipients').value,
    subject: document.querySelector('#compose-subject').value,
    body: document.querySelector('#compose-body').value
  };

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: email.recipients,
      subject: email.subject,
      body: email.body
    })
  })
  .then(Response => Response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  })


  // setTimeout(function (){
  
  //   load_mailbox('sent');
              
  // }, 250);
  
  return false;
}


function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    document.querySelector('#emails-view').append(arrayToTable(emails, mailbox));
  });
}

function arrayToTable(arr, mailbox) {
  if (arr.length > 0) {
    // Create Table Headeers
    const tbl = document.createElement('table');
    tbl.className = "mailTable"
    const tblHeader = document.createElement('thead');
    // Sender Header
    const th_sender = document.createElement('th');
    th_sender.innerHTML="FROM";
    tblHeader.appendChild(th_sender);
    // Subject Header
    const th_subject = document.createElement('th');
    th_subject.innerHTML="SUBJECT";
    tblHeader.appendChild(th_subject);
    // Timestamp Header
    const th_timestamp = document.createElement('th');
    th_timestamp.innerHTML="TIME";
    tblHeader.appendChild(th_timestamp);

    tbl.appendChild(tblHeader);

    const tblBody = document.createElement('tbody');
    arr.forEach((email)=> {
      const tr = document.createElement('tr');
      console.log(email.read)
      tr.className = "emailRow" + (email.read ? " readed" : " unread");
      console.log(tr.className)
      // Create Table cells
      // Sender
      const td_sender = document.createElement('td');
      td_sender.className = "emailCell";
      td_sender.addEventListener('click', ()=> loadEmail(email.id, mailbox));
      td_sender.innerHTML = email.sender;
      tr.appendChild(td_sender);
      // Subject
      const td_subject = document.createElement('td');
      td_subject.className = "emailCell";
      td_subject.addEventListener('click', ()=> loadEmail(email.id, mailbox));
      td_subject.innerHTML = email.subject
      tr.appendChild(td_subject);
      // Timestamp
      const td_timestamp = document.createElement('td');
      td_timestamp.className="emailCell";
      td_timestamp.addEventListener('click', ()=> loadEmail(email.id, mailbox));
      td_timestamp.innerHTML = email.timestamp;
      tr.appendChild(td_timestamp);
      // Archive handler
      if (mailbox != "sent") {
        const td_archive = document.createElement('td');
        td_archive.className = "tdArchive";
        const btn_archive = document.createElement('button');
        td_archive.appendChild(btn_archive);
        btn_archive.className = "btnArchive";
        btn_archive.innerHTML = (mailbox == "inbox" ? "Archive" : "Unarchive");
        btn_archive.addEventListener('click', ()=> {
          // Read tag
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: (mailbox == "inbox" ? true : false)
            })
          })
          .then(response => load_mailbox('inbox'));
        });
        tr.appendChild(td_archive);
      }

      tblBody.appendChild(tr);
    });
    tbl.appendChild(tblBody);
    //tbl.setAttribute("border", "2");

    return tbl;
  }
  return "";
}

function loadEmail(emailId, mailbox) {
  document.querySelector('#emails-view').innerHTML = "";

  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      const div = document.createElement('div');
  
      // From
      const p_from = document.createElement('p')
      p_from.className = "emailHeader";
      const span_from = document.createElement('span');
      span_from.className = 'title';
      span_from.innerHTML = "From: ";
      p_from.append(span_from);
      p_from.append(email.sender);
      
      // To
      const p_to = document.createElement('p');
      p_to.className = "emailHeader";
      const span_to = document.createElement('span');
      span_to.className = "title";
      span_to.innerHTML = "To: ";
      p_to.append(span_to);
      p_to.append(email.recipients); // Should be currect

      // Subject
      const p_subject = document.createElement('p');
      p_subject.className = "emailHeader";
      const span_subject = document.createElement('span');
      span_subject.className = "title";
      span_subject.innerHTML = "Subject: ";
      p_subject.append(span_subject);
      p_subject.append(email.subject);

      // Timestamp
      const p_timestamp = document.createElement('p');
      p_timestamp.className = "emailHeader";
      const span_timestamp = document.createElement('span');
      span_timestamp.className = "title";
      span_timestamp.innerHTML = "Timestamp: ";
      p_timestamp.append(span_timestamp);
      p_timestamp.append(email.timestamp);

      // Reply
      const btn_reply = document.createElement('button');
      btn_reply.className = "btn btn-primary";
      btn_reply.innerHTML = "Reply";
      btn_reply.addEventListener('click', ()=> {
        compose_email(undefined, email);
      });

      // hr
      const hr = document.createElement('hr');

      // body
      const body = document.createElement('p');
      body.className = "emailBody";
      body.innerHTML = email.body.replace(/\n\r?/g, '<br />');

      // Concatenating elements
      div.append(p_from);
      div.append(p_to);
      div.append(p_subject);
      div.append(p_timestamp);
      if (mailbox != "sent") {div.append(btn_reply);}
      div.append(hr);
      div.append(body);

      document.querySelector('#emails-view').append(div);

      // Read tag
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
  });

  
}
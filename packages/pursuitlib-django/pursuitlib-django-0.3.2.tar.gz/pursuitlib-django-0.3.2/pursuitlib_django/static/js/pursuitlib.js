/*
  Collapse toggle
 */

function onCollapseToggled(sender)
{
    let child = sender.children.length > 0 ? sender.children[0] : null;

    if(child != null)
    {
        if(sender.classList.contains("collapsed"))
        {
            child.classList.remove("fa-chevron-up");
            child.classList.add("fa-chevron-down");
        }
        else
        {
            child.classList.remove("fa-chevron-down");
            child.classList.add("fa-chevron-up");
        }
    }
}


/*
  Modal form
 */

function onModalFormKeyDown(id, event) {
    let keycode = (event.keyCode ? event.keyCode : event.which);

    if(keycode === 13) { // If the "enter" key is down
        event.preventDefault();
        $(`#${id}-submit`).click();
    }
}

/*
  REST utilities
 */

const XHR_COMPLETE = 4
const HTTP_OK = 200

function sendGet(url, callback = null) {
    let request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.setRequestHeader("Accept", "application/json");

    request.onreadystatechange = function () {
        if (request.readyState === XHR_COMPLETE) {
            let response = null;
            if(request.status === HTTP_OK)
                response = JSON.parse(request.responseText);

            if(callback)
                callback(response);
        }
    };

    request.send();
}

function sendPost(url, data, callback = null) {
    let request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept", "application/json");

    request.onreadystatechange = function () {
        if (request.readyState === XHR_COMPLETE) {
            let response = null;
            if(request.status === HTTP_OK)
                response = JSON.parse(request.responseText);

            if(callback)
                callback(response);
        }
    };

    let dataText = JSON.stringify(data);
    request.send(dataText);
}

/*
  GET & POST links
 */

function clickOnGetLink(link) {
    window.location.href = link.getAttribute("data-href");
}

function clickOnPostLink(link) {
    let target = link.getAttribute("data-post");
    let formData = {}

    // Get global form data
    document.querySelectorAll("meta[data-post]").forEach(e => {
        for(let attr of e.attributes) {
            if(!attr.name.startsWith("data-post-"))
                continue;

            let name = attr.name.substring("data-post-".length);
            formData[name] = attr.value;
        }
    });

    // Get local form data
    for(let attr of link.attributes) {
        if(!attr.name.startsWith("data-post-"))
            continue;

        let name = attr.name.substring("data-post-".length);
        formData[name] = attr.value;
    }

    // Create form from data
    let formDef = `<form action="${target}" method="post" hidden>`;
    for(let name of Object.keys(formData)) {
        let value = formData[name];
        formDef += `<input type="hidden" name="${name}" value="${value}">`;
    }

    formDef += '</form>';

    let form = $(formDef);

    // Add the form to the document
    // It is hidden, so it doesn't actually appear on the page
    $('body').append(form);

    form.submit();
}


/*
  Prepare document when ready
 */

$(document).ready(() => {
    // Prepare Bootstrap tooltips
    document.querySelectorAll("[title]").forEach(e => {
      new bootstrap.Tooltip(e);
    });

    // Prepare GET links
    document.querySelectorAll("[data-href]").forEach(e => {
        if(e.tagName === "A")
            e.setAttribute("href", "javascript:void(0)");
        e.onclick = () => clickOnGetLink(e);
    });

    // Prepare POST links
    document.querySelectorAll("[data-post]").forEach(e => {
        if(e.tagName === "A")
            e.setAttribute("href", "javascript:void(0)");
        e.onclick = () => clickOnPostLink(e);
    });
});

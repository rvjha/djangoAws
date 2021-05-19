let createClassBtn = document.getElementById("createClassBtn");
let uploadJsonBtn = document.getElementById("uploadJsonBtn");
let musicJsonFile = document.getElementById("musicJsonFile");
let collectImageBtn = document.getElementById("collectImageBtn");
let createBucketBtn = document.getElementById("createBucketBtn");
var text = document.getElementById("status");


function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		var cookies = document.cookie.split(";");
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

// check if music class exists
function table_exists(dType, table) {
	let data = {
		"action": "get_table",
		"type": dType,
		"table": table
	};
	$.ajax({
		type: "POST",
		url: "check_table",
		data: data,
		credentials: "same-origin",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			table_response(dType, response)
		},
	});
}

function table_response(ty, response) {
	var btn = " ";
	if (ty == "table") {
		btn = createClassBtn;
	}
	if (ty == "s3") {
		btn = createBucketBtn;
	}
	if (response == "true") {
		btn.setAttribute("disabled", true);
		btn.classList.remove("btn-primary");
		btn.classList.add("btn-danger");
		if (ty == "table") {
			btn.innerHTML = "Table Already Exists!";
		} else {
			btn.innerHTML = "Bucket Already Exists!";
		}
	} else {
		btn.classList.remove("btn-danger");
		btn.classList.add("btn-primary");
		btn.setAttribute("enable", true);
	}

}

// get users
function get_users() {
	let getUsers = {
		"action": "get_users",
	};

	$.ajax({
		type: "POST",
		url: "get_users",
		data: getUsers,
		datatype: "json",
		credentials: "same-origin",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			// console.log(response)
			if (response == "Invalid Request") {
				show_msg_log(0, "status", response);
			} else {
				create_user_table(response);
			}
		},
	});
}

$(document).ready(() => {
	text.innerHTML = "";
	text.style.display = "none";
	get_users();
	table_exists("table", "music");
	table_exists("s3", "romibucket");
});

// create music table
createClassBtn.addEventListener("click", () => {
	create_table_request("table", "music")
});

// show response messages
function show_msg_log(tp, id, m) {
	var msg = document.getElementById(id);
	call_loader(true)
	if (tp == 1) {
		msg.style.color = "green";
	} else {
		msg.style.color = "red";
	}
	msg = document.getElementById("status");
	msg.innerHTML = m;
	text.style.display = "inline-block";

	setTimeout(() => {
		msg.innerHTML = "";
		msg.style.display = "none";
	}, 5000);
}

// create table
function create_user_table(data) {
	let table = document.getElementById("UserTable");

	if (data != false) {
		// console.log(data)
		var col;
		var i = 1;
		data.forEach((element) => {
			let row = document.createElement("tr");
			col = document.createElement("td");
			row.appendChild(col);
			col.innerHTML = i;
			for (const key in element) {
				if (Object.hasOwnProperty.call(element, key)) {
					const e = element[key];
					col = document.createElement("td");
					col = document.createElement("td");
					col.style.paddingLeft = "19%";
					col.innerHTML = e;
					row.appendChild(col);
				}
			}
			table.appendChild(row);
			i++;
		});
	} else {
		let row = document.createElement("tr");
		let col = document.createElement("td");
		col.colSpan = "3";
		col.classList.add("text-center");
		col.classList.add("text-danger");
		col.innerHTML = "No Data Found";
		row.appendChild(col);
		table.appendChild(row);
	}
}

// upoad json file 
uploadJsonBtn.addEventListener("click", (e) => {
	e.preventDefault();
	let file = document.getElementById("musicJsonFile").files[0];
	var allowedExtensions = /(\.json)$/g;
	if (file) {
		if (allowedExtensions.exec(file.name)) {
			call_loader(false)
			$.ajax({
				type: "POST",
				url: "upload_music_data",
				data: file,
				cache: false,
				processData: false,
				// dataType: "json",
				// contentType: "application/json",
				credentials: "same-origin",
				headers: {
					"X-CSRFToken": getCookie("csrftoken"),
				},
				success: function (response) {

					if (response == "Table not exists" || response == "not authroise") {
						show_msg_log(0, "status", response);
					} else {
						document.getElementById("musicJsonFile").value = "";
						show_msg_log(1, "status", "Data Uploaded!");
					}
				},
			});
		} else {
			show_msg_log(0, "status", "Invalid file format!");
		}
	} else {
		show_msg_log(0, "status", "Please select a json file!");
	}
});

// collect images from table and upload it to rominaBucket
collectImageBtn.addEventListener("click", () => {
	let data = {
		"action": "collect_images",
	};
	call_loader(false)
	$.ajax({
		type: "POST",
		url: "collect_image_data",
		data: data,
		credentials: "same-origin",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			call_loader(false)
			if (response == "uploaded") {
				show_msg_log(1, "status", "Images Collected!");
			} else {
				show_msg_log(0, "status", "error");
			}
		},
	});
});

// create bucket 
// create music table
createBucketBtn.addEventListener("click", () => {
	create_table_request("s3", "romibucket")

});

function create_table_request(dt, table) {
	let url = ""
	let data = {
		"action": "create_data",
		"table": table,
		"type": dt
	};
	if(dt == "s3"){
		url = "build_bucket";
	}
	if(dt == "table"){
		url = "build_table";
	}
	call_loader(false)
	$.ajax({
		type: "POST",
		url: url,
		data: data,
		credentials: "same-origin",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			if (response == "true") {
				table_exists(dt,table);
				if(dt == "s3"){
					show_msg_log(1, "status", "S3 Bucket has been created");
				}
				if(dt == "table"){
					show_msg_log(1, "status", "Dynamodb Table has been created");
				}
			}else {
				show_msg_log(0, "status", "status");
			}
		},
	});
}

function call_loader(status){
	console.log(status)
	let loader = document.getElementById('loader')
	if(status){
		loader.style.display='none';
	}else{
		loader.style.display='block';
	}
}
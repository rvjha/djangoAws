var musicIcon = document.getElementById("backToHome");
musicIcon.onclick = () => {
	window.location.href = "/";
};

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

$(document).ready(() => {
	get_music_table();

});
// =========================== get users =========================

function get_music_table() {
	let url = "";
	let rUrl = window.location.href
	let uArr = rUrl.split("/")
	for (let i = 0; i < uArr.length; i++) {
		if (uArr[i] == "query" || uArr[i] == "profile") {
			url = 'get_music_data'
			break
		}
		url = 'accounts/get_music_data'
	}
	let getUsers = {
		action: "get_music_data",
	};
	$.ajax({
		type: "POST",
		url: url,
		data: getUsers,
		datatype: "json",
		credentials: "same-origin",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			document.getElementById("pages").innerHTML = "Total Records: " + response.length;
			if (response) {
				create_table(response);
			} else {
				create_table(false)
			}
		},
	});
}

// =========================== show status =========================

function show_msg(tp, id, msg) {
	var text;
	text = document.getElementById(id);
	if (tp == 1) {
		text.style.color = "green";
	} else {
		text.style.color = "red";
	}
	text.innerHTML = msg;
	text.style.display = "inline-block";

	setTimeout(() => {
		text.innerHTML = "";
		text.style.display = "none";
	}, 5000);
}

let tb;
// =========================== create table =========================

function create_table(res) {
	tb = document.getElementById("mainTable");
	tb.innerHTML = ""
	if (res == "Invalid Request" || res == "Table not exists" || res == false) {
		let row = document.createElement("tr");
		let col = document.createElement("td");
		let heading = document.createElement("h1");
		col.colSpan = "6";
		col.classList.add("text-center");
		col.classList.add("text-danger");
		col.classList.add("p-3");
		heading.classList.add("jumbotron");
		heading.innerHTML = "No Data Found";
		col.appendChild(heading);
		row.appendChild(col);
		tb.appendChild(row);
	} else {
		var col;
		var i = 1;
		res.forEach((element) => {
			let row = document.createElement("tr");
			col = document.createElement("td");
			row.appendChild(col);
			col.innerHTML = i;
			for (const key in element) {
				if (Object.hasOwnProperty.call(element, key)) {
					const e = element[key];
					col = document.createElement("td");
					if (key == "img_url") {
						let imgAr = (element[key].split('/'));
						imgName = imgAr[(imgAr.length) - 1];
						imgBlock = document.createElement('img')
						imgUrl = "https://romibucket.s3.amazonaws.com/" + imgName;
						imgBlock.setAttribute('src', imgUrl)
						imgBlock.setAttribute('class', 'imgBlock')
						col.appendChild(imgBlock);
					} else {
						col.innerHTML = e;
					}
					row.appendChild(col);
				}
				row.appendChild(col);
			}
			col = document.createElement("td");
			row.appendChild(col);
			let rowId = 'row-' + element['title']
			row.setAttribute('id', rowId)
			let btn = document.createElement("button");
			btn.classList.add("btn");
			let sId = element["title"];
			let ar = element['artist']
			btn.setAttribute("onclick", "sub_fun('" + sId + "')");
			btn.setAttribute("id", sId);
			btn.setAttribute("data-artist", ar);
			btn.innerHTML = "Subscribe";

			col.appendChild(btn);
			row.appendChild(col);
			tb.appendChild(row);
			i++;
		});
	}
	// pagination();

	user_sub_list();
}
// =========================== pagination =========================

// function pagination() {
// 	tb = document.getElementById("mainTable");
// 	let rows = tb.getElementsByTagName("tr");
// 	let perPageRow = 10;
// 	let pages = Math.ceil(rows.length / perPageRow);
// 	try {
// 		document.getElementById("pages").innerHTML = pages;
// 		for (let i = 1; i < rows.length; i++) {
// 			if (i > perPageRow - 1) {
// 				rows[i].style.display = "none";
// 			}
// 		}
// 	} catch (e) {

// 	}

// }

// =========================== subscription =========================

function sub_fun(id) {
	let url = "";
	let btn = document.getElementById(id);
	let artist = btn.getAttribute('data-artist');
	let rUrl = window.location.href
	let uArr = rUrl.split("/")
	for (let i = 0; i < uArr.length; i++) {
		if (uArr[i] == "query" || uArr[i] == "profile") {
			url = 'subscribe'
			break
		}
		url = 'accounts/subscribe'
	}

	var data = {
		'sId': id,
		'artist': artist,
	};
	$.ajax({
		type: "POST",
		url: url,
		data: data,
		credentials: "same-origin",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			// console.log(response);
			if (response == "require_loign") {
				show_msg(0, "msg", "Require Login!")
			} else {
				if (response == "sub") {
					document.getElementById(id).classList.add('btn-success')

				} else if (response == "unsub") {
					document.getElementById(id).classList.remove('btn-success')
				} else {
					show_msg(0, "msg", "Error!")
				}
			}
		},
	});
}

// =========================== register =========================
try {
	let frmReg = document.getElementById("regFrm");
	frmReg.addEventListener("submit", (e) => {
		e.preventDefault();
		var data = {}
		let nm = document.getElementById("regName");
		let email = document.getElementById("regEmail");
		let pass = document.getElementById("regPass");
		let pass1 = document.getElementById("regPass1");
		let msg = [];
		if (!nm.value) {
			msg.push({
				regNameErr: "Please enter your name!",
			});
		}
		if (!email.value) {
			msg.push({
				regEmailErr: "Please enter your name!",
			});
		}
		if (!pass.value) {
			msg.push({
				regPassErr: "Please enter your password!",
			});
		}
		if (!pass1.value) {
			msg.push({
				regPass1Err: "Please enter your password!",
			});
		}
		if (pass1.value.length <= 10) {
			msg.push({
				msg: "must be 10 digit long",
			});
		}

		if (pass1.value !== pass.value) {
			msg.push({
				regPass1Err: "Password not match",
			});
		}
		if (msg.length) {
			msg.forEach((element) => {
				show_msg(0, Object.keys(element), element[Object.keys(element)]);
			});
		} else {
			data = {
				email: email.value,
				name: nm.value,
				pass: pass.value,
			};
			$.ajax({
				type: "POST",
				url: "register_req",
				data: data,
				headers: {
					"X-CSRFToken": getCookie("csrftoken"),
				},
				success: function (response) {
					if (response == "User Added") {
						show_msg(1, "msg", response);
						frmReg.reset();
						window.location.href = "login";
					} else {
						show_msg(0, "msg", response);
					}
				},
			});
		}
	});
} catch (e) {

}
// =========================== login =========================
try {

	let frmlog = document.getElementById("logFrm");
	frmlog.addEventListener("submit", (e) => {
		let url = "";
		let rUrl = window.location.href
		let uArr = rUrl.split("/")
		for (let i = 0; i < uArr.length; i++) {
			if (uArr[i] == "login") {
				url = 'login_req'
				break
			}
			url = 'accounts/login_req'
		}
		e.preventDefault();

		var data = {}
		let email = document.getElementById("logEmail");
		let pass = document.getElementById("logPass");
		let msg = [];
		if (!email.value) {
			msg.push({
				logEmailErr: "Please enter your Email!",
			});
		}
		if (!pass.value) {
			msg.push({
				logPassErr: "Please enter your Password!",
			});
		}
		if (msg.length) {
			msg.forEach((element) => {
				show_msg(0, Object.keys(element), element[Object.keys(element)]);
			});
		} else {
			data = {
				email: email.value,
				pass: pass.value,
			};
			$.ajax({
				type: "POST",
				url: url,
				data: data,
				headers: {
					"X-CSRFToken": getCookie("csrftoken"),
				},
				success: function (response) {
					// console.log(response)
					if (response == "False") {
						show_msg(0, "msg", "Not valid credentials!");
						frmlog.reset();
					} else {
						window.location.href = "/";
						frmlog.reset();
					}
				},
			});
		}
	});
} catch (e) {

}

// =========================== checkbox  =========================
let checkStatus;
let qSong;

function get_check() {
	checkStatus = document.getElementById("getSong");
	qSong = document.getElementById("querySong");
	if (checkStatus.checked) {
		qSong.style.display = "inline-block";
	} else {
		qSong.style.display = "none";
		qSong.value = "";
	}
}
// =========================== query =========================

function search_query() {
	let qArtist = document.getElementById("queryArtist");
	qSong = document.getElementById("querySong");
	checkStatus = document.getElementById("getSong");
	var data;
	if (qArtist.value == undefined || qArtist.value == "") {
		show_msg(0, "msg", "Please enter Artist name");
		return
	}
	if (checkStatus.checked && (qSong.value == undefined || qSong.value == "")) {
		show_msg(0, "msg", "Please enter song name");
		return
	}
	if (checkStatus.checked) {
		data = {
			"artist": qArtist.value,
			"title": qSong.value
		}
	} else {
		data = {
			"artist": qArtist.value,
		}
	}
	$.ajax({
		type: "POST",
		url: "query",
		data: data,
		credentials: "same-origin",
		datatype: "json",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			// console.log(response)
			if (response) {
				create_table(response)
			} else {
				create_table(response)
				show_msg(0, "msg", "No data found");
			}
		},
	});
}

// =========================== get subscribe list =========================
function user_sub_list() {
	let url = "";
	let rUrl = window.location.href
	let uArr = rUrl.split("/")
	for (let i = 0; i < uArr.length; i++) {
		if (uArr[i] == "query" || uArr[i] == "profile") {
			url = 'get_sub_data'
			break
		}
		url = 'accounts/get_sub_data'
	}
	$.ajax({
		type: "POST",
		url: url,
		credentials: "same-origin",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
		},
		success: function (response) {
			if (response.length >= 0) {
				toggle_button(response)
				display_user_sub(response)
			}
		}
	});
}

// =========================== toggle sub buttons =========================
function toggle_button(data) {
	// console.log(data)
	let table = document.getElementById('mainTable')
	let td = table.getElementsByTagName('td')
	let btns = table.getElementsByTagName('button')
	for (const key in data) {
		if (Object.hasOwnProperty.call(data, key)) {
			const element = data[key];
			try {
				btn = document.getElementById(element['songId'])
				btn.classList.add('btn-success')

			} catch (error) {

			}

		}
	}

}

function display_user_sub(data) {
	let url = "";
	let rUrl = window.location.href
	let uArr = rUrl.split("/")
	for (let i = 0; i < uArr.length; i++) {
		if (uArr[i] == "query" || uArr[i] == "profile") {
			url = 'profile'
			break
		}
		url = false
	}
	if (url == "profile") {
		tb = document.getElementById("mainTable");
		let rows = tb.getElementsByTagName("tr");
		try {
			document.getElementById("pages").innerHTML = "Subscribed Records: " + data.length;
			for (let i = 0; i < rows.length; i++) {
				rows[i].style.display = "none";
			}
			for (const key in data) {
				if (Object.hasOwnProperty.call(data, key)) {
					const element = data[key];
					document.getElementById('row-' + element['songId']).style.display = ""
				}
			}
		} catch (e) {

		}
	}
}


function service_div(service_name, num_ok, num_warnings, num_errors) {
	let div_1 = document.createElement('div');
	div_1.classList.add(...['col-xl-1', 'col-lg-3', 'col-md-3', 'col-sm-6', 'serviceDiv']);

	let div_2 = document.createElement('div');
	div_2.classList.add(...['row', 'serviceRow']);
	div_2.style = "border: 5px solid green;";

	let div_3 = document.createElement('div');
	div_3.classList.add(...['col-sm-7', 'col-md-7', 'col-lg-8', 'textCol']);

	let div_4 = document.createElement('div');
	div_4.classList.add(...['textTable']);

	let div_5 = document.createElement('div');
	div_5.classList.add(...['textInnerTable']);
	div_5.style = "color: green;";

	let div_6 = document.createElement('div');
	div_6.classList.add(...['col-sm-5', 'col-md-5', 'col-lg-4', 'countDiv']);

	let div_7 = document.createElement('div');
	div_7.classList.add(...['countRow']);

	let img_1 = document.createElement('img');
	img_1.setAttribute("src", "/rlmon/public_resources/img/icons/ok.png");
	img_1.classList.add(...['statusIcon']);

	let div_8 = document.createElement('div');
	div_8.classList.add(...['countRow']);

	let img_2 = document.createElement('img');
	img_2.setAttribute("src", "/rlmon/public_resources/img/icons/warning.png");
	img_2.classList.add(...['statusIcon']);

	let div_9 = document.createElement('div');
	div_9.classList.add(...['countRow']);

	let img_3 = document.createElement('img');
	img_3.setAttribute("src", "/rlmon/public_resources/img/icons/error.png");
	img_3.classList.add(...['statusIcon']);

	div_5.appendChild(document.createTextNode(service_name));
	div_4.appendChild(div_5);
	div_3.appendChild(div_4);
	div_2.appendChild(div_3);
	div_7.appendChild(img_1);
	div_7.appendChild(document.createTextNode(num_ok));
	div_6.appendChild(div_7);
	div_8.appendChild(img_2);
	div_8.appendChild(document.createTextNode(num_warnings));
	div_6.appendChild(div_8);
	div_9.appendChild(img_3);
	div_9.appendChild(document.createTextNode(num_errors));
	div_6.appendChild(div_9);
	div_2.appendChild(div_6);
	div_1.appendChild(div_2);
	return div_1;
}

function simple_div() {
	let aaa = document.createElement('div');
	aaa.id = aaa;
	aaa.classList.add(...['bbb']);

	let bbb = document.createElement('div');
	bbb.id = bbb;
	bbb.classList.add(...['ccc']);

	let ccc = document.createElement('div');
	ccc.id = ccc;
	ccc.classList.add(...['ddd']);

	let div_1 = document.createElement('div');

	aaa.appendChild(bbb);
	aaa.appendChild(ccc);
	aaa.appendChild(div_1);
	return aaa;
}

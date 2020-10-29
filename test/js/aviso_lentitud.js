		//AUTOGENERATED FUNCTION. Check the script in https://github.com/vLabayen/html2js
		//The output should be a element such that contains the following structure:
		//<h3 style="margin-bottom:50px; color:#ccc; font-size 12pt; text-align:center" id="aviso_lentitud">
		//	<span class="alert alert-danger">
		//		<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
		//		Atención: Puede experimentar lentitud si elige un gran intervalo de tiempo.
		//	</span>
		//</h3>
		function aviso_lentitud() {
			let aviso_lentitud = document.createElement('h3');
			aviso_lentitud.style = "margin-bottom:50px; color:#ccc; font-size 12pt; text-align:center";
			aviso_lentitud.id = "aviso_lentitud";

			let span_1 = document.createElement('span');
			span_1.classList.add(...['alert', 'alert-danger']);

			let span_2 = document.createElement('span');
			span_2.classList.add(...['glyphicon', 'glyphicon-exclamation-sign']);
			span_2.setAttribute("aria-hidden", "true");

			span_1.appendChild(span_2);
			span_1.appendChild(document.createTextNode('Atención: Puede experimentar lentitud si elige un gran intervalo de tiempo.'));
			aviso_lentitud.appendChild(span_1);
			return aviso_lentitud;
		}
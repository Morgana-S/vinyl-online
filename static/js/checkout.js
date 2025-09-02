document.addEventListener('DOMContentLoaded', function () {
	const showNewAddressBtn = document.getElementById('show-new-address-btn');
	const newAddressFields = document.getElementById('new-address-fields');
	const savedAddressSelect = document.getElementById('id_saved_address');
	const saveAddressCheck = document.getElementById('save-address');

	if (showNewAddressBtn && newAddressFields) {
		showNewAddressBtn.addEventListener('click', function () {
			newAddressFields.style.display = 'block';
			if (savedAddressSelect) {
				savedAddressSelect.value = '';
				document.getElementById('saved-addresses').style.display = 'none';
				showNewAddressBtn.style.display = 'none';
			}
			if (saveAddressCheck) {
				saveAddressCheck.style.display = 'flex';
			}
		});
	}

	if (savedAddressSelect && newAddressFields) {
		savedAddressSelect.addEventListener('change', function () {
			if (this.value) {
				const selectedOption = this.options[this.selectedIndex];
				newAddressFields.style.display = 'none';
				if (saveAddressCheck) {
					saveAddressCheck.style.display = 'none';
				}
				document.getElementById('id_address_line1').value =
					selectedOption.dataset.line1 || '';
				document.getElementById('id_address_line2').value =
					selectedOption.dataset.line2 || '';
				document.getElementById('id_city').value =
					selectedOption.dataset.city || '';
				document.getElementById('id_postcode').value =
					selectedOption.dataset.postcode || '';
			} else {
				newAddressFields.style.display = 'none';
				clearNewAddressFields();
				if (saveAddressCheck) {
					saveAddressCheck.style.display = 'flex';
				}
			}
		});
	}
});

function clearNewAddressFields() {
	document.getElementById('id_full_name').value = '';
	document.getElementById('id_phone_number').value = '';
	document.getElementById('id_email').value = '';
	document.getElementById('id_address_line1').value = '';
	document.getElementById('id_address_line2').value = '';
	document.getElementById('id_city').value = '';
	document.getElementById('id_postcode').value = '';
}

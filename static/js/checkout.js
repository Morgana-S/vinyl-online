document.addEventListener('DOMContentLoaded', function () {
    // Checkout Form Details
	const showNewAddressBtn = document.getElementById('show-new-address-btn');
	const newAddressFields = document.getElementById('new-address-fields');
	const savedAddressSelect = document.getElementById('saved-address-select');
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
				document.getElementById('address-line-1').value =
					selectedOption.dataset.line1 || '';
				document.getElementById('address-line-2').value =
					selectedOption.dataset.line2 || '';
				document.getElementById('city').value =
					selectedOption.dataset.city || '';
				document.getElementById('postcode').value =
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

// Clears the fields in the New Address section
function clearNewAddressFields() {
	document.getElementById('address-line1').value = '';
	document.getElementById('address-line2').value = '';
	document.getElementById('city').value = '';
	document.getElementById('postcode').value = '';
}

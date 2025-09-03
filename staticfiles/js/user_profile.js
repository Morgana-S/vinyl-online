document.addEventListener('DOMContentLoaded', function () {
	deleteAddressButtonInit();
});

function deleteAddressButtonInit() {
	const deleteButtons = document.querySelectorAll('.delete-button');
	const deleteModal = new bootstrap.Modal(
		document.getElementById('deleteAddressModal')
	);
	const deleteForm = document.getElementById('deleteAddressForm');

	deleteButtons.forEach((btn) => {
		btn.addEventListener('click', function () {
			const actionUrl = btn.dataset.url;
			deleteForm.setAttribute('action', actionUrl);
			deleteModal.show();
		});
	});
}

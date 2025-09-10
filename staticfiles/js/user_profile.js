document.addEventListener('DOMContentLoaded', function () {
	deleteAddressButtonInit();
});

function deleteAddressButtonInit() {
	const deleteButtons = document.querySelectorAll('.delete-button');
	const deleteModal = new bootstrap.Modal(
		document.getElementById('delete-address-modal')
	);
	const deleteForm = document.getElementById('delete-address-form');

	deleteButtons.forEach((btn) => {
		btn.addEventListener('click', function () {
			const actionUrl = btn.dataset.url;
			deleteForm.setAttribute('action', actionUrl);
			deleteModal.show();
		});
	});
}

module.exports = { deleteAddressButtonInit };

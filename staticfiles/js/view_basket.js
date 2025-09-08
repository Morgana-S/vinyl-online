document.addEventListener('DOMContentLoaded', function () {
	document.querySelectorAll('.basket-qty').forEach((input) => {
		input.addEventListener('change', () => {
			input.form.submit();
		});
	});
	removeModalInit();
});


function removeModalInit() {
		const removeButtons = document.getElementsByClassName('remove-button');
		const removeModal = new bootstrap.Modal(
			document.getElementById('remove-from-basket-modal')
		);
		const removeForm = document.getElementById('remove-from-basket-form');

		Array.from(removeButtons).forEach(button => {
			button.addEventListener('click', function() {
				const actionUrl = button.dataset.url;
				removeForm.setAttribute('action', actionUrl);
				removeModal.show();
			})
		})
}
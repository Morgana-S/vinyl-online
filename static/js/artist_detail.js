document.addEventListener('DOMContentLoaded', function() {
    deleteArtistButtonInit();
})

// Initialize the delete button for the artist
function deleteArtistButtonInit() {
	const deleteButton = document.getElementById('delete-button');
	const deleteModal = new bootstrap.Modal(
		document.getElementById('deleteArtistModal')
	);
	const deleteForm = document.getElementById('deleteArtistForm');

	deleteButton.addEventListener('click', function () {
		const actionUrl = deleteButton.dataset.url;
		deleteForm.setAttribute('action', actionUrl);
		deleteModal.show();
	});
}
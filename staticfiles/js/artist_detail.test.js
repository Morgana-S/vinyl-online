/**
 * @jest-environment jsdom
 */

const { deleteArtistButtonInit } = require('./artist_detail.js');

// Mock Bootstrap Modal
global.bootstrap = {
	Modal: jest.fn().mockImplementation(() => ({
		show: jest.fn(),
	})),
};

let deleteButton, deleteModalElement, deleteForm, modalInstance;

beforeEach(() => {
	document.body.innerHTML = `
        <button id="delete-button" data-url="/artist/1/delete"></button>
        <div id="delete-artist-modal"></div>
        <form id="delete-artist-form"></form>
        `;

	deleteArtistButtonInit();
	deleteButton = document.getElementById('delete-button');
	deleteForm = document.getElementById('delete-artist-form');
	deleteModalElement = document.getElementById('delete-artist-modal');

	modalInstance = bootstrap.Modal.mock.results[0].value;
});

test('Clicking delete button sets form action and shows modal', () => {
	deleteButton.click();

	expect(deleteForm.getAttribute('action')).toBe('/artist/1/delete');

	expect(modalInstance.show).toHaveBeenCalled();
});

test('bootstrap.Modal is instantiated with the modal element', () => {
    expect(bootstrap.Modal).toHaveBeenCalledWith(deleteModalElement);
})
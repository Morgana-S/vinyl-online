/**
 * @jest-environment jsdom
 */

const { removeModalInit } = require('../../static/js/view_basket.js');

// Mock Bootstrap Modal
global.bootstrap = {
	Modal: jest.fn().mockImplementation(() => ({ show: jest.fn() })),
};

describe('Basket interactions', () => {
	describe('Basket quantity inputs', () => {
		let form, input;

		beforeEach(() => {
			form = document.createElement('form');
			form.submit = jest.fn(); // mock submit

			input = document.createElement('input');
			input.className = 'basket-qty';
			input.type = 'number';
			form.appendChild(input);

			document.body.appendChild(form);

			// Attach event listener as in your code
			document.querySelectorAll('.basket-qty').forEach((el) => {
				el.addEventListener('change', () => el.form.submit());
			});
		});

		test('Changing input calls form.submit', () => {
			input.value = 5;
			input.dispatchEvent(new Event('change'));
			expect(form.submit).toHaveBeenCalled();
		});
	});

	describe('Remove modal buttons', () => {
		let removeForm, modalInstance;

		beforeEach(() => {
			document.body.innerHTML = `
        <button class="remove-button" data-url="/item/1/remove"></button>
        <button class="remove-button" data-url="/item/2/remove"></button>
        <div id="remove-from-basket-modal"></div>
        <form id="remove-from-basket-form"></form>
      `;

			removeForm = document.getElementById('remove-from-basket-form');

			removeModalInit();

			modalInstance = bootstrap.Modal.mock.results[0].value;
		});

		test('Clicking first remove button sets form action and shows modal', () => {
			const firstButton = document.getElementsByClassName('remove-button')[0];
			firstButton.click();

			expect(removeForm.getAttribute('action')).toBe('/item/1/remove');
			expect(modalInstance.show).toHaveBeenCalled();
		});

		test('Clicking second remove button sets form action and shows modal', () => {
			const secondButton = document.getElementsByClassName('remove-button')[1];
			secondButton.click();

			expect(removeForm.getAttribute('action')).toBe('/item/2/remove');
			expect(modalInstance.show).toHaveBeenCalled();
		});
	});
});

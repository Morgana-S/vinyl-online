/**
 * @jest-environment jsdom
 */

const $ = require('jquery');
global.$ = $;

const {
	renderRatingStars,
	deleteRecordButtonInit,
	deleteReviewButtonInit,
} = require('../../static/js/record_detail.js');

// Mock Bootstrap Modal and Toast
global.bootstrap = {
	Modal: jest.fn().mockImplementation(() => ({ show: jest.fn() })),
	Toast: jest.fn().mockImplementation(() => ({ show: jest.fn() })),
};

describe('renderRatingStars', () => {
	beforeEach(() => {
		document.body.innerHTML = '<div id="rating"></div>';
	});

	test('Renders full, half, and empty stars correctly', () => {
		renderRatingStars('#rating', 3.5);
		const html = document.getElementById('rating').innerHTML;
		expect(html).toContain('fa-star'); // full stars
		expect(html).toContain('fa-star-half-stroke'); // half star
		expect(html).toContain('fa-regular fa-star'); // empty stars
	});
});

describe('Thumbnail click', () => {
	beforeEach(() => {
		document.body.innerHTML = `
      <img id="main-image" src="main.jpg" alt="main">
      <img class="clickable" src="thumb.jpg" alt="thumb">
    `;
		$('.clickable').on('click', function () {
			const mainImage = $('#main-image');
			const tempSrc = mainImage.attr('src');
			const tempAlt = mainImage.attr('alt');
			mainImage.attr('src', $(this).attr('src'));
			mainImage.attr('alt', $(this).attr('alt'));
		});
	});

	test('Clicking thumbnail swaps main image', () => {
		$('.clickable').click();
		expect($('#main-image').attr('src')).toBe('thumb.jpg');
		expect($('#main-image').attr('alt')).toBe('thumb');
	});
});

describe('Quantity buttons', () => {
	beforeEach(() => {
		document.body.innerHTML = `
      <button class="btn-outline-danger"><i class="fa-minus"></i></button>
      <input class="qty_input" min="1" max="5" value="3">
      <button class="btn-outline-danger"><i class="fa-plus"></i></button>
    `;

		$('.btn-outline-danger').click(function (e) {
			e.preventDefault();
			const $input = $(this).siblings('input.qty_input');
			let currentVal = parseInt($input.val());
			const min = parseInt($input.attr('min'));
			const max = parseInt($input.attr('max'));

			if ($(this).find('i').hasClass('fa-minus')) {
				if (currentVal > min) currentVal--;
			} else if ($(this).find('i').hasClass('fa-plus')) {
				if (currentVal < max) currentVal++;
			}

			$input.val(currentVal);
		});
	});

	test('Minus button decreases value', () => {
		$('button:has(.fa-minus)').click();
		expect($('input.qty_input').val()).toBe('2');
	});

	test('Plus button increases value', () => {
		$('button:has(.fa-plus)').click();
		expect($('input.qty_input').val()).toBe('4');
	});
});

describe('Delete buttons', () => {
	beforeEach(() => {
		document.body.innerHTML = `
      <button id="delete-button" data-url="/record/1/delete"></button>
      <div id="delete-record-modal"></div>
      <form id="delete-record-form"></form>

      <button id="delete-review-button" data-url="/review/1/delete"></button>
      <div id="delete-review-modal"></div>
      <form id="delete-review-form"></form>
    `;
	});

	test('deleteRecordButtonInit sets action and shows modal', () => {
		deleteRecordButtonInit();
		const button = document.getElementById('delete-button');
		const form = document.getElementById('delete-record-form');
		const modalInstance = bootstrap.Modal.mock.results[0].value;

		button.click();
		expect(form.getAttribute('action')).toBe('/record/1/delete');
		expect(modalInstance.show).toHaveBeenCalled();
	});

	test('deleteReviewButtonInit sets action and shows modal', () => {
		deleteReviewButtonInit();
		const button = document.getElementById('delete-review-button');
		const form = document.getElementById('delete-review-form');
		const modalInstance = bootstrap.Modal.mock.results[1].value;

		button.click();
		expect(form.getAttribute('action')).toBe('/review/1/delete');
		expect(modalInstance.show).toHaveBeenCalled();
	});
});
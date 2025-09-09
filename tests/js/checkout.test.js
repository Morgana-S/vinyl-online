/**
 * @jest-environment jsdom
 */

const {
	clearNewAddressFields,
	initCheckoutForm,
} = require('../../static/js/checkout.js');

let showNewBtn, newFields, savedSelect, saveCheck, savedAddresses;
let line1, line2, city, postcode;

beforeEach(() => {
	document.body.innerHTML = `
      <button id="show-new-address-btn"></button>
      <div id="new-address-fields" style="display:none"></div>
      <select id="saved-address-select">
        <option value="">Select</option>
        <option value="1" data-line1="123 Main" data-line2="Apt 4" data-city="London" data-postcode="E1 6AN">Home</option>
      </select>
      <div id="saved-addresses" style="display:block"></div>
      <div id="save-address" style="display:none"></div>
      <input id="address-line-1" value="">
      <input id="address-line-2" value="">
      <input id="city" value="">
      <input id="postcode" value="">
    `;

	showNewBtn = document.getElementById('show-new-address-btn');
	newFields = document.getElementById('new-address-fields');
	savedSelect = document.getElementById('saved-address-select');
	saveCheck = document.getElementById('save-address');
	savedAddresses = document.getElementById('saved-addresses');

	line1 = document.getElementById('address-line-1');
	line2 = document.getElementById('address-line-2');
	city = document.getElementById('city');
	postcode = document.getElementById('postcode');

	initCheckoutForm();
});

test('Clicking "show new address" button reveals new fields', () => {
	showNewBtn.click();

	expect(newFields.style.display).toBe('block');
	expect(savedSelect.value).toBe('');
	expect(savedAddresses.style.display).toBe('none');
	expect(showNewBtn.style.display).toBe('none');
	expect(saveCheck.style.display).toBe('flex');
});

 test('Selecting a saved address populates fields and hides new fields', () => {
		savedSelect.value = '1';
		savedSelect.dispatchEvent(new Event('change'));

		expect(newFields.style.display).toBe('none');
		expect(saveCheck.style.display).toBe('none');

		expect(line1.value).toBe('123 Main');
		expect(line2.value).toBe('Apt 4');
		expect(city.value).toBe('London');
		expect(postcode.value).toBe('E1 6AN');
 });

  test('Selecting blank option clears fields and shows save address checkbox', () => {
		savedSelect.value = '';
		line1.value = 'should clear';
		line2.value = 'should clear';
		city.value = 'should clear';
		postcode.value = 'should clear';

		savedSelect.dispatchEvent(new Event('change'));

		expect(newFields.style.display).toBe('none');
		expect(saveCheck.style.display).toBe('flex');

		expect(line1.value).toBe('');
		expect(line2.value).toBe('');
		expect(city.value).toBe('');
		expect(postcode.value).toBe('');
	});

  test('clearNewAddressFields clears all input fields', () => {
		line1.value = '123';
		line2.value = '456';
		city.value = 'City';
		postcode.value = 'Zip';

		clearNewAddressFields();

		expect(line1.value).toBe('');
		expect(line2.value).toBe('');
		expect(city.value).toBe('');
		expect(postcode.value).toBe('');
	});
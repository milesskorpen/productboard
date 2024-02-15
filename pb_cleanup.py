import requests
import time

# API details
headers = {
	'X-Version': '1',
	'Authorization': 'Bearer INSERT-YOUR-TOKEN-HERE'
}

base_url = 'https://api.productboard.com'
companies_endpoint = '/companies'
delete_endpoint = '/companies/{company_id}'

n = 0

def delete_companies_in_batches(batch):
	global n
	i = 1
	for company in batch:
		company_id = company['id']
		company_name = company['name']
		
		if company['sourceOrigin'] == 'salesforce':
			delete_response = requests.delete(f'{base_url}{delete_endpoint.format(company_id=company_id)}', headers=headers)
			if delete_response.status_code == 204:
				print(f'{n}. Successfully deleted company: {company_name} // {company_id}')
				n += 1
			else:
				print(f'Failed to delete company ID: {company_id}', delete_response.status_code)
			
			if i == 50:
				time.sleep(1)  # Respect the rate limit
				i = 1
			else:
				i += 1
		else:
			print(f'NOT FROM SALES FORCE: {company_name} // {company_id}')

def get_and_delete_companies():
	page = 1
	while True:
		response = requests.get(f'{base_url}{companies_endpoint}?hasNotes=false&pageOffset={page}', headers=headers)
		if response.status_code != 200:
			print('Failed to retrieve companies:', response.status_code)
			break

		companies = response.json()['data']
		if not companies:
			break  # Exit the loop if no companies are returned

		print(f"Deleting companies on page {page}...")
		delete_companies_in_batches(companies)

		page += 1  # Move to the next page

get_and_delete_companies()
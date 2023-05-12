import unittest
import requests

# Base URL of Flask Application
base_url = 'http://fair-rent-split.com:30022'  

class TestLogin(unittest.TestCase):

    # Test login endpoint with correct credentials
    def test_login_with_correct_credentials(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = requests.post(f'{base_url}/login', data=login_data)
        self.assertEqual(response.status_code, 200)
    
    # Test login endpoint with incorrect credentials
    '''
    def test_login_with_incorrect_credentials(self):
        login_data = {
            'username': 'wronguser@gmail.com',
            'password': 'wrongpassword123'
        }
    '''

    # Test the register endpoint correct details
    def test_register_with_correct_credentials(self):
        register_data = {
            'username': 'newuser',
            'email': 'newuser@gmail.com',
            'password': 'newuser123',
            'confirm_password': 'newuser123'
        }
        response = requests.post(f'{base_url}/register', data=register_data)
        self.assertEqual(response.status_code, 200)

    # Test the register endpoint with incorrect details

    # Test the size_input endpoint

    # Test the matrix_input endpoint with correct details

    # Test the matrix_input endpoint with incorrect details

    # Test the output endpoint

if __name__ == '__main__':
    unittest.main()

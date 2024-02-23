import unittest
import unittest.mock as mock
import requests
import json

API_GATEWAY_URL='http://127.0.0.1:8000/api/'


class TestAuthAPI(unittest.TestCase):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    def setUp(self):
        json_data = {
            "username": "jankee1",
            "password": "password_1"
        }

        response = requests.post(
            "{}/login/".format(API_GATEWAY_URL), 
            headers=self.headers, json=json_data
        )
        res_dict = response.json()
        self.logged_in_user_id = res_dict['data']['user']['id']
        self.token =res_dict['data']['token']
        # self.headers['Authorization'] = f"Bearer {self.token}"


# -------------------login/token----------------------
    def test_token_valid_credentials(self):

        json_data = {
            "username": "jankee1",
            "password": "password_1"
        }

        response = requests.post('{}/login/'.format(API_GATEWAY_URL), 
            headers=self.headers,
            json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 200)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                        {
                            "token": "f03439b311e4b27d6b4d3dae76916a8c479989a5"
                        }
                    }
        )

    def test_token_invalid_password(self):
        json_data = {
            'username': 'jankee1',
            'password': 'ztech@441'
        }

        response = requests.post('{}/login/'.format(API_GATEWAY_URL), 
            headers=self.headers,
            json=json_data)
        # Status code should be 401 as per swagger
        self.assertEqual(response.status_code, 401)
        res_dict = response.json()
        self.assertEqual(res_dict, {
                            "error": "Invalid credentials"
                            }
                        )

    def test_token_invalid_username(self):
        json_data = {
            'username': 'jkdd',
            'password': 'password_1'
        }

        response = requests.post('{}/login/'.format(API_GATEWAY_URL), \
            headers=self.headers,
            json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 401)
        res_dict = response.json()
        self.assertEqual(res_dict, {
                            "code": 400,
                            "data": {},
                            "message": "Invalid email or password."
                            }
                        )

    def test_token_invalid_credentials(self):
        json_data = [
            {
            'username': '<script>user</script>',
            'password': '<script>pswd</script>',

            }
        ]

        for json_data in json_data:
            response = requests.post('{}/login/'.format(API_GATEWAY_URL), \
                headers=self.headers,
                json=json_data)
            # Status code should be 200
            self.assertEqual(response.status_code, 400)
            res_dict = response.json()
            self.assertEqual(
                res_dict, {
                        "error": "Invalid credentials"
                    }
            )

# # -------------------Create Notes----------------------
    def test_create_notes_with_token(self):

        self.headers['Authorization'] = f"Bearer {self.token}"
        json_data = {
            "title":"title1",
            "content":"content1",
        }

        response = requests.post('{}/notes/create/'.format(API_GATEWAY_URL), 
            headers=self.headers,
            json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 200)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                    "id": 2,
                    "title": "title1",
                    "content": "content1",
                    "created_at": "2024-02-23T17:57:34.840827Z",
                    "updated_at": "2024-02-23T17:57:34.840827Z",
                    "owner": 2
                    
                    }
        )

    def test_create_notes_without_token(self):

        json_data = {
            "title":"title1",
            "content":"content1",
        }

        response = requests.post('{}/notes/create/'.format(API_GATEWAY_URL), 
            headers=self.headers,
            json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 400)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                    "id": 2,
                    "title": "title1",
                    "content": "content1",
                    "created_at": "2024-02-23T17:57:34.840827Z",
                    "updated_at": "2024-02-23T17:57:34.840827Z",
                    "owner": 2
                    
                }
        )



# # -------------------Get Notes----------------------

    def test_gate_notes_valid_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"
        response = requests.get('{}/notes/2/'.format(API_GATEWAY_URL), 
            headers=self.headers)
        # Status code should be 200
        self.assertEqual(response.status_code, 200)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                    "id": 2,
                    "title": "title1",
                    "content": "content1",
                    "created_at": "2024-02-23T17:57:34.840827Z",
                    "updated_at": "2024-02-23T17:57:34.840827Z",
                    "owner": 2
                    
                }
        )

    def test_gate_notes_invalid_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"
        response = requests.get('{}/notes/200/'.format(API_GATEWAY_URL), 
            headers=self.headers)
        # Status code should be 200
        self.assertEqual(response.status_code, 400)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                     "error": "Invalid id"  
                }
        )


# # -------------------Share Notes----------------------
    def test_share_notes_valid_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"

        json_data = {
            "note_id": 1,
            "shared_with": ["jankee3"]
        }

        response = requests.post('{}/notes/share/'.format(API_GATEWAY_URL), 
            headers=self.headers, json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 200)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                   'message': 'Note shared successfully'
                }
        )

    def test_share_notes_invalid_note_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"
        json_data = {
            "note_id": 1000,
            "shared_with": ["jankee3"]
        }
        response = requests.post('{}/notes/share/'.format(API_GATEWAY_URL), 
            headers=self.headers, json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 404)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                     "error": "Note not found"  
                }
        )


    def test_share_notes_invalid_user_id(self):
       
        json_data = {
            "note_id": 1,
            "shared_with": ["jankee3"]
        }
        response = requests.post('{}/notes/share/'.format(API_GATEWAY_URL), 
            headers=self.headers, json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 404)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                     "error": "User not found"  
                }
        )




# # -------------------Update Notes----------------------
        
    def test_update_notes_valid_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"

        json_data = {
            "title": "Updated Note Title",
             "content": "Updated note content."
        }

        response = requests.put('{}/notes/update/1/'.format(API_GATEWAY_URL), 
            headers=self.headers, json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code, 200)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                   'message': 'Note shared successfully'
                }
        )

    def test_update_notes_invalid_note_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"
        json_data = {
             "title": "Updated Note Title",
             "content": "Updated note content."
        }
        response = requests.put('{}/notes/update/1000/'.format(API_GATEWAY_URL), 
            headers=self.headers, json=json_data)
        # Status code should be 200
        self.assertEqual(response.status_code,404)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                     "error": "Note not found"  
                }
        )

# # -------------------Virsion history ----------------------
        
    def test_version_history_valid_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"
        response = requests.get('{}/notes/version-history/1/'.format(API_GATEWAY_URL), 
            headers=self.headers)
        # Status code should be 200
        self.assertEqual(response.status_code, 200)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                   'message': 'Note shared successfully'
                }
        )

    def test_version_history_invalid_note_id(self):
        self.headers['Authorization'] = f"Bearer {self.token}"

        response = requests.get('{}/notes/version-history/1000/'.format(API_GATEWAY_URL), 
            headers=self.headers)
        # Status code should be 200
        self.assertEqual(response.status_code,404)
        res_dict = response.json()

        self.assertEqual(
            res_dict,{
                     "error": "Note not found"  
                }
        )
